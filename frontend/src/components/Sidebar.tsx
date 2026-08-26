import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { memoryApi } from '@/services/api';
import { Database, TrendingUp, FolderTree, Loader2 } from 'lucide-react';

const Sidebar: React.FC = () => {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['memory-stats'],
    queryFn: memoryApi.getStats,
    refetchInterval: 30000, // Actualizar cada 30 segundos
  });

  const { data: categories, isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: memoryApi.getCategories,
  });

  const getCategoryIcon = (icon?: string) => icon || '📌';

  return (
    <div className="w-80 bg-gradient-to-b from-slate-900 to-slate-800 border-r border-slate-700/50 flex flex-col shadow-2xl">
      {/* Header */}
      <div className="p-6 border-b border-slate-700/50 bg-slate-900/50">
        <h2 className="text-xl font-bold text-white flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg">
            <Database className="w-5 h-5 text-white" />
          </div>
          <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            Sistema Neural
          </span>
        </h2>
      </div>

      {/* Stats */}
      <div className="p-6 space-y-4">
        {statsLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-6 h-6 text-cyan-400 animate-spin" />
          </div>
        ) : (
          <>
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700/50 shadow-lg hover:shadow-cyan-500/10 transition-shadow">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-300">Conversaciones</span>
                <TrendingUp className="w-5 h-5 text-green-400" />
              </div>
              <p className="text-3xl font-bold text-white mt-2 bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent">
                {stats?.total_conversations || 0}
              </p>
            </div>

            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700/50 shadow-lg hover:shadow-blue-500/10 transition-shadow">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-300">Memorias Guardadas</span>
                <Database className="w-5 h-5 text-blue-400" />
              </div>
              <p className="text-3xl font-bold text-white mt-2 bg-gradient-to-r from-blue-400 to-cyan-500 bg-clip-text text-transparent">
                {stats?.total_memories || 0}
              </p>
            </div>
          </>
        )}
      </div>

      {/* Categories */}
      <div className="flex-1 overflow-y-auto px-6 pb-6">
        <h3 className="text-sm font-bold text-slate-300 mb-4 flex items-center gap-2 uppercase tracking-wider">
          <FolderTree className="w-4 h-4 text-cyan-400" />
          Categorías
        </h3>

        {categoriesLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-6 h-6 text-cyan-400 animate-spin" />
          </div>
        ) : (
          <div className="space-y-3">
            {categories?.map((category) => (
              <div
                key={category.id}
                className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700/50 hover:border-cyan-500/50 transition-all cursor-pointer group hover:shadow-lg hover:shadow-cyan-500/10 hover:scale-[1.02]"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl group-hover:scale-110 transition-transform">{getCategoryIcon(category.icon)}</span>
                    <span className="text-sm font-semibold text-white capitalize">
                      {category.name}
                    </span>
                  </div>
                  <span className="text-xs bg-slate-700/50 px-3 py-1 rounded-full text-slate-300 group-hover:bg-cyan-500/20 group-hover:text-cyan-400 transition-colors font-medium">
                    {category.conversation_count || 0}
                  </span>
                </div>
                {category.keywords && Array.isArray(category.keywords) && category.keywords.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {category.keywords.slice(0, 3).map((keyword, idx) => (
                      <span
                        key={idx}
                        className="text-[10px] bg-slate-700/50 px-2 py-1 rounded-full text-slate-400 group-hover:bg-slate-700 transition-colors"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-6 border-t border-slate-700/50 bg-slate-900/50">
        <p className="text-xs text-slate-400 text-center">
          <span className="font-semibold text-cyan-400">Cerebro Digital</span> v1.0.0
          <br />
          <span className="text-slate-500">Sistema Neural Activo 🧠</span>
        </p>
      </div>
    </div>
  );
};

export default Sidebar;
