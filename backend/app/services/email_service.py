import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL = os.getenv("EMAIL")
PASSWORD_APP_GMAIL = os.getenv("PASSWORD_APP_GMAIL")

def send_email(to_email: str, subject: str, html_body: str):
  """
  Envia o e-mail real usando o servidor SMTP do Gmail.
  """
  if not EMAIL or not PASSWORD_APP_GMAIL:
    print("⚠️ Configurações de e-mail (EMAIL/PASSWORD_APP_GMAIL) não encontradas. Apenas simulando.")
    return False

  try:
    msg = MIMEMultipart()
    msg['From'] = f"DARM Labs <{EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html_body, 'html'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, PASSWORD_APP_GMAIL)
    text = msg.as_string()
    server.sendmail(EMAIL, to_email, text)
    server.quit()
    
    print(f"✅ E-mail enviado para {to_email}")
    return True

  except Exception as e:
    print(f"❌ Erro ao enviar e-mail: {str(e)}")
    return False
  