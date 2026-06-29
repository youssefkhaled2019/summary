
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from core.config import settings
from fastapi import HTTPException


# SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "" #settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(  to_encode, settings.SECRET_KEY,    algorithm=ALGORITHM   )



def decode_token(token: str):#
    try:
        payload = jwt.decode( token, settings.SECRET_KEY, algorithms=[ALGORITHM] )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail=" JWTError " )