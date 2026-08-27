# 🐦 NEELASTACK

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi\&logoColor=white)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react\&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Frontend-646CFF?logo=vite\&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-000000)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql\&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Queue%20%26%20Cache-DC382D?logo=redis\&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![RAG](https://img.shields.io/badge/AI-RAG-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **A local-first AI engineering platform for building, running, and experimenting with AI agents, chat, workflows, RAG, voice, tools, and background jobs — primarily on your own machine.**

NEELASTACK is a **full-stack AI engineering platform** designed around one principle:

> **Run AI locally first. Use external APIs only when you choose to.**

The default development setup can use a local **Ollama** model, allowing you to experiment with AI applications without requiring a paid OpenAI API key.

The platform combines a **FastAPI backend**, **React + TypeScript frontend**, **Ollama-based local inference**, **PostgreSQL**, **Redis**, background workers, authentication, RAG capabilities, voice services, agent orchestration, and Docker-based development.

---

# 📌 Project Overview

Modern AI applications are more than a chatbot.

A production-oriented AI system needs:

* model providers
* authentication
* conversations
* memory
* agents
* workflows
* background jobs
* retries
* cancellation
* tool execution
* RAG
* embeddings
* voice
* observability
* security
* rate limiting
* persistence
* APIs
* web interfaces

**NEELASTACK brings these components together into one modular AI engineering platform.**

The architecture is designed to work **locally by default**, while still allowing external providers to be configured when required.

---

# 🎯 Core Philosophy

### 🏠 Local First

The default setup is designed to run primarily on your own machine.

```text
React
   ↓
FastAPI
   ↓
Provider Router
   ↓
Ollama
   ↓
Local AI Model
```

No paid AI API is required for the default local chat workflow.

---

### 🔌 Provider Agnostic

NEELASTACK separates application logic from model providers.

```text
                 ┌── Ollama
                 │
Provider Router ─┼── OpenAI
                 │
                 ├── Groq
                 │
                 └── Future Providers
```

If an external API key is available, an additional provider can be configured without redesigning the application.

---

### ⚙️ Engineering First

NEELASTACK is intended not only as a chatbot, but as an environment for experimenting with:

* AI agents
* orchestration
* RAG
* tools
* workflows
* memory
* background processing
* voice
* model routing
* evaluations
* observability
* security

---

# ✨ Features

## 🤖 AI Chat

* Local AI chat through Ollama
* Provider abstraction
* Streaming responses
* Conversation history
* Persistent conversations
* Configurable model providers
* Optional external providers

---

## 🧠 AI Agents

Modular agent architecture for specialized tasks.

Example agent roles include:

* Planner
* Researcher
* Analyst
* Coder
* Reviewer
* Executor

Agents can be composed into workflows and orchestration pipelines.

---

## 🔄 Workflow Orchestration

Support for multi-step AI workflows.

```text
User Request
     │
     ▼
Planner
     │
     ▼
Researcher
     │
     ▼
Analyst
     │
     ▼
Coder
     │
     ▼
Reviewer
     │
     ▼
Final Result
```

The orchestration layer provides reusable building blocks for complex AI tasks.

---

# ⚡ Background Job System

Long-running operations are designed to execute through background jobs instead of blocking HTTP requests.

Supported task categories include:

* Chat
* Speech-to-Text
* Text-to-Speech
* AI processing
* Tool execution
* Other asynchronous workloads

### Job lifecycle

```text
QUEUED
   │
   ▼
RUNNING
   │
   ├──────────────► FAILED
   │                  │
   │                  ▼
   │                RETRY
   │
   ▼
COMPLETED

QUEUED / RUNNING
        │
        ▼
    CANCELLED
```

Jobs can expose:

* status
* progress
* attempts
* retries
* errors
* results
* timestamps
* cancellation state

---

# 🎙️ Voice AI

NEELASTACK includes a modular voice architecture.

### Speech-to-Text

```text
Microphone
    ↓
Audio
    ↓
STT Provider
    ↓
Text
    ↓
AI Pipeline
```

### Text-to-Speech

```text
AI Response
    ↓
TTS Provider
    ↓
Audio
    ↓
User
```

The provider abstraction allows local or optional external voice implementations.

---

# 📚 Local RAG

NEELASTACK includes a Retrieval-Augmented Generation architecture for working with documents.

```text
Document
   ↓
Loader
   ↓
Text Extraction
   ↓
Chunking
   ↓
Local Embeddings
   ↓
Vector Store
   ↓
Retriever
   ↓
Relevant Context
   ↓
AI Model
   ↓
Answer
```

This allows the platform to answer questions using user-provided documents rather than relying only on the model's built-in knowledge.

---

# 🧩 Tool System

The platform provides a modular tool architecture for extending AI agents.

Example tool categories include:

* Filesystem tools
* HTTP tools
* Code tools
* Database handlers
* Tool execution
* Permissions
* Validation
* Sandboxing

This allows agents to move beyond text generation into controlled tool execution.

---

# 🔐 Authentication & Security

NEELASTACK includes authentication and security-oriented components such as:

* User registration
* Login
* JWT authentication
* Password hashing
* Role-based access control
* Protected API routes
* Permission checks
* Security middleware
* Rate limiting
* Prompt-injection testing
* Tool permissions

Example authentication flow:

```text
Register
   ↓
Password Hash
   ↓
Database
   ↓
JWT
   ↓
Authenticated API Requests
```

---

# 🚦 Rate Limiting

The API architecture includes shared rate-limiting support to help protect endpoints from excessive requests.

Rate limiting can be applied across API workloads rather than relying only on individual frontend clients.

---

# 📊 Observability

The project includes an observability layer for monitoring application behavior.

Areas include:

* logging
* metrics
* telemetry
* tracing
* application state
* request visibility
* AI workflow execution

This provides a foundation for moving from local development toward production environments.

---

# 🗄️ Data & Persistence

NEELASTACK uses persistent storage for application state.

### PostgreSQL

Used for structured application data such as:

* users
* projects
* agents
* conversations
* messages
* documents
* workflows
* jobs
* memory
* audit information

### Redis

Used for infrastructure such as:

* job processing
* queues
* shared state
* caching
* coordination

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │   React + TypeScript │
                         │      Web App         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │        API           │
                         └──────────┬───────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
     Authentication             Chat/API                  Jobs
          │                         │                         │
          │                         ▼                         ▼
          │                  Provider Router               Redis
          │                         │                         │
          │              ┌──────────┼──────────┐              ▼
          │              │          │          │           Worker
          │              ▼          ▼          ▼
          │           Ollama     OpenAI     Groq
          │
          ├──────────────────────────────────────┐
          │                                      │
          ▼                                      ▼
     PostgreSQL                              RAG System
                                                 │
                                         ┌───────┴───────┐
                                         ▼               ▼
                                    Embeddings       Vector Store

                         Voice
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
                 STT               TTS
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic
* Alembic

## Frontend

* React
* TypeScript
* Vite
* CSS
* Modern component architecture

## AI

* Ollama
* Local LLMs
* Provider abstraction
* Streaming
* Agents
* Workflows
* RAG
* Embeddings

## Database

* PostgreSQL
* SQLAlchemy ORM
* Alembic migrations

## Infrastructure

* Redis
* Docker
* Docker Compose
* Worker processes

## Security

* JWT
* Password hashing
* RBAC
* Permissions
* Rate limiting
* Security testing

## Testing

* Pytest
* Integration tests
* Unit tests
* Security tests
* Evaluation tests
* Load testing

---

# 📂 Project Structure

```text
NEELASTACK/
│
├── apps/
│   ├── api/
│   │   └── main.py
│   │
│   ├── cli/
│   │   └── main.py
│   │
│   └── worker/
│       └── main.py
│
├── frontend/
│   ├── web/
│   │   ├── src/
│   │   │   ├── api/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── layouts/
│   │   │   ├── pages/
│   │   │   ├── services/
│   │   │   ├── store/
│   │   │   ├── types/
│   │   │   └── utils/
│   │   │
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── vite.config.ts
│   │
│   └── mobile/
│
├── packages/
│   └── neelastack/
│       │
│       ├── agents/
│       ├── api/
│       ├── auth/
│       ├── core/
│       ├── database/
│       ├── evaluations/
│       ├── mcp/
│       ├── memory/
│       ├── models/
│       ├── observability/
│       ├── orchestration/
│       ├── providers/
│       ├── rag/
│       ├── skills/
│       ├── storage/
│       ├── tools/
│       ├── voice/
│       └── workflows/
│
├── alembic/
│   └── versions/
│
├── infrastructure/
│   ├── compose/
│   ├── docker/
│   ├── kubernetes/
│   └── terraform/
│
├── scripts/
│
├── tests/
│   ├── agents/
│   ├── evaluations/
│   ├── integration/
│   ├── load/
│   ├── security/
│   └── unit/
│
├── docs/
│   ├── AGENTS.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── EVALUATIONS.md
│   ├── MCP.md
│   ├── MEMORY.md
│   ├── OBSERVABILITY.md
│   ├── ORCHESTRATION.md
│   ├── PRODUCTION.md
│   ├── RAG.md
│   ├── SECURITY.md
│   └── VOICE.md
│
├── .env.example
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# 🚀 Quick Start

## 1. Clone the Repository

```bash
git clone https://github.com/simhadris17/NEELASTACK.git
cd NEELASTACK
```

---

# 2. Create Environment File

Copy the example environment file:

### Windows

```powershell
Copy-Item .env.example .env
```

### Linux/macOS

```bash
cp .env.example .env
```

Review `.env` and adjust values if required.

> Never commit secrets or API keys to Git.

---

# 3. Install Ollama

Install Ollama on your machine and verify that it is available:

```bash
ollama --version
```

Check installed models:

```bash
ollama list
```

Pull a local model if necessary:

```bash
ollama pull llama3.2
```

You can use another Ollama-supported model according to your hardware.

---

# 4. Start the Stack with Docker Compose

```bash
docker compose up --build
```

The local stack can include:

* FastAPI
* React web application
* PostgreSQL
* Redis
* Worker services

---

# 5. Open the Application

### Web Application

```text
http://localhost:3000
```

### FastAPI

```text
http://localhost:8000
```

### Interactive API Documentation

```text
http://localhost:8000/docs
```

### OpenAPI Schema

```text
http://localhost:8000/openapi.json
```

---

# 🧪 Local API Health Check

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
"ok"
```

---

# 🔐 Authentication Example

## Register

```http
POST /auth/register
```

Example:

```json
{
  "email": "user@example.com",
  "password": "test1234"
}
```

---

## Login

```http
POST /auth/login
```

Example:

```json
{
  "email": "user@example.com",
  "password": "test1234"
}
```

Example response:

```json
{
  "access_token": "YOUR_JWT_TOKEN",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}
```

---

# 💬 Local AI Chat

The default architecture is designed to use Ollama.

```text
User
 │
 ▼
React
 │
 ▼
FastAPI
 │
 ▼
Provider Router
 │
 ▼
Ollama
 │
 ▼
Local Model
 │
 ▼
Response
```

This means a local development setup does not have to depend on a paid OpenAI API key.

---

# 🔌 Optional External Providers

NEELASTACK can be extended with external providers when API keys are available.

Example environment configuration:

```env
# Local-first default
OLLAMA_BASE_URL=http://localhost:11434

# Optional providers
OPENAI_API_KEY=
GROQ_API_KEY=
```

If no external key is configured, the application should continue using the local provider where supported.

---

# 🧠 RAG Example

A typical RAG workflow:

```text
Upload Document
      ↓
Extract Text
      ↓
Split into Chunks
      ↓
Generate Embeddings
      ↓
Store Vectors
      ↓
User Question
      ↓
Similarity Retrieval
      ↓
Relevant Context
      ↓
Local LLM
      ↓
Answer
```

This makes NEELASTACK useful for experimenting with:

* personal knowledge bases
* documentation assistants
* project knowledge
* local research
* private documents

---

# ⚡ Job API

Example conceptual job lifecycle:

```http
POST /jobs
GET  /jobs/{job_id}
POST /jobs/{job_id}/cancel
GET  /jobs/{job_id}/result
```

A job can expose:

```json
{
  "id": "job_123",
  "status": "running",
  "progress": 65,
  "attempt": 1,
  "max_attempts": 3
}
```

Completed jobs can return their associated result, while failed jobs can be retried according to configured retry behavior.

---

# 🎙️ Voice Workflow

### STT

```text
Audio
 ↓
Speech-to-Text Job
 ↓
Worker
 ↓
Transcript
```

### TTS

```text
Text
 ↓
Text-to-Speech Job
 ↓
Worker
 ↓
Audio
```

Both workflows can be processed asynchronously.

---

# 📡 API Design

The API is organized into modular domains such as:

```text
/auth
/agents
/chat
/conversations
/evaluations
/files
/history
/jobs
/mcp
/memory
/observability
/projects
/rag
/security
/tools
/voice
/workflows
```

For the authoritative endpoint list, use:

```text
http://localhost:8000/docs
```

---

# 🧪 Testing

Run the test suite with:

```bash
pytest
```

The repository includes tests covering areas such as:

```text
tests/
├── agents/
├── evaluations/
├── integration/
├── load/
├── security/
└── unit/
```

Security-oriented tests include areas such as:

* permissions
* authentication
* prompt injection
* security behavior

---

# 🐳 Docker Development

Build the complete environment:

```bash
docker compose build
```

Start:

```bash
docker compose up
```

Start in background:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

---

# 🗃️ Database Migrations

Apply migrations with the project's migration tooling:

```bash
alembic upgrade head
```

The repository contains versioned migrations under:

```text
alembic/versions/
```

---

# 🧰 Development Scripts

The repository includes helper scripts under:

```text
scripts/
```

Typical development operations include:

```text
dev
build
health
lint
migrate
seed
test
deploy
```

Use the appropriate platform-specific script when available.

---

# ☁️ Deployment

NEELASTACK is designed with multiple deployment targets in mind.

Possible environments include:

* Local development
* Docker
* Docker Compose
* Cloud VMs
* Kubernetes
* Terraform-managed infrastructure
* Vercel for the web frontend
* Other container platforms

The important distinction is:

> **Local Ollama development and public cloud deployment are different environments.**

A Vercel-hosted frontend cannot directly access:

```text
127.0.0.1
```

on your personal computer.

For a public deployment, the API must be reachable by the deployed frontend.

---

# 🏠 Recommended Local Architecture

For development:

```text
┌─────────────────────────────┐
│       Your Computer         │
│                             │
│  React                      │
│    │                        │
│    ▼                        │
│  FastAPI                    │
│    │                        │
│    ├── PostgreSQL            │
│    ├── Redis                 │
│    ├── Worker                │
│    └── Ollama                │
│          │                  │
│          ▼                  │
│       Local LLM              │
│                             │
└─────────────────────────────┘
```

This is the preferred setup when privacy, cost, and local experimentation are priorities.

---

# 🔒 Security Notes

Do not commit:

```text
.env
API keys
JWT secrets
database passwords
private credentials
production secrets
```

Use:

```text
.env.example
```

for safe configuration templates.

For production deployments:

* use strong secrets
* enable HTTPS
* restrict CORS
* protect database access
* protect Redis
* configure proper authentication
* use production logging
* configure rate limiting
* review tool permissions
* avoid exposing internal services publicly

---

# 📈 Production-Oriented Architecture

The repository contains infrastructure for scaling beyond a single-machine development environment.

```text
                         Load Balancer
                              │
                 ┌────────────┴────────────┐
                 │                         │
              API #1                    API #2
                 │                         │
                 └────────────┬────────────┘
                              │
                         Redis / Queue
                              │
                 ┌────────────┴────────────┐
                 │                         │
             Worker #1                 Worker #2
                 │                         │
                 └────────────┬────────────┘
                              │
                         PostgreSQL
```

Infrastructure directories include:

```text
infrastructure/
├── compose/
├── docker/
├── kubernetes/
└── terraform/
```

---

# 🧭 Roadmap

Future improvements can include:

* [ ] More local LLM integrations
* [ ] Improved model routing
* [ ] Advanced agent memory
* [ ] Better RAG evaluation
* [ ] More embedding providers
* [ ] Advanced vector databases
* [ ] More STT providers
* [ ] More TTS providers
* [ ] Real-time voice conversations
* [ ] Agent marketplace
* [ ] Plugin system
* [ ] Advanced workflow editor
* [ ] Distributed workers
* [ ] Advanced observability
* [ ] Production-grade deployment presets
* [ ] Kubernetes autoscaling
* [ ] More comprehensive evaluation suites

---

# 📚 Documentation

Project documentation is available under:

```text
docs/
```

Important documentation areas include:

| Document           | Purpose                        |
| ------------------ | ------------------------------ |
| `ARCHITECTURE.md`  | System architecture            |
| `AGENTS.md`        | Agent architecture             |
| `ORCHESTRATION.md` | AI orchestration               |
| `RAG.md`           | Retrieval-Augmented Generation |
| `MEMORY.md`        | Memory architecture            |
| `VOICE.md`         | Voice system                   |
| `MCP.md`           | MCP integration                |
| `SECURITY.md`      | Security architecture          |
| `OBSERVABILITY.md` | Monitoring and telemetry       |
| `EVALUATIONS.md`   | AI evaluation                  |
| `DEPLOYMENT.md`    | Deployment                     |
| `PRODUCTION.md`    | Production considerations      |

---

# 💡 Why NEELASTACK?

Traditional AI application development often looks like:

```text
Frontend
   ↓
API
   ↓
One AI API
```

NEELASTACK is designed as a broader engineering platform:

```text
                    NEELASTACK
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
     Agents            RAG              Voice
       │                 │                 │
       ├──────────────┐  │  ┌──────────────┤
       │              │  │  │              │
   Workflows        Memory │ STT           TTS
       │              │  │  │              │
       └──────────────┼──┼──┼──────────────┘
                      │  │
                    Tools
                      │
                  Job System
                      │
                 Provider Router
                      │
              ┌───────┴────────┐
              │                │
            Ollama          External APIs
              │
          Local Models
```

The goal is to provide a **single engineering foundation** for experimenting with modern AI systems while keeping the default development environment local.

---

# 📊 What This Project Demonstrates

NEELASTACK demonstrates practical engineering across multiple areas:

### AI Engineering

* Local LLM inference
* Provider abstraction
* Agent architecture
* AI orchestration
* RAG
* Embeddings
* Memory
* Voice
* AI evaluations

### Backend Engineering

* FastAPI
* REST APIs
* JWT authentication
* SQLAlchemy
* PostgreSQL
* Redis
* Background workers
* Job queues
* Retry mechanisms
* API validation

### Frontend Engineering

* React
* TypeScript
* Vite
* Component architecture
* API integration
* Streaming UI
* Chat interface
* Voice controls
* Dashboard interfaces

### Infrastructure

* Docker
* Docker Compose
* Kubernetes
* Terraform
* CI/CD
* Production configuration

### Security

* Authentication
* Authorization
* RBAC
* Rate limiting
* Permission systems
* Prompt-injection testing
* Secure configuration

---

# 🏷️ GitHub Topics

```text
ai
artificial-intelligence
ai-engineering
local-ai
local-first
ollama
llm
fastapi
react
typescript
vite
python
rag
retrieval-augmented-generation
embeddings
ai-agents
agentic-ai
llm-agents
workflow-orchestration
voice-ai
speech-to-text
text-to-speech
postgresql
redis
docker
docker-compose
kubernetes
terraform
machine-learning
generative-ai
```

---

# 🌐 Project

## GitHub

https://github.com/simhadris17/NEELASTACK

## Local API

```text
http://localhost:8000
```

## API Documentation

```text
http://localhost:8000/docs
```

## Web Application

```text
http://localhost:3000
```

---

# 👨‍💻 Author

## Simhadri Bhukya

**B.Tech — Computer Science Engineering**

AI Engineering • Machine Learning • Full Stack Development • Generative AI

Interested in building practical AI systems that combine:

```text
AI + Software Engineering + Infrastructure
```

---

# 📄 License

This project is licensed under the **MIT License**.

See:

```text
LICENSE
```

for details.

---

# ⭐ Support

If you find NEELASTACK useful:

⭐ Star the repository
🍴 Fork the project
🐛 Open issues
💡 Suggest improvements
🚀 Build your own AI workflows

---

# 🐦 NEELASTACK

> **Local-first AI engineering.
> Your machine. Your models. Your data. Your platform.**

Built to experiment.
Built to learn.
Built to engineer AI systems.
