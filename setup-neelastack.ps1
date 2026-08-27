$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Frontend = Join-Path $Root "frontend\web"
$EnvFile = Join-Path $Root ".env"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "              NEELASTACK BOOTSTRAP" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

function Step($Number, $Text) {
    Write-Host ""
    Write-Host "[$Number] $Text" -ForegroundColor Yellow
}

function Fail($Text) {
    Write-Host ""
    Write-Host "ERROR: $Text" -ForegroundColor Red
    Write-Host ""
    exit 1
}

function Check-Command($CommandName, $InstallHint) {
    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) {
        Fail "$CommandName was not found. $InstallHint"
    }
}

Set-Location $Root

# --------------------------------------------------
# 1. Environment
# --------------------------------------------------

Step "01/10" "Checking environment"

Check-Command "python" "Install Python 3.11+ and restart PowerShell."
Check-Command "node" "Install Node.js and restart PowerShell."
Check-Command "npm" "Install Node.js/npm and restart PowerShell."
Check-Command "docker" "Install Docker Desktop and make sure Docker is running."

$PythonVersion = python --version
$NodeVersion = node --version
$DockerVersion = docker --version

Write-Host "Python : $PythonVersion" -ForegroundColor DarkGray
Write-Host "Node   : $NodeVersion" -ForegroundColor DarkGray
Write-Host "Docker : $DockerVersion" -ForegroundColor DarkGray

# --------------------------------------------------
# 2. Environment file
# --------------------------------------------------

Step "02/10" "Checking environment configuration"

if (-not (Test-Path $EnvFile)) {
    $ExampleEnv = Join-Path $Root ".env.example"

    if (Test-Path $ExampleEnv) {
        Copy-Item $ExampleEnv $EnvFile
        Write-Host ".env created from .env.example" -ForegroundColor Green
    }
    else {
        Write-Host "WARNING: .env and .env.example are missing." -ForegroundColor Yellow
    }
}
else {
    Write-Host ".env already exists - keeping existing configuration." -ForegroundColor Green
}

# --------------------------------------------------
# 3. Python virtual environment
# --------------------------------------------------

Step "03/10" "Preparing Python environment"

$Venv = Join-Path $Root ".venv"
$PythonExe = Join-Path $Venv "Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    Write-Host "Creating .venv..." -ForegroundColor Cyan
    python -m venv $Venv
}

if (-not (Test-Path $PythonExe)) {
    Fail "Python virtual environment could not be created."
}

& $PythonExe -m pip install --upgrade pip

# Install declared project/dev dependencies if available.
Write-Host "Installing declared Python dependencies..." -ForegroundColor Cyan

try {
    & $PythonExe -m pip install -e ".[dev]"
}
catch {
    Write-Host ""
    Write-Host "WARNING: pyproject.toml does not currently declare all runtime dependencies." -ForegroundColor Yellow
    Write-Host "The API health check below will identify any missing imports." -ForegroundColor Yellow
}

# --------------------------------------------------
# 4. Docker services
# --------------------------------------------------

Step "04/10" "Starting PostgreSQL, Redis and Ollama"

docker compose up -d

if ($LASTEXITCODE -ne 0) {
    Fail "Docker Compose could not start."
}

Start-Sleep -Seconds 5

docker compose ps

# --------------------------------------------------
# 5. Database migration
# --------------------------------------------------

Step "05/10" "Checking database migrations"

$Alembic = Join-Path $Root "alembic.ini"

if (Test-Path $Alembic) {
    try {
        & $PythonExe -m alembic upgrade head
        Write-Host "Database migrations completed." -ForegroundColor Green
    }
    catch {
        Write-Host "WARNING: Database migration did not complete." -ForegroundColor Yellow
        Write-Host "Continuing to API validation..." -ForegroundColor Yellow
    }
}
else {
    Write-Host "No alembic.ini found. Skipping migrations." -ForegroundColor DarkGray
}

# --------------------------------------------------
# 6. Ollama
# --------------------------------------------------

Step "06/10" "Checking Ollama"

try {
    $OllamaResponse = Invoke-WebRequest `
        -Uri "http://127.0.0.1:11434/api/tags" `
        -UseBasicParsing `
        -TimeoutSec 5

    if ($OllamaResponse.StatusCode -eq 200) {
        Write-Host "Ollama is online." -ForegroundColor Green
    }
}
catch {
    Write-Host "WARNING: Ollama API is not responding yet." -ForegroundColor Yellow
}

# Do not automatically download a multi-GB model.
# Model installation is intentionally left to the user.

Write-Host ""
Write-Host "Ollama model download is NOT automatic." -ForegroundColor DarkGray
Write-Host "Use: docker exec -it neelastack-ollama-1 ollama pull llama3.2" -ForegroundColor DarkGray

# --------------------------------------------------
# 7. Frontend dependencies
# --------------------------------------------------

Step "07/10" "Preparing frontend"

if (-not (Test-Path (Join-Path $Frontend "package.json"))) {
    Fail "frontend\web\package.json was not found."
}

Set-Location $Frontend

if (-not (Test-Path (Join-Path $Frontend "node_modules"))) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    npm install
}
else {
    Write-Host "node_modules already exists - running npm install for consistency." -ForegroundColor DarkGray
    npm install
}

Set-Location $Root

# --------------------------------------------------
# 8. Frontend build
# --------------------------------------------------

Step "08/10" "Building frontend"

Set-Location $Frontend

npm run build

if ($LASTEXITCODE -ne 0) {
    Set-Location $Root
    Fail "Frontend build failed."
}

Set-Location $Root

Write-Host "Frontend build completed." -ForegroundColor Green

# --------------------------------------------------
# 9. Start API
# --------------------------------------------------

Step "09/10" "Starting FastAPI backend"

$ApiLog = Join-Path $Root "neelastack-api.log"

if (Test-Path $ApiLog) {
    Remove-Item $ApiLog -Force
}

$ApiProcess = Start-Process `
    -FilePath $PythonExe `
    -ArgumentList "-m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000" `
    -WorkingDirectory $Root `
    -RedirectStandardOutput ".\api.stdout.log" `
    -RedirectStandardError ".\api.stderr.log" `
    -PassThru

Write-Host "API PID: $($ApiProcess.Id)" -ForegroundColor DarkGray

# Wait for API
$ApiReady = $false

for ($i = 1; $i -le 30; $i++) {
    Start-Sleep -Seconds 1

    try {
        $Health = Invoke-WebRequest `
            -Uri "http://127.0.0.1:8000/docs" `
            -UseBasicParsing `
            -TimeoutSec 2

        if ($Health.StatusCode -eq 200) {
            $ApiReady = $true
            break
        }
    }
    catch {
        # API still starting.
    }
}

if (-not $ApiReady) {
    Write-Host ""
    Write-Host "API failed to become ready." -ForegroundColor Red
    Write-Host ""
    Write-Host "========== API LOG ==========" -ForegroundColor Red

    if (Test-Path $ApiLog) {
        Get-Content $ApiLog -Tail 80
    }

    Write-Host "=============================" -ForegroundColor Red
    exit 1
}

Write-Host "FastAPI is online: http://127.0.0.1:8000" -ForegroundColor Green

# --------------------------------------------------
# 10. Final status + frontend server
# --------------------------------------------------

Step "10/10" "Starting NEELASTACK frontend"

$FrontendLog = Join-Path $Root "neelastack-frontend.log"

if (Test-Path $FrontendLog) {
    Remove-Item $FrontendLog -Force
}

$FrontendProcess = Start-Process `
    -FilePath "npm.cmd" `
    -ArgumentList "run dev -- --host 127.0.0.1 --port 5173" `
    -WorkingDirectory $Frontend `
    -RedirectStandardOutput $FrontendLog `
    -RedirectStandardError $FrontendLog `
    -PassThru

Write-Host "Frontend PID: $($FrontendProcess.Id)" -ForegroundColor DarkGray

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "             NEELASTACK READY" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend : http://127.0.0.1:5173" -ForegroundColor Cyan
Write-Host "API      : http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "API Docs : http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Postgres: localhost:5432" -ForegroundColor DarkGray
Write-Host "Redis   : localhost:6379" -ForegroundColor DarkGray
Write-Host "Ollama  : http://127.0.0.1:11434" -ForegroundColor DarkGray
Write-Host ""
Write-Host "API log      : .\neelastack-api.log" -ForegroundColor DarkGray
Write-Host "Frontend log : .\neelastack-frontend.log" -ForegroundColor DarkGray
Write-Host ""
Write-Host "NEELASTACK startup completed." -ForegroundColor Green
Write-Host ""