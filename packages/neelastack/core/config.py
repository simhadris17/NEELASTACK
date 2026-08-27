from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NEELASTACK"
    environment: str = "development"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./neelastack.db"
    redis_url: str = "redis://localhost:6379/0"
    model_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_timeout_seconds: float = 600
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    groq_api_key: str | None = None
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "llama-3.1-8b-instant"
    provider_fallbacks: str = "ollama,openai,groq"
    provider_timeout_seconds: float = 120
    provider_max_retries: int = 2
    jwt_expire_minutes: int = 720
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60
    rate_limit_use_redis: bool = True
    cors_origins: str = (
        "http://localhost:3000,http://localhost:5173,http://localhost:5174,"
        "http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:5174"
    )
    max_request_body_bytes: int = 10 * 1024 * 1024
    security_headers_enabled: bool = True
    hsts_enabled: bool = False
    trust_proxy_headers: bool = False
    allowed_hosts: str = "*"
    stt_provider: str = "local"
    tts_provider: str = "local"
    voice_fallbacks: str = "local,openai,groq"
    voice_max_upload_bytes: int = 25 * 1024 * 1024
    whisper_command: str | None = None
    whisper_model: str = "base"
    openai_stt_model: str = "whisper-1"
    openai_tts_model: str = "gpt-4o-mini-tts"
    openai_tts_voice: str = "alloy"
    groq_stt_model: str = "whisper-large-v3-turbo"
    worker_poll_seconds: float = 1.0
    worker_concurrency: int = 1
    worker_job_timeout_seconds: int = 600
    worker_max_attempts: int = 3

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def provider_fallback_list(self) -> list[str]:
        return [name.strip().lower() for name in self.provider_fallbacks.split(",") if name.strip()]

    @property
    def allowed_host_list(self) -> list[str]:
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @model_validator(mode="after")
    def validate_production_security(self):
        if self.environment.lower() in {"production", "prod"}:
            if self.secret_key in {"change-me", "change-this-in-local-development"} or len(self.secret_key) < 32:
                raise ValueError("SECRET_KEY must be a random value of at least 32 characters in production")
            if "*" in self.cors_origin_list:
                raise ValueError("CORS_ORIGINS cannot be wildcard in production")
        return self

settings = Settings()
