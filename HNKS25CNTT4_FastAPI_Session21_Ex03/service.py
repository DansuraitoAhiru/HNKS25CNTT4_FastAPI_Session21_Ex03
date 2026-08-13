from model import UserModel
from schema import RegisterRequest
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from auth import hash_password, verify_password, validate_password, create_access_token

def register_user(user: RegisterRequest, db: Session):
    try:
        exist = db.query(UserModel).filter(UserModel.email == user.email).first()
        if exist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "email đã tồn tại")

        if not validate_password(user.password):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Mật khẩu phải có ít nhất 8 ký tự, chữ hoa, chữ thường và số")
        password_hash = hash_password(user.password)
        new_user = UserModel(
            email=user.email,
            password_hash=password_hash,
            full_name=user.full_name,
            role="student",
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def login_user(email: str, password: str, db: Session):
    try:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Email hoặc pass sai")
        if not user.is_active:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tài khoản đã bị khóa")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email hoặc pass sai")
        
        token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role
            },
            expire_minutes=30
        )
        return token
    except HTTPException:
        db.rollback()
        raise
    except ValueError as e:
        db.rollback()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def get_user(id: int, db: Session):
    try:
        user = db.query(UserModel).filter(UserModel.id == id).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Người dùng không tồn tại")
        return user
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))