import bcrypt
import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
# timedelta dùng để cộng/trừ một khoảng thời gian, timezone dùng để xác định múi giờ của thời gian tùy theo nơi ở

SECRET_KEY = "Supercalifragilisticexpialidocious"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def validate_password(password):
    if len(password) < 8:
        raise HTTPException(400, "Mật khẩu phải có ít nhất 8 ký tự")
    if not any(char.isupper() for char in password):
        raise HTTPException(400, "Mật khẩu phải có chữ hoa")
    if not any(char.islower() for char in password):
        raise HTTPException(400, "Mật khẩu phải chữ thường")
    if not any(char.isdigit() for char in password):
        raise HTTPException(400, "Mật khẩu phải có số")
    return password


def create_access_token(data: dict, expire_minutes: int) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload["exp"] = expire
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise Exception("Token không hợp lệ")