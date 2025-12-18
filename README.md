# 🎼 Maestro – Sistema de Gestão de Requisitos

O **Maestro** é uma solução **Full Stack** desenvolvida para o processo seletivo do **DARM Labs**.  
O projeto tem como objetivo a construção de um ambiente completo para **gestão de Requisitos**, **Histórias de Usuário** e **Regras de Negócio**, seguindo boas práticas de arquitetura, organização de código e versionamento.

---

## 🏗️ Arquitetura do Projeto

A solução foi estruturada com foco em **modularidade**, **manutenibilidade** e **separação de responsabilidades**:

- **Back-End**  
  Desenvolvido em **Python** utilizando o framework **FastAPI**, responsável pela criação de APIs RESTful de alta performance.

- **Front-End**  
  Interface construída com **React (Vite + TypeScript)**, priorizando componentes reutilizáveis e consumo eficiente da API.

- **Banco de Dados**  
  Persistência de dados utilizando **SQLAlchemy (ORM)**.

- **Versionamento**  
  Histórico de commits organizado seguindo boas práticas de **Git**.

---

## 🚀 Funcionalidades Principais

De acordo com os **Requisitos Funcionais (RF)** definidos:

### 🔐 Autenticação
- Login com tratamento de erros
- Autenticação via **JWT**
- Opção **“Lembrar de mim”**

### 🔑 Recuperação de Senha
- Redefinição de senha via **código de verificação de 6 dígitos**

### 📋 Gestão de Itens
- CRUD completo de:
  - Histórias de Usuário
  - Regras de Negócio

### 🔗 Associações
- Associação e desassociação entre:
  - Histórias de Usuário ↔ Regras de Negócio

### 📊 Dashboard
- Interface administrativa com:
  - Sidebar colapsável
  - Navegação hierárquica
  - Toggle de tema (claro/escuro)

---

## 🛠️ Tecnologias e Dependências

### Back-End (Python)
- **FastAPI** – Framework web
- **Pydantic** – Validação de dados
- **SQLAlchemy** – ORM para persistência

### Front-End (React)
- **React Hook Form** – Gerenciamento e validação de formulários
- **Lucide React** – Biblioteca de ícones
- **Axios** – Cliente HTTP
- **React Toastify** – Notificações em tempo real

---

## 💻 Como Executar o Projeto

### ✅ Pré-requisitos
- **Python 3.13+**
- **Node.js 24+**

---

## Clonar o repositório
```
git clone https://github.com/WellingtonLSoares/desafio-maestro-darm-lab.git
cd desafio-maestro-darm-lab
```

### Back-end

```bash
cd backend
python -m venv venv
```

### Ativação do ambiente virtual
Linux / macOS:
```
source venv/bin/activate
```
Windows:
```
venv\Scripts\activate
```
### Instalar dependências
```
pip install -r requirements.txt
```

### Configurar o .env
- Crie um arquivo .env
- Abra o .env.Example e copie e cole o conteúdo de lá
- Preenchas as variáveis de ambiente que estiverem várias(ex: EMAIL) ou altere as variáveis conforme deseja executar seu ambiente.

### Executar o projeto
```
uvicorn app.main:app --reload
```

Acesse:
```
http://127.0.0.1:8000/docs
```

### Front-end
```
cd frontend
npm install
npm run dev
```

### Configurar o .env
- Crie um arquivo .env
- Abra o .env.Example e copie e cole o conteúdo de lá
- Preenchas as variáveis de ambiente que estiverem várias ou altere as variáveis conforme deseja executar seu ambiente(exemplo, API_BASE_URL para a porta que desejar ou link para um ambiente de produção).

Acesse:
```
http://localhost:5173
```
