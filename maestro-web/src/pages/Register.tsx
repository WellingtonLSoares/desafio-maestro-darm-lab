import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { useNavigate, Link } from 'react-router-dom';
import { authService, type RegisterRequest } from '../services/auth';
import { AxiosError } from 'axios';

import '../css/login.css'; 
import MaestroLogo from '../assets/maestro-logo.svg';
import { AuthBanner } from '../components/AuthBanner';
import { Input } from '../components/Input';

interface RegisterFormInputs extends RegisterRequest {
  confirmPassword: string;
}

const Register = () => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm<RegisterFormInputs>();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const password = watch("password");

  const handleRegister = async (formData: RegisterFormInputs) => {
    setLoading(true);
    try {
      const payload: RegisterRequest = {
        full_name: formData.full_name,
        email: formData.email,
        password: formData.password,
        phone_number: formData.phone_number,
        birth_date: formData.birth_date,
        terms_accepted: formData.terms_accepted
      };

      await authService.register(payload);
      
      toast.success("Conta criada com sucesso!");
      navigate('/'); 
      
    } catch (err) {
      const error = err as AxiosError<any>;
      const msg = error.response?.data?.detail || "Erro ao criar conta. Verifique os dados.";
      
      if (Array.isArray(msg)) {
         toast.error(msg[0].msg || "Erro de validação");
      } else {
         toast.error(msg);
      }
    } finally {
      setLoading(false);
    }
  };

  const formatPhoneNumber = (value: string) => {
    if (!value) return value;
    
    const numbers = value.replace(/\D/g, "");
    const len = numbers.length;

    if (len <= 2) return numbers;
    
    if (len <= 6) return `(${numbers.slice(0, 2)}) ${numbers.slice(2)}`;
    
    if (len <= 10) {
      return `(${numbers.slice(0, 2)}) ${numbers.slice(2, 6)}-${numbers.slice(6)}`;
    }
    
    return `(${numbers.slice(0, 2)}) ${numbers.slice(2, 7)}-${numbers.slice(7, 11)}`;
  };

  return (
    <div className="login-container">
      <div className="left-section">
        <div className="form-wrapper">
          
          <div className="logo-header">
            <img src={MaestroLogo} alt="Logo" className="logo-img" />
            <span className="brand-name">Maestro</span>
          </div>

          <h1 className="page-title">Criar Conta</h1>
          
          {/* Scroll no form caso a tela seja pequena */}
          <form onSubmit={handleSubmit(handleRegister)} className="overflow-y-auto max-h-[80vh] pr-2">
             
             {/* Nome Completo */}
             <Input 
                label="Nome Completo" 
                placeholder="Ex: João da Silva"
                {...register("full_name", { required: "Nome completo é obrigatório" })}
                error={errors.full_name?.message} 
             />

             {/* Email */}
             <Input 
                label="Email" 
                placeholder="exemplo@email.com"
                type="email"
                {...register("email", { 
                  required: "E-mail é obrigatório",
                  pattern: {
                    value: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
                    message: "E-mail inválido"
                  }
                })}
                error={errors.email?.message} 
             />

             {/* Telefone */}
             <Input 
                label="Telefone (Celular)" 
                placeholder="(00) 00000-0000"
                type="tel"
                maxLength={15}
                {...register("phone_number", { 
                   required: "Telefone é obrigatório",
                   onChange: (e) => {
                     e.target.value = formatPhoneNumber(e.target.value);
                   },
                   pattern: {
                     value: /^\(\d{2}\) \d{4,5}-\d{4}$/, 
                     message: "Formato inválido. Use (XX) XXXXX-XXXX"
                   }
                })}
                error={errors.phone_number?.message} 
             />

             {/* Data de Nascimento */}
             <Input 
                label="Data de Nascimento" 
                type="date"
                {...register("birth_date", { required: "Data de nascimento obrigatória" })}
                error={errors.birth_date?.message} 
             />

             {/* Senha */}
             <Input 
                label="Senha" 
                type="password"
                placeholder="••••••••"
                {...register("password", { 
                  required: "Senha é obrigatória",
                  minLength: { value: 6, message: "Mínimo de 6 caracteres" }
                })}
                error={errors.password?.message}
             />

             {/* Confirmar Senha */}
             <Input 
                label="Confirmar Senha" 
                type="password"
                placeholder="••••••••"
                {...register("confirmPassword", { 
                  required: "Confirme sua senha",
                  validate: (val) => val === password || "As senhas não conferem"
                })}
                error={errors.confirmPassword?.message}
             />

             {/* Termos de Aceite */}
             <div className="input-group" style={{ flexDirection: 'row', alignItems: 'flex-start', gap: '10px' }}>
                <input 
                  type="checkbox" 
                  id="terms"
                  style={{ marginTop: '4px' }}
                  {...register("terms_accepted", { required: "Você deve aceitar os termos" })} 
                />
                <div style={{ display: 'flex', flexDirection: 'column' }}>
                  <label htmlFor="terms" className="input-label" style={{ cursor: 'pointer', marginBottom: 0 }}>
                    Li e aceito os <Link to="#" className="forgot-link">Termos de Uso</Link> e <Link to="#" className="forgot-link">Política de Privacidade</Link>.
                  </label>
                  {errors.terms_accepted && <span className="error-msg">{errors.terms_accepted.message}</span>}
                </div>
             </div>
             
             <button type="submit" disabled={loading} className="submit-btn" style={{ marginTop: '16px' }}>
                {loading ? 'Criando...' : 'Cadastrar'}
             </button>

             <p className="footer-text">
                Já tem uma conta? <Link to="/">Entrar</Link>
             </p>
          </form>

        </div>
      </div>
      <AuthBanner />
    </div>
  );
};

export default Register;