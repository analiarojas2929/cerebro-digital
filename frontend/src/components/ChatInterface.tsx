import React, { useState, useRef, useEffect } from 'react';
import { Send, Brain, Trash2 } from 'lucide-react';
import { useChatStore } from '@/store/chatStore';
import { chatApi } from '@/services/api';
import type { Message } from '@/types';
import MessageBubble from './MessageBubble';

const ChatInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { messages, sessionId, isLoading, addMessage, setSessionId, setLoading, clearMessages } =
    useChatStore();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    addMessage(userMessage);
    setInput('');
    setLoading(true);

    try {
      const response = await chatApi.sendMessage({
        message: input,
        session_id: sessionId || undefined,
      });

      if (!sessionId) {
        setSessionId(response.session_id);
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        category: response.category,
        timestamp: new Date(),
        relatedMemories: response.related_memories,
      };

      addMessage(assistantMessage);
    } catch (error) {
      console.error('Error al enviar mensaje:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.',
        timestamp: new Date(),
      };
      
      addMessage(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClear = () => {
    if (confirm('¿Estás seguro de que quieres borrar la conversación?')) {
      clearMessages();
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 border-b border-slate-700/50 p-6 flex items-center justify-between shadow-xl">
        <div className="flex items-center gap-4">
          <div className="bg-gradient-to-br from-cyan-500 to-blue-600 p-3 rounded-xl shadow-lg shadow-cyan-500/20">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              Cerebro Digital
            </h1>
            <p className="text-sm text-slate-400 font-medium">
              {sessionId ? `Sesión: ${sessionId.slice(0, 8)}...` : 'Nueva conversación'}
            </p>
          </div>
        </div>
        
        {messages.length > 0 && (
          <button
            onClick={handleClear}
            className="p-3 hover:bg-slate-700/50 rounded-xl transition-all hover:scale-105 shadow-lg"
            title="Borrar conversación"
          >
            <Trash2 className="w-5 h-5 text-slate-400 hover:text-red-400 transition-colors" />
          </button>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="mb-6 relative">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full blur-2xl opacity-20 animate-pulse"></div>
              <div className="relative bg-gradient-to-br from-cyan-500 to-blue-600 p-6 rounded-2xl">
                <Brain className="w-16 h-16 text-white" />
              </div>
            </div>
            <h2 className="text-3xl font-bold text-white mb-3">
              ¡Hola! Soy tu Cerebro Digital
            </h2>
            <p className="text-slate-300 max-w-md text-lg leading-relaxed">
              Puedo recordar nuestras conversaciones, clasificar información y ayudarte
              a encontrar lo que necesitas. ¿En qué puedo ayudarte hoy?
            </p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="flex gap-2 items-center text-slate-400 p-4">
                <div className="w-3 h-3 bg-cyan-500 rounded-full animate-bounce shadow-lg shadow-cyan-500/50" />
                <div
                  className="w-3 h-3 bg-blue-500 rounded-full animate-bounce shadow-lg shadow-blue-500/50"
                  style={{ animationDelay: '0.1s' }}
                />
                <div
                  className="w-3 h-3 bg-purple-500 rounded-full animate-bounce shadow-lg shadow-purple-500/50"
                  style={{ animationDelay: '0.2s' }}
                />
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 border-t border-slate-700/50 p-6 shadow-2xl">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu mensaje..."
            className="flex-1 bg-slate-800 text-white rounded-xl px-5 py-4 resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500/50 border border-slate-700/50 placeholder-slate-500"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed text-white p-4 rounded-xl transition-all shadow-lg hover:shadow-cyan-500/50 hover:scale-105 disabled:scale-100"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
