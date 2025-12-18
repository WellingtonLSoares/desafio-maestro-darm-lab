import { useState, useRef, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { authService } from '../services/auth';

import '../css/login.css'; 
import MaestroLogo from '../assets/maestro-logo.svg';
import { AuthBanner } from '../components/AuthBanner';

const VerifyCode = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const email = location.state?.email; 

  const CODE_LENGTH = 6;

  const [code, setCode] = useState<string[]>(Array(CODE_LENGTH).fill(""));
  const inputsRef = useRef<(HTMLInputElement | null)[]>([]);
  const [timer, setTimer] = useState(60);

  useEffect(() => {
    if (!email) {
      toast.error("Fluxo inválido.");
      navigate('/esqueceu-senha');
    }
  }, [email, navigate]);

  useEffect(() => {
    if (timer > 0) {
      const interval = setInterval(() => setTimer((t) => t - 1), 1000);
      return () => clearInterval(interval);
    }
  }, [timer]);

  const handleChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return; 

    const newCode = [...code];
    newCode[index] = value.slice(-1); 
    setCode(newCode);

    if (value && index < CODE_LENGTH - 1) {
      inputsRef.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pasteData = e.clipboardData.getData("text").slice(0, CODE_LENGTH).split("");
    if (pasteData.every(char => /^\d$/.test(char))) {
      const newCode = [...code];
      pasteData.forEach((char, i) => { if (i < CODE_LENGTH) newCode[i] = char; });
      setCode(newCode);
      const nextIndex = Math.min(pasteData.length, CODE_LENGTH - 1);
      inputsRef.current[nextIndex]?.focus();
    }
  };

  const handleNextStep = () => {
    const fullCode = code.join("");
    if (fullCode.length < CODE_LENGTH) {
      toast.warning("Digite o código completo.");
      return;
    }
    
    navigate('/redefinir-senha', { state: { email, code: fullCode } });
  };

  const handleResend = async () => {
    if (timer > 0) return;
    try {
      await authService.forgotPassword(email);
      setTimer(60);
      toast.success("Novo código enviado!");
    } catch {
      toast.error("Erro ao reenviar código.");
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

          <h1 className="page-title">Código de verificação</h1>
          <p style={{ marginBottom: '24px', color: '#6b7280' }}>
            Digite o código de 6 dígitos enviado para <strong>{email}</strong>
          </p>

          <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', justifyContent: 'center' }}>
            {code.map((digit, index) => (
              <input
                key={index}
                ref={(el) => { inputsRef.current[index] = el }}
                type="text"
                inputMode="numeric"
                maxLength={1}
                value={digit}
                onChange={(e) => handleChange(index, e.target.value)}
                onKeyDown={(e) => handleKeyDown(index, e)}
                onPaste={index === 0 ? handlePaste : undefined}
                className="custom-input"
                style={{ 
                  width: '45px',
                  height: '50px', 
                  textAlign: 'center', 
                  fontSize: '20px', 
                  padding: '0',
                  borderColor: digit ? '#2563eb' : '#e5e7eb' 
                }}
              />
            ))}
          </div>

          <div style={{ marginBottom: '24px', fontSize: '14px', textAlign: 'center' }}>
            {timer > 0 ? (
              <span className="text-gray-500">Reenviar em {timer}s</span>
            ) : (
              <button onClick={handleResend} className="forgot-link" style={{background:'none', border:'none', padding:0}}>
                Reenviar código
              </button>
            )}
          </div>

          <button onClick={handleNextStep} className="submit-btn">
            Verificar Código
          </button>

        </div>
      </div>
      <AuthBanner />
    </div>
  );
};

export default VerifyCode;