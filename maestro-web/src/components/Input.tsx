import { forwardRef, useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, type = "text", className = "", ...props }, ref) => {
    
    const [showPassword, setShowPassword] = useState(false);
    
    const isPasswordType = type === 'password';
    const inputType = isPasswordType ? (showPassword ? 'text' : 'password') : type;

    return (
      <div className="input-group">
        <label className="input-label">{label}</label>
        
        <div className="input-wrapper" style={{ position: 'relative' }}>
          <input
            ref={ref}
            type={inputType}
            className={`custom-input ${error ? 'error' : ''} ${className}`}
            {...props}
          />
          
          {/* Renderiza o olhinho automaticamente se for senha */}
          {isPasswordType && (
            <button
              type="button"
              className="toggle-btn"
              onClick={() => setShowPassword(!showPassword)}
              tabIndex={-1}
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          )}
        </div>

        {error && <span className="error-msg">{error}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';