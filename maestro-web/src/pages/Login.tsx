import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { AlertTriangle } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { authService, type LoginResponse } from '../services/auth';
import { AxiosError } from 'axios';

// Estilos
import '../css/login.css';

// Assets e Componentes
import MaestroLogo from '../assets/maestro-logo.svg';
import { AuthBanner } from '../components/AuthBanner';
import { Input } from '../components/Input';

type LoginFormInputs = {
  email: string;
  password: string;
  rememberMe: boolean;
};

const Login = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormInputs>();
  const [loading, setLoading] = useState(false);
    
  const [isLocked, setIsLocked] = useState(false);
  const [lockoutTimer, setLockoutTimer] = useState(0);

  const navigate = useNavigate();

  useEffect(() => {
    let interval: number;
    if (isLocked && lockoutTimer > 0) {
      interval = setInterval(() => setLockoutTimer((prev) => prev - 1), 1000);
    } else if (lockoutTimer === 0) {
      setIsLocked(false);
    }
    return () => clearInterval(interval);
  }, [isLocked, lockoutTimer]);

  const handleLogin = async (data: LoginFormInputs) => {
    setLoading(true);
    try {
      const response: LoginResponse = await authService.login(data.email, data.password, data.rememberMe);

      localStorage.setItem('@Maestro:token', response.access_token);
      localStorage.setItem('@Maestro:user', JSON.stringify({ id: response.user_id, username: response.username }));

      toast.success(`Bem-vindo, ${response.username}!`);

      navigate('/dashboard'); 
    } catch (error: any) {
      const status = error.response?.status;
      const detail = error.response?.data?.detail || "Erro ao realizar login";
      if (status === 403) {
        setIsLocked(true);
        setLockoutTimer(30);
        toast.error("Conta bloqueada temporariamente.");
      } else {
        toast.error(detail);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      
      {/* esquerda: Formulário */}
      <div className="left-section">
        <div className="form-wrapper">
          
          <div className="logo-header">
            <img src={MaestroLogo} alt="Logo" className="logo-img" />
            <span className="brand-name">Maestro</span>
          </div>

          <h1 className="page-title">Entrar</h1>
          
          {isLocked && (
            <div className="alert-box">
              <AlertTriangle size={20} color="#ea580c" style={{ flexShrink: 0 }} />
              <span>Aguarde <strong>{lockoutTimer}s</strong>.</span>
            </div>
          )}
          
          <form onSubmit={handleSubmit(handleLogin)}>
             <Input 
                label="Email" 
                placeholder="exemplo@email.com"
                disabled={isLocked}
                {...register("email", { required: "E-mail obrigatório" })}
                error={errors.email?.message} 
             />
             <Input 
                label="Senha" 
                type="password"
                placeholder="••••••••"
                disabled={isLocked}
                {...register("password", { required: "Senha obrigatória" })}
                error={errors.password?.message}
             />
             
             <div className="actions-row">
                <label className="checkbox-container">
                  <input type="checkbox" {...register("rememberMe")} /> 
                  Lembrar de mim
                </label>

                <Link to="/esqueceu-senha" className="forgot-link">Esqueceu a senha?</Link>
             </div>

             <button type="submit" disabled={loading || isLocked} className="submit-btn">
                {loading ? 'Entrando...' : 'Entrar'}
             </button>

             <p className="footer-text">
                Você não tem conta?
                <Link to="/cadastro">Cadastrar</Link>
             </p>
          </form>

        </div>
      </div>

      {/* direita: O Banner Componentizado */}
      <AuthBanner />

    </div>
  );
};

export default Login;