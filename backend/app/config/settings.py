"""Configuración central de BodegaOS usando pydantic-settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BodegaOS"
    app_version: str = "1.0.0"
    debug: bool = True
    database_url: str = "sqlite:///./bodegaos.db"
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:5500"
    stock_minimo_default: int = 5

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
