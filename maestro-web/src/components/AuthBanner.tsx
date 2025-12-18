import '../css/authbanner.css';

import MaestroBanner from '../assets/maestro-banner.svg';
import MaestroLogoCenter from '../assets/maestro-logo-transparent.svg';

export function AuthBanner() {
  return (
    <div className="auth-banner-section">
      
      {/* 1. Fundo */}
      <img src={MaestroBanner} alt="Fundo Decorativo" className="banner-bg" />

      {/* 2. Textos de Assinatura */}
      <span className="corner-text text-bottom-left">Maestro</span>
      <span className="corner-text text-top-right">Maestro</span>

      {/* 3. Logo Central */}
      <img src={MaestroLogoCenter} alt="Logo Maestro" className="center-logo" />
      
    </div>
  );
}