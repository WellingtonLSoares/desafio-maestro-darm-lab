import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import Dashboard from './pages/Dashboard';
import PrivateRoute from './components/PrivateRoute';
import VerifyCode from './pages/VerifyCode';
import ResetPassword from './pages/ResetPassword';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/cadastro" element={<Register />} />

        <Route path="/esqueceu-senha" element={<ForgotPassword />} />
        <Route path="/verificar-codigo" element={<VerifyCode />} />
        <Route path="/redefinir-senha" element={<ResetPassword />} />

        <Route element={<PrivateRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
        </Route>

      </Routes>
      <ToastContainer autoClose={3000} position="top-right" />
    </Router>
  );
}

export default App;