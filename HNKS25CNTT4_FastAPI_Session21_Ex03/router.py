from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from schema import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, UserResponse
from service import register_user, login_user, get_user
from auth import decode_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

security = HTTPBearer() # dùng để lấy và kiểm tra token mà client gửi lên API

@router.post("/register", response_model=RegisterResponse)
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(user, db)
    return user


@router.post("/login", response_model=LoginResponse)
def login(user: LoginRequest,db: Session = Depends(get_db)):
    try:
        token = login_user(user.email, user.password, db)
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 1800
        }
    except ValueError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))


@router.get("/me", response_model=UserResponse)
def get_me(header: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):  # HTTPAuthorizationCredentials dùng để lấy thông tin từ Header Authorization khi client gửi JWT lên API
    token = header.credentials   # thuộc tính chứa phần token trong đối tượng HTTPAuthorizationCredentials
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token không hợp lệ")

        user = get_user(user_id, db)
        return user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token không hợp lệ hoặc đã hết hạn")