import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Crear instancia de axios con configuración base
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token a todas las requests
apiClient.interceptors.request.use(
  (config) => {
    // Obtener token del localStorage (donde Zustand lo guarda con persist)
    const authStorage = localStorage.getItem('cerebro-auth-storage');
    if (authStorage) {
      try {
        const { state } = JSON.parse(authStorage);
        if (state?.token) {
          config.headers.Authorization = `Bearer ${state.token}`;
        }
      } catch (error) {
        console.error('Error parsing auth token:', error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de autenticación
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token inválido o expirado - limpiar auth
      localStorage.removeItem('cerebro-auth-storage');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

export default apiClient;
