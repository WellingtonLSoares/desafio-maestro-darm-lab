import api from './api';

export interface LoginResponse {
  access_token: string;
  user_id: number;
  username: string;
}

export interface RegisterResponse {
  id: number;
  username: string;
  email: string;
  full_name: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  phone_number: string;
  birth_date: string
  terms_accepted: boolean;
}

export interface ResetPasswordRequest {
  email: string;
  reset_code: string;
  new_password: string;
}

export const authService = {
  login: async (email: string, password: string, remember_me: boolean): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/autenticacao/login', {
      email,
      password,
      remember_me
    });

    return response.data;
  },

  register: async (data: RegisterRequest) => {
    const response = await api.post<RegisterResponse>('/autenticacao/cadastro', data);

    return response.data;
  },

  forgotPassword: async (email: string) => {
    const response = await api.post('/autenticacao/esqueceu-senha/solicitar', { email });

    return response.data;
  },

  resetPassword: async (data: ResetPasswordRequest) => {
    const response = await api.post('/autenticacao/esqueceu-senha/redefinir', data);
    return response.data;
  }
};