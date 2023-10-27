import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    API: str = os.getenv("API")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT"))
    MYSQL_DB: str = os.getenv("MYSQL_DB")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    APPLICATION_PORT: int = int(os.getenv("APPLICATION_PORT"))
    LOGSTASH_HOST: str = os.getenv("LOGSTASH_HOST")
    LOGSTASH_PORT: int = int(os.getenv("LOGSTASH_PORT"))

    def __init__(self):
        if not all([self.PROJECT_NAME, self.API, self.MYSQL_HOST, self.MYSQL_PORT, self.MYSQL_DB,
                    self.MYSQL_USER, self.MYSQL_PASSWORD, self.APPLICATION_PORT, self.LOGSTASH_HOST, self.LOGSTASH_PORT]):
            raise ValueError("Some environment variables are not set. Please check your .env file.")

settings = Settings()
