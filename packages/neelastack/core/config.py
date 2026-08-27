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
    jwt_expire_minutes: int = 720

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
