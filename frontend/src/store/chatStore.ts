import { create } from 'zustand';
import type { Message } from '@/types';

interface ChatState {
  messages: Message[];
  sessionId: string | null;
  isLoading: boolean;
  currentCategory: string | null;
  
  addMessage: (message: Message) => void;
  setSessionId: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setCurrentCategory: (category: string | null) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  sessionId: null,
  isLoading: false,
  currentCategory: null,

  addMessage: (message: Message) =>
    set((state: ChatState) => ({
      messages: [...state.messages, message],
    })),

  setSessionId: (id: string) => set({ sessionId: id }),

  setLoading: (loading: boolean) => set({ isLoading: loading }),

  setCurrentCategory: (category: string | null) => set({ currentCategory: category }),

  clearMessages: () => set({ messages: [], sessionId: null }),
}));
