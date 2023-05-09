from pydantic import BaseSettings


class Settings(BaseSettings):
    access_token: str
    port: int = 9872

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "ynab_exporter_"
