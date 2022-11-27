from pydantic import BaseSettings


class Settings(BaseSettings):
    hardware_config: str = "default"

    class Config:
        env_file = ".env"


settings = Settings()
