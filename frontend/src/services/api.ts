import axios from 'axios';
import type { MessageInput, MessageResponse, MemoryStats, Category } from '@/types';
import { useAuthStore } from '@/store/authStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.DEV ? `http://${window.location.hostname}:8000` : ''
);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && error.config?.headers?.Authorization) {
      localStorage.removeItem('cerebro-auth-storage');
      window.location.reload();
    }
    return Promise.reject(error);
  },
);

export const chatApi = {
  sendMessage: async (input: MessageInput): Promise<MessageResponse> => {
    const { data } = await api.post<MessageResponse>('/chat/message', input);
    return data;
  },

  getHistory: async (sessionId: string, limit = 50) => {
    const { data } = await api.get(`/chat/history/${sessionId}`, {
      params: { limit },
    });
    return data;
  },

  searchMemories: async (query: string, limit = 5, category?: string) => {
    const { data } = await api.post('/chat/search', {
      query,
      limit,
      category,
    });
    return data;
  },

  consolidateSession: async (sessionId: string) => {
    const { data } = await api.post(`/chat/consolidate/${sessionId}`);
    return data;
  },
};

export const memoryApi = {
  getStats: async (): Promise<MemoryStats> => {
    const { data } = await api.get<MemoryStats>('/memory/stats');
    return data;
  },

  getMemories: async (limit = 50, category?: string) => {
    const { data } = await api.get('/memory/memories', {
      params: { limit, category },
    });
    return data;
  },

  getCategories: async (): Promise<Category[]> => {
    const { data } = await api.get<Category[]>('/memory/categories');
    return data;
  },

  getNeuralGraph: async () => {
    const { data } = await api.get('/memory/neural-graph');
    return data;
  },

  deleteMemory: async (memoryId: number) => {
    const { data } = await api.delete(`/memory/memories/${memoryId}`);
    return data;
  },

  addComment: async (memoryId: string, comment: string, user = 'Usuario') => {
    const { data } = await api.post('/memory/comment', {
      memory_id: memoryId,
      comment,
      user
    });
    return data;
  },

  getMemoryThread: async (memoryId: string) => {
    const { data } = await api.get(`/memory/thread/${memoryId}`);
    return data;
  },

  // Nuevas funciones de gestión de memorias
  deleteMemoryById: async (memoryId: string) => {
    const { data} = await api.delete(`/memory/${memoryId}`);
    return data;
  },

  updateImportance: async (memoryId: string, important: boolean) => {
    const { data } = await api.put(`/memory/${memoryId}/importance`, null, {
      params: { important }
    });
    return data;
  },

  setReminder: async (memoryId: string, reminderDate: string, reminderMessage?: string) => {
    const { data } = await api.put(`/memory/${memoryId}/reminder`, null, {
      params: { reminder_date: reminderDate, reminder_message: reminderMessage }
    });
    return data;
  },

  getReminders: async () => {
    const { data } = await api.get('/memory/reminders');
    return data;
  },

  setExpiration: async (memoryId: string, expiresAt: string) => {
    const { data } = await api.put(`/memory/${memoryId}/expiration`, null, {
      params: { expires_at: expiresAt }
    });
    return data;
  },

  getExpired: async () => {
    const { data } = await api.get('/memory/expired');
    return data;
  },

  cleanupExpired: async () => {
    const { data } = await api.post('/memory/cleanup');
    return data;
  },

  getMemoryById: async (memoryId: string) => {
    const { data } = await api.get(`/memory/${memoryId}`);
    return data;
  },
};

export default api;
