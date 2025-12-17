# Arquivo: app/utils/email_templates.py

def get_reset_password_template(code: str) -> str:
    """
    Retorna o HTML do e-mail de recuperação de senha.
    """
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #2c3e50; text-align: center;">Recuperação de Senha</h2>
            <p>Olá,</p>
            <p>Recebemos uma solicitação para redefinir sua senha. Seu código de verificação é:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <h1 style="color: #2980b9; letter-spacing: 5px; font-size: 32px; margin: 0;">{code}</h1>
            </div>
            
            <p>Este código expira em <strong>10 minutos</strong>.</p>
            <p style="font-size: 12px; color: #777;">Se você não solicitou isso, por favor ignore este e-mail.</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="text-align: center; font-size: 12px; color: #aaa;">Maestro</p>
        </div>
      </body>
    </html>
    """