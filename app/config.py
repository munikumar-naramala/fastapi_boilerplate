from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    API: str = "/api"
    SQLALCHEMY_DATABASE_URI: str
    USER_NAME: str
    PASSWORD: str
    APPLICATION_PORT: int
    LOGSTASH_HOST: str
    LOGSTASH_PORT: int

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
