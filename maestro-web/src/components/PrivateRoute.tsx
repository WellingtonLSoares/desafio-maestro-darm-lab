import { Navigate, Outlet } from 'react-router-dom';

const PrivateRoute = () => {
  const token = localStorage.getItem('@Maestro:token');

  return token ? <Outlet /> : <Navigate to="/" replace />;
};

export default PrivateRoute;

