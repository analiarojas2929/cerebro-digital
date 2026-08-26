import React from 'react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { User, Brain, Tag, Clock } from 'lucide-react';
import type { Message } from '@/types';
import ReactMarkdown from 'react-markdown';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  const getCategoryColor = (category?: string) => {
    const colors: Record<string, string> = {
      trabajo: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
      personal: 'bg-green-500/20 text-green-300 border-green-500/30',
      aprendizaje: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
      tecnología: 'bg-red-500/20 text-red-300 border-red-500/30',
      salud: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
      finanzas: 'bg-teal-500/20 text-teal-300 border-teal-500/30',
      entretenimiento: 'bg-pink-500/20 text-pink-300 border-pink-500/30',
      ideas: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
    };
    return colors[category || ''] || 'bg-slate-500/20 text-slate-300 border-slate-500/30';
  };

  return (
    <div className={`flex gap-3 animate-fadeIn ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary-500' : 'bg-slate-700'
        }`}
      >
        {isUser ? <User className="w-5 h-5 text-white" /> : <Brain className="w-5 h-5 text-white" />}
      </div>

      {/* Message Content */}
      <div className={`flex-1 max-w-2xl ${isUser ? 'items-end' : ''}`}>
        <div
          className={`rounded-lg p-4 ${
            isUser
              ? 'bg-primary-600 text-white'
              : 'bg-slate-800 text-slate-100 border border-slate-700'
          }`}
        >
          <div className="prose prose-invert max-w-none">
            {isUser ? (
              <p className="whitespace-pre-wrap">{message.content}</p>
            ) : (
              <ReactMarkdown>{message.content}</ReactMarkdown>
            )}
          </div>

          {/* Metadata */}
          <div className="flex items-center gap-3 mt-3 text-xs opacity-70">
            <div className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {format(new Date(message.timestamp), 'HH:mm', { locale: es })}
            </div>

            {message.category && (
              <div className={`flex items-center gap-1 px-2 py-1 rounded border ${getCategoryColor(message.category)}`}>
                <Tag className="w-3 h-3" />
                {message.category}
              </div>
            )}
          </div>
        </div>

        {/* Related Memories */}
        {message.relatedMemories && message.relatedMemories.length > 0 && (
          <div className="mt-2 space-y-1">
            <p className="text-xs text-slate-500 font-medium">Información relacionada:</p>
            {message.relatedMemories.map((memory, idx) => (
              <div
                key={idx}
                className="text-xs bg-slate-800/50 border border-slate-700 rounded p-2 text-slate-400"
              >
                <div className="flex items-center gap-2 mb-1">
                  {memory.category && (
                    <span className={`px-1.5 py-0.5 rounded text-[10px] ${getCategoryColor(memory.category)}`}>
                      {memory.category}
                    </span>
                  )}
                  <span className="text-slate-500">
                    {(memory.similarity * 100).toFixed(0)}% relevante
                  </span>
                </div>
                <p className="line-clamp-2">{memory.content}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
