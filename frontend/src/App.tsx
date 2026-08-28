import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';
import { NeuralNetwork } from './components/NeuralNetwork';

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

  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex h-screen w-full bg-slate-900">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          {/* Botones de navegación */}
          <div className="bg-gradient-to-r from-slate-900 to-slate-800 border-b border-slate-700/50 px-6 py-4 flex gap-3 shadow-lg">
            <button
              onClick={() => setView('chat')}
              className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                view === 'chat'
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30 scale-105'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/50'
              }`}
            >
              💬 Chat
            </button>
            <button
              onClick={() => setView('neural')}
              className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                view === 'neural'
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30 scale-105'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/50'
              }`}
            >
              🧠 Red Neuronal
            </button>
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
