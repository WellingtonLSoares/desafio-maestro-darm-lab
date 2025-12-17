from sqlalchemy import Column, Integer, String, Date, DateTime
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  full_name = Column(String, nullable=False)
  username = Column(String, unique=True, index=True, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  phone_number = Column(String, nullable=False)
  birth_date = Column(Date, nullable=False)
  hashed_password = Column(String, nullable=False)

  term_agreement = relationship("UserTerm", back_populates="user", uselist=False)

  failed_login_attempts = Column(Integer, default=0)
  last_failed_login = Column(DateTime(timezone=True), nullable=True)
