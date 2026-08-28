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
    <div className="flex h-full flex-col bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 max-md:min-h-0">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-700/50 bg-gradient-to-r from-slate-900 to-slate-800 p-6 shadow-xl max-md:p-3">
        <div className="flex min-w-0 items-center gap-4 max-md:gap-2">
          <div className="rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 p-3 shadow-lg shadow-cyan-500/20 max-md:shrink-0 max-md:p-2">
            <Brain className="h-6 w-6 text-white max-md:h-5 max-md:w-5" />
          </div>
          <div className="min-w-0">
            <h1 className="truncate text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent max-md:text-lg">
              Cerebro Digital
            </h1>
            <p className="truncate text-sm font-medium text-slate-400 max-md:text-xs">
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
      <div className="flex-1 space-y-4 overflow-y-auto p-6 max-md:min-h-0 max-md:p-3">
        {messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="relative mb-6 max-md:mb-3">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full blur-2xl opacity-20 animate-pulse"></div>
              <div className="relative rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 p-6 max-md:p-4">
                <Brain className="h-16 w-16 text-white max-md:h-12 max-md:w-12" />
              </div>
            </div>
            <h2 className="mb-3 w-full break-words text-3xl font-bold text-white max-md:text-xl">
              ¡Hola! Soy tu Cerebro Digital
            </h2>
            <p className="w-full max-w-md break-words text-lg leading-relaxed text-slate-300 max-md:text-sm">
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
      <div className="border-t border-slate-700/50 bg-gradient-to-r from-slate-900 to-slate-800 p-6 shadow-2xl max-md:p-3">
        <div className="flex gap-3 max-md:items-end max-md:gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu mensaje..."
            className="flex-1 resize-none rounded-xl border border-slate-700/50 bg-slate-800 px-5 py-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 max-md:min-w-0 max-md:px-4 max-md:py-3"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 p-4 text-white shadow-lg transition-all hover:from-cyan-600 hover:to-blue-700 hover:scale-105 hover:shadow-cyan-500/50 disabled:cursor-not-allowed disabled:from-slate-600 disabled:to-slate-700 disabled:scale-100 max-md:shrink-0 max-md:p-3"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
