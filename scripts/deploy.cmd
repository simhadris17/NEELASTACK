@echo off
setlocal
if "%1"=="rollback" goto rollback
if "%KUBE_NAMESPACE%"=="" set KUBE_NAMESPACE=neelastack
if "%API_IMAGE%"=="" set API_IMAGE=neelastack/api
if "%WORKER_IMAGE%"=="" set WORKER_IMAGE=neelastack/worker
kubectl apply -f infrastructure\kubernetes\namespace.yaml || exit /b 1
for %%f in (infrastructure\kubernetes\*.yaml) do (
  if /I not "%%~nxf"=="secret.yaml" if /I not "%%~nxf"=="namespace.yaml" (
    kubectl apply -f "%%f" -n %KUBE_NAMESPACE% || exit /b 1
  )
)
kubectl -n %KUBE_NAMESPACE% get secret neelastack-secret >nul || (
  echo Missing neelastack-secret. Provision it with your secret manager before deploying.
  exit /b 1
)
if not "%IMAGE_TAG%"=="" (
  kubectl -n %KUBE_NAMESPACE% set image deployment/neelastack-api api=%API_IMAGE%:%IMAGE_TAG% || exit /b 1
  kubectl -n %KUBE_NAMESPACE% set image deployment/neelastack-worker worker=%WORKER_IMAGE%:%IMAGE_TAG% || exit /b 1
)
kubectl -n %KUBE_NAMESPACE% rollout status deployment/neelastack-api --timeout=5m || (
  echo Rollout failed. Run scripts\deploy.cmd rollback to restore the previous revision.
  exit /b 1
)
kubectl -n %KUBE_NAMESPACE% rollout status deployment/neelastack-worker --timeout=5m || exit /b 1
exit /b 0

:rollback
if "%KUBE_NAMESPACE%"=="" set KUBE_NAMESPACE=neelastack
kubectl -n %KUBE_NAMESPACE% rollout undo deployment/neelastack-api || exit /b 1
kubectl -n %KUBE_NAMESPACE% rollout undo deployment/neelastack-worker || exit /b 1
kubectl -n %KUBE_NAMESPACE% rollout status deployment/neelastack-api --timeout=5m
