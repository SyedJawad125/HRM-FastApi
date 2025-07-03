# from pydantic_settings  import BaseSettings

# class Settings(BaseSettings):
#     database_url: str = "postgresql://postgres:admin@localhost/hrms_db"
#     secret_key: str = "your-secret-key-here"
#     algorithm: str = "HS256"
#     access_token_expire_minutes: int = 30

#     class Config:
#         env_file = ".env"

# settings = Settings()


from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    # Database configuration
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./hrms.db"
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()