from pydantic_settings import BaseSettings, SettingsConfigDict

class Env(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str

env = Env() #type: ignore
