#/core/security.py
#password hashing + JWT implementation

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext        
from jose import jwt, JWTError                  
from app.core.config import settings

#configue hashing without bcrpyt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

#Standard HMAC SHA256 algorithm JWT
ALGO = "HS256"

def hash_password(plain: str) -> str:
    """Hash a plain text  password for storage"""
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """verify a plaintext password against stored password"""
    return pwd_context.verify(plain,hashed)

def create_token(sub: str) -> str:
    """
    Create a signed JWT.
    sub = subject where we will store user email
    exp = expiration time for token
    """

    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub" : sub,
        "exp" : expires
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)


def decode_token(token: str)-> str:
    """
    decodes and validates a JWT
    Return a subject = email if valid raise if invalid/expired
    """

    data = jwt.decode(token,settings.SECRET_KEY, algorithms=[ALGO])
    return data["sub"]