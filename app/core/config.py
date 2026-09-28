from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "School Portal"
    environment: str = "development"
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        allowed = {"development", "staging", "production"}
        normalized = value.lower()
        if normalized not in allowed:
            raise ValueError(
                "environment must be one of: development, staging, production"
            )
        return normalized

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret_key(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("jwt_secret_key must be at least 32 characters long")
        return value

    @property
    def parsed_cors_origins(self) -> list[str]:
        origins = [item.strip() for item in self.cors_origins.split(",")]
        return [origin for origin in origins if origin]


settings = Settings()