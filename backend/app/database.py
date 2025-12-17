from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# check_same_thread=False é necessário apenas para SQLite
engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para injetar o banco nas rotas
def get_db():
  db = SessionLocal()
  
  try:
    yield db
  finally:
    db.close()