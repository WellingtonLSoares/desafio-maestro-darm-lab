import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  Lightbulb, 
  Code2, 
  TestTube2, 
  ChevronDown, 
  ChevronLeft,
  Sun,
  Moon,
  UserCircle
} from 'lucide-react';
import '../css/dashboard.css';
import MaestroLogo from '../assets/maestro-logo.svg';

const Dashboard = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [activeMenu, setActiveMenu] = useState('requisitos');

  return (
    <div className="dashboard-layout">
      {/* SIDEBAR */}
      <aside className="sidebar" style={{ width: isSidebarOpen ? '260px' : '80px' }}>
        <div className="sidebar-header">
          <div className="logo-container">
            <img src={MaestroLogo} alt="Logo" className="logo-img" />
            {isSidebarOpen && <span className="logo-text">MAESTRO</span>}
          </div>
          
          {/* Botão Toggle */}
          <button className="toggle-sidebar-btn" onClick={() => setSidebarOpen(!isSidebarOpen)}>
            <ChevronLeft 
              size={14} 
              style={{ 
                transform: isSidebarOpen ? 'rotate(0deg)' : 'rotate(180deg)', 
                transition: '0.3s' 
              }} 
            />
          </button>
        </div>

        <nav className="nav-container">
          {/* Dashboard Link */}
          <a href="#" className="nav-item">
            <div className="nav-icon"><LayoutDashboard size={20} /></div>
            {isSidebarOpen && <span>Dashboard</span>}
          </a>

          {/* Requisitos Dropdown */}
          <div>
            <button 
              onClick={() => setActiveMenu(activeMenu === 'requisitos' ? '' : 'requisitos')}
              className={`nav-item ${activeMenu === 'requisitos' ? 'active' : ''}`}
            >
              <div className="nav-icon"><Lightbulb size={20} /></div>
              {isSidebarOpen && (
                <>
                  <span style={{ flex: 1, textAlign: 'left' }}>Requisitos</span>
                  <ChevronDown 
                    size={16} 
                    style={{ 
                      transform: activeMenu === 'requisitos' ? 'rotate(180deg)' : 'rotate(0deg)',
                      transition: '0.2s' 
                    }} 
                  />
                </>
              )}
            </button>
            
            {/* SUBMENU */}
            {isSidebarOpen && activeMenu === 'requisitos' && (
              <div className="submenu">
                <a href="#" className="nav-sub-item">Tarefas</a>
                <a href="#" className="nav-sub-item">Épicos</a>
                <a href="#" className="nav-sub-item">Requisitos Funcionais</a>
                <a href="#" className="nav-sub-item">Requisitos Não Funcionais</a>
                <a href="#" className="nav-sub-item">Regras de Negócio</a>
                <a href="#" className="nav-sub-item">Histórias de Usuário</a>
              </div>
            )}
          </div>

          <a href="#" className="nav-item">
            <div className="nav-icon"><Code2 size={20} /></div>
            {isSidebarOpen && <span>Desenvolvimento</span>}
          </a>

          <a href="#" className="nav-item">
            <div className="nav-icon"><TestTube2 size={20} /></div>
            {isSidebarOpen && <span>Testes de Software</span>}
          </a>
        </nav>
      </aside>

      {/* CONTEÚDO PRINCIPAL */}
      <main className="main-content">
        <header className="top-header">
          <h2 className="text-lg font-semibold text-slate-700">Dashboard</h2>
          
          <div className="header-actions">
            {/* Switch de Tema estilo Pílula/Figma */}
            <div className="theme-switch-container">
              <button className="theme-btn active">
                <Sun size={16} />
              </button>
              <button className="theme-btn">
                <Moon size={16} />
              </button>
            </div>
            
            <button className="user-profile-btn">
              <UserCircle size={32} />
            </button>
          </div>
        </header>

        <section className="construction-container">
          <img 
            src="https://cdni.iconscout.com/illustration/premium/thumb/empty-state-2130362-1800926.png" 
            alt="Página em construção" 
            className="construction-img"
          />
          <h3 className="text-xl font-medium">Página em construção</h3>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;