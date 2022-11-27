from pydantic import BaseSettings


class Settings(BaseSettings):
    hardware_config: str = "default"
    sampling_rate: float = 0.5

    class Config:
        env_file = ".env"


settings = Settings()
