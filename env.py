from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    VECTORDB_HOST: str
    VECTORDB_PORT: int
    JWT_SECRET: str
    TOKEN_EXPIRY: int  # in minutes
    REFRESH_EXPIRY: int  # in minutes
    JWT_ALGORITHM: str
    ENVIRONMENT: str
    OPENAI_BASE_URL: str
    OPENAI_API_KEY: str


env = Env()  # type: ignore
