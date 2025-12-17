from pydantic import BaseModel

class UserLogin(BaseModel):
  email: str
  password: str
  remember_me: bool = False

class Token(BaseModel):
  access_token: str
  user_id: int
  username: str