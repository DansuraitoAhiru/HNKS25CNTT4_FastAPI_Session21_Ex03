from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "mysql+pymysql://root:WXvs6026%40@localhost:3306/auth_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()