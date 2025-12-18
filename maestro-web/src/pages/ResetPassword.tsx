import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { authService } from '../services/auth';
import { AxiosError } from 'axios';

import '../css/login.css'; 
import MaestroLogo from '../assets/maestro-logo.svg';
import { AuthBanner } from '../components/AuthBanner';
import { Input } from '../components/Input';

const ResetPassword = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { email, code } = location.state || {}; 

  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  
  const password = watch("new_password");

  useEffect(() => {
    if (!email || !code) {
      navigate('/esqueceu-senha');
    }
  }, [email, code, navigate]);

  const handleReset = async (data: any) => {
    setLoading(true);
    try {
      await authService.resetPassword({
        email: email,
        reset_code: code,
        new_password: data.new_password
      });
      
      toast.success("Senha alterada com sucesso!");
      navigate('/'); 
      
    } catch (err) {
      const error = err as AxiosError<any>;
      const detail = error.response?.data?.detail;

      toast.error(detail || "Erro ao redefinir. O código pode ter expirado.");
    } finally {
      setLoading(false);
    }
  };

  const handleRequestNewCode = async () => {
    setResending(true);
    try {
      await authService.forgotPassword(email);
      toast.success("Um novo código foi enviado para seu e-mail.");
      
      navigate('/verificar-codigo', { state: { email } });
    } catch (err) {
      toast.error("Erro ao solicitar novo código.");
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="login-container">
      <div className="left-section">
        <div className="form-wrapper">
          
          <div className="logo-header">
            <img src={MaestroLogo} alt="Logo" className="logo-img" />
            <span className="brand-name">Maestro</span>
          </div>

          <h1 className="page-title">Nova senha</h1>
          <p style={{ marginBottom: '24px', color: '#6b7280' }}>
            Quase lá! Digite sua nova senha abaixo.
          </p>

          <form onSubmit={handleSubmit(handleReset)}>
             <Input 
                label="Nova senha" 
                type="password"
                placeholder="••••••••"
                {...register("new_password", { 
                  required: "Senha obrigatória",
                  minLength: { value: 6, message: "Mínimo de 6 caracteres" }
                })}
                error={errors.new_password?.message as string}
             />

             <Input 
                label="Confirmar senha" 
                type="password"
                placeholder="••••••••"
                {...register("confirmPassword", { 
                  required: "Confirme a senha",
                  validate: (val) => val === password || "As senhas não conferem"
                })}
                error={errors.confirmPassword?.message as string}
             />

             <button type="submit" disabled={loading} className="submit-btn" style={{ marginTop: '16px' }}>
                {loading ? 'Salvando...' : 'Redefinir Senha'}
             </button>

             <div style={{ textAlign: 'center', marginTop: '24px', borderTop: '1px solid #f3f4f6', paddingTop: '16px' }}>
               <p className="footer-text" style={{ fontSize: '13px' }}>
                 Seu código expirou ou é inválido?
               </p>
               <button 
                 type="button" 
                 onClick={handleRequestNewCode}
                 disabled={resending}
                 className="forgot-link" 
                 style={{ 
                   background: 'none', 
                   border: 'none', 
                   fontWeight: '600',
                   color: '#2563eb',
                   cursor: 'pointer'
                 }}
               >
                 {resending ? 'Enviando...' : 'Solicitar novo código'}
               </button>
             </div>
          </form>

        </div>
      </div>
      <AuthBanner />
    </div>
  );
};

export default ResetPassword;