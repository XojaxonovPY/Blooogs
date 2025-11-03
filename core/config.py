import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# @dataclass
# class RedisConfig:
#     REDIS_URL: str = os.getenv("REDIS_URL")


@dataclass
class EmailConfig:
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587


@dataclass
class BotConfig:
    pass


@dataclass
class Configuration:
    db = DatabaseConfig()
    # redis = RedisConfig()
    bot = BotConfig()
    email = EmailConfig()


conf = Configuration()
