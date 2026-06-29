


# --------------core/config.py --------------
from pydantic_settings import BaseSettings
class Settings(BaseSettings):

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM:str
    class Config:
        env_file = ".env"


settings = Settings()
# ------------------------------------------
# from core.config import settings
# DATABASE_URL = settings.DATABASE_URL 
# ------------------------------------------

# 
# main.py
# .env

# -----------.env -----------
DATABASE_URL = "sqlite:///./test.db"
SECRET_KEY = "change_this_later"
ALGORITHM = "HS256"