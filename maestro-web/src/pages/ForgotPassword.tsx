import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';
import { AxiosError } from 'axios';

import '../css/login.css'; 
import MaestroLogo from '../assets/maestro-logo.svg';
import { AuthBanner } from '../components/AuthBanner';
import { Input } from '../components/Input';

type ForgotPasswordInput = {
  email: string;
};

const ForgotPassword = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<ForgotPasswordInput>();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleForgotPassword = async (data: ForgotPasswordInput) => {
    setLoading(true);
    try {
      await authService.forgotPassword(data.email);
      
      toast.success("Código enviado! Verifique seu e-mail.");
      
      navigate('/verificar-codigo', { state: { email: data.email } });

    } catch (err) {
      const error = err as AxiosError<any>;
      const msg = error.response?.data?.detail || "Erro ao solicitar recuperação.";

      toast.error(msg);
    } finally {
      setLoading(false);
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

          <h1 className="page-title">Esqueci minha senha</h1>
          <p style={{ marginBottom: '24px', color: '#6b7280' }}>
            Insira seu e-mail para receber o código de verificação e redefinir sua senha.
          </p>

          <form onSubmit={handleSubmit(handleForgotPassword)}>
            <Input 
              label="Email" 
              placeholder="exemplo@email.com"
              type="email"
              {...register("email", { 
                required: "E-mail é obrigatório",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "E-mail inválido"
                }
              })}
              error={errors.email?.message} 
            />

            <button type="submit" disabled={loading} className="submit-btn" style={{ marginTop: '16px' }}>
              {loading ? 'Enviando...' : 'Enviar'}
            </button>

            <p className="footer-text">
              Lembrou sua senha? <Link to="/">Login</Link>
            </p>
          </form>
        </div>
      </div>

      <AuthBanner />
    </div>
  );
};

export default ForgotPassword;