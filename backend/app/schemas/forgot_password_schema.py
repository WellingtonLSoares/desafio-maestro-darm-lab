from pydantic import BaseModel

# 1. Solicitar o código
class ForgotPasswordRequest(BaseModel):
  email: str

class ResetPasswordRequest(BaseModel):
  email: str
  reset_code: str
  new_password: str
