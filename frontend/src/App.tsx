import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';
import { NeuralNetwork } from './components/NeuralNetwork';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { useAuthStore } from './store/authStore';
import { useChatStore } from './store/chatStore';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  const [view, setView] = useState<'chat' | 'neural'>('chat');
  const [authView, setAuthView] = useState<'login' | 'register'>('login');
  const { isAuthenticated, user, logout } = useAuthStore();
  const clearMessages = useChatStore((state) => state.clearMessages);

  const handleLogout = () => {
    clearMessages();
    queryClient.clear();
    logout();
  };

  if (!isAuthenticated) {
    return authView === 'login' ? (
      <Login onSwitchToRegister={() => setAuthView('register')} />
    ) : (
      <Register onSwitchToLogin={() => setAuthView('login')} />
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex h-screen w-full bg-slate-900 max-md:flex-col">
        <Sidebar />
        <div className="flex flex-1 flex-col max-md:min-h-0 max-md:min-w-0">
          {/* Botones de navegación */}
          <div className="flex gap-3 border-b border-slate-700/50 bg-gradient-to-r from-slate-900 to-slate-800 px-6 py-4 shadow-lg max-md:flex-wrap max-md:gap-2 max-md:px-3 max-md:py-3">
            <button
              onClick={() => setView('chat')}
              className={`rounded-xl px-6 py-3 font-semibold transition-all max-md:px-4 max-md:py-2.5 max-md:text-sm ${
                view === 'chat'
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30 scale-105'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/50'
              }`}
            >
              💬 Chat
            </button>
            <button
              onClick={() => setView('neural')}
              className={`rounded-xl px-6 py-3 font-semibold transition-all max-md:px-4 max-md:py-2.5 max-md:text-sm ${
                view === 'neural'
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30 scale-105'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/50'
              }`}
            >
              🧠 Red Neuronal
            </button>
            <div className="ml-auto flex items-center gap-3 max-md:min-w-0 max-md:gap-2">
              <span className="text-sm text-slate-400 max-md:max-w-[110px] max-md:truncate max-md:text-xs">{user?.full_name || user?.username}</span>
              <button
                onClick={handleLogout}
                className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition-colors hover:border-red-400 hover:text-red-300 max-md:whitespace-nowrap max-md:px-3 max-md:text-xs"
              >
                Cerrar sesión
              </button>
            </div>
          </div>

          {/* Contenido */}
          <div className="flex-1 overflow-hidden">
            {view === 'chat' ? <ChatInterface /> : <NeuralNetwork />}
          </div>
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
