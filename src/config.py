from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str = 'mafia_db'
    DB_USER: str = 'mafia_user'
    DB_PASSWORD: str = 'mafia_password'
    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 5432

    SECRET_KEY: str = 'secret_key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120


settings = Settings()
