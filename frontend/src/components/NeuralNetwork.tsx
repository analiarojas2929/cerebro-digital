import { useCallback, useEffect, useRef, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { memoryApi } from '@/services/api';
import { X, ZoomIn, ZoomOut, Maximize2, Info } from 'lucide-react';

interface Node {
  id: string;
  name: string;
  color: string;
  icon?: string;
  count?: number;
  val: number;
  layer?: number;
  full_text?: string;
  date?: string;
  time?: string;
  category?: string;
  subcategory?: string;
  type?: string;
}

interface Link {
  source: string;
  target: string;
  value: number;
}

interface GraphData {
  nodes: Node[];
  links: Link[];
}

interface MemoryDetail {
  id?: string;
  name: string;
  full_text?: string;
  date?: string;
  time?: string;
  category?: string;
  subcategory?: string;
  color: string;
  layer?: number;
  user?: string;
  type?: string;
  important?: boolean;
  has_reminder?: boolean;
  archived?: boolean;
}

export function NeuralNetwork() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);
  const [selectedNode, setSelectedNode] = useState<MemoryDetail | null>(null);
  const [comment, setComment] = useState('');
  const [savingComment, setSavingComment] = useState(false);
  const [showReminderForm, setShowReminderForm] = useState(false);
  const [reminderDate, setReminderDate] = useState('');
  const [reminderMessage, setReminderMessage] = useState('');
  const [showExpirationForm, setShowExpirationForm] = useState(false);
  const [expirationDate, setExpirationDate] = useState('');
  const [showStats, setShowStats] = useState(() => (
    typeof window === 'undefined' || !window.matchMedia('(max-width: 767px)').matches
  ));
  const [viewport, setViewport] = useState({ width: 800, height: 600 });
  const sizeRef = useRef(viewport);
  const headerRef = useRef<HTMLDivElement>(null);
  const resizeObserverRef = useRef<ResizeObserver | null>(null);
  const graphRef = useRef<any>();

  const handleSaveComment = async (nodeId: string) => {
    if (!comment.trim()) return;
    
    setSavingComment(true);
    try {
      await memoryApi.addComment(nodeId, comment);
      setComment('');
      // Recargar el grafo para mostrar el nuevo comentario
      await loadNeuralNetwork();
      alert('✅ Comentario guardado exitosamente');
    } catch (error) {
      console.error('Error guardando comentario:', error);
      alert('❌ Error al guardar comentario');
    } finally {
      setSavingComment(false);
    }
  };

  const handleDeleteMemory = async (memoryId: string) => {
    if (!confirm('¿Estás seguro de que quieres eliminar esta memoria? Esta acción no se puede deshacer.')) {
      return;
    }
    
    try {
      await memoryApi.deleteMemoryById(memoryId);
      setSelectedNode(null);
      await loadNeuralNetwork();
      alert('✅ Memoria eliminada exitosamente');
    } catch (error) {
      console.error('Error eliminando memoria:', error);
      alert('❌ Error al eliminar memoria');
    }
  };

  const handleToggleImportance = async (memoryId: string, currentlyImportant: boolean) => {
    try {
      await memoryApi.updateImportance(memoryId, !currentlyImportant);
      await loadNeuralNetwork();
      alert(`✅ Memoria marcada como ${!currentlyImportant ? 'importante' : 'normal'}`);
    } catch (error) {
      console.error('Error actualizando importancia:', error);
      alert('❌ Error al actualizar importancia');
    }
  };

  const handleSetReminder = async (memoryId: string) => {
    if (!reminderDate) {
      alert('Por favor selecciona una fecha');
      return;
    }
    
    try {
      await memoryApi.setReminder(memoryId, reminderDate, reminderMessage || undefined);
      setShowReminderForm(false);
      setReminderDate('');
      setReminderMessage('');
      await loadNeuralNetwork();
      alert('✅ Recordatorio establecido exitosamente');
    } catch (error) {
      console.error('Error estableciendo recordatorio:', error);
      alert('❌ Error al establecer recordatorio');
    }
  };

  const handleSetExpiration = async (memoryId: string) => {
    if (!expirationDate) {
      alert('Por favor selecciona una fecha');
      return;
    }
    
    try {
      await memoryApi.setExpiration(memoryId, expirationDate);
      setShowExpirationForm(false);
      setExpirationDate('');
      await loadNeuralNetwork();
      alert('✅ Fecha de caducidad establecida exitosamente');
    } catch (error) {
      console.error('Error estableciendo caducidad:', error);
      alert('❌ Error al establecer caducidad');
    }
  };

  // Mide el contenedor real cuando se monta (evita depender de refs que no existen durante la carga)
  const containerCallbackRef = useCallback((node: HTMLDivElement | null) => {
    resizeObserverRef.current?.disconnect();
    resizeObserverRef.current = null;
    if (!node) return;
    const updateSize = () => {
      const containerRect = node.getBoundingClientRect();
      const headerHeight = node.firstElementChild?.getBoundingClientRect().height ?? 0;
      const width = Math.round(containerRect.width);
      const height = Math.round(containerRect.height - headerHeight);
      if (width > 0 && height > 0) {
        const next = { width, height };
        sizeRef.current = next;
        setViewport(next);
        loadNeuralNetwork();
      }
    };
    updateSize();
    const observer = new ResizeObserver(updateSize);
    observer.observe(node);
    resizeObserverRef.current = observer;
  }, []);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(max-width: 767px)');
    const handleMediaChange = (event: MediaQueryListEvent) => setShowStats(!event.matches);
    mediaQuery.addEventListener('change', handleMediaChange);
    loadNeuralNetwork();
    const interval = setInterval(loadNeuralNetwork, 5000);
    return () => {
      clearInterval(interval);
      resizeObserverRef.current?.disconnect();
      mediaQuery.removeEventListener('change', handleMediaChange);
    };
  }, []);

  const loadNeuralNetwork = async () => {
    try {
      const data = await memoryApi.getNeuralGraph();
      
      // ORGANIZAR NODOS EN CAPAS TIPO RED NEURONAL CLÁSICA
      const nodesByLayer: { [key: number]: any[] } = {};
      data.nodes.forEach((node: any) => {
        const layer = node.layer || 0;
        if (!nodesByLayer[layer]) nodesByLayer[layer] = [];
        nodesByLayer[layer].push(node);
      });
      
      // Dimensiones reales del área del grafo (medidas con ResizeObserver)
      const { width, height } = sizeRef.current;
      const layers = Object.keys(nodesByLayer).map(Number).sort((a, b) => a - b);
      const maxLayer = Math.max(...layers);
      
      // Posicionar nodos en capas
      data.nodes.forEach((node: any) => {
        const layer = node.layer || 0;
        const layerNodes = nodesByLayer[layer];
        const indexInLayer = layerNodes.indexOf(node);
        const totalInLayer = layerNodes.length;
        
        // DISTRIBUCIÓN HORIZONTAL (de izquierda a derecha)
        // Posición X: por capas con más espacio
        const layerSpacing = width / (maxLayer + 2);
        node.fx = (layer + 1) * layerSpacing;
        
        // Posición Y: distribuir verticalmente dentro de la capa
        const verticalSpacing = height / (totalInLayer + 1);
        node.fy = (indexInLayer + 1) * verticalSpacing;
        
        // Establecer posiciones iniciales
        node.x = node.fx;
        node.y = node.fy;
        
        // Colores por tipo y capa
        if (node.type === 'comment') {
          node.color = '#a855f7';  // Morado para comentarios
          node.val = 8;
        } else if (layer === 0) {
          node.color = '#00bcd4';  // Cian para categorías (entrada)
          node.val = 15;
        } else if (layer === 1) {
          node.color = '#2196f3';  // Azul para subcategorías
          node.val = 12;
        } else {
          // Verde/colores originales para memorias
          node.color = node.color || '#4caf50';
          node.val = node.val || 10;
        }
      });
      
      console.log('Nodos organizados:', data.nodes.length, 'Ejemplo:', data.nodes[0]);
      
      setGraphData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error cargando red neuronal:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full bg-gradient-to-br from-slate-950 via-slate-900 to-black">
        <div className="text-center">
          <div className="relative mb-6">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full blur-2xl opacity-30 animate-pulse"></div>
            <div className="relative animate-spin rounded-full h-16 w-16 border-4 border-slate-700 border-t-cyan-500 mx-auto"></div>
          </div>
          <p className="text-slate-300 text-lg font-semibold mb-2">Construyendo red neuronal...</p>
          <p className="text-slate-500 text-sm">Organizando memorias y conexiones</p>
        </div>
      </div>
    );
  }

  if (!graphData || !graphData.nodes || !graphData.links) {
    return (
      <div className="flex items-center justify-center h-full bg-gradient-to-br from-slate-950 via-slate-900 to-black">
        <div className="text-center bg-slate-800/50 border border-slate-700/50 rounded-2xl p-8 backdrop-blur-sm">
          <div className="text-6xl mb-4">🧠</div>
          <p className="text-slate-300 text-lg font-semibold mb-2">No hay datos disponibles</p>
          <p className="text-slate-500 text-sm">Comienza una conversación para crear memorias</p>
        </div>
      </div>
    );
  }

  const handleZoomIn = () => {
    if (graphRef.current) {
      graphRef.current.zoom(graphRef.current.zoom() * 1.3, 400);
    }
  };

  const handleZoomOut = () => {
    if (graphRef.current) {
      graphRef.current.zoom(graphRef.current.zoom() / 1.3, 400);
    }
  };

  const handleCenterGraph = () => {
    if (graphRef.current) {
      graphRef.current.zoomToFit(400, 50);
    }
  };

  const getNodeStats = () => {
    const categories = graphData.nodes.filter(n => n.layer === 0).length;
    const subcategories = graphData.nodes.filter(n => n.layer === 1).length;
    const memories = graphData.nodes.filter(n => n.layer === 2 || (n.layer! > 1 && n.type !== 'comment')).length;
    const comments = graphData.nodes.filter(n => n.type === 'comment').length;
    return { categories, subcategories, memories, comments };
  };

  const stats = getNodeStats();

  return (
    <div ref={containerCallbackRef} className="relative flex h-full min-h-0 w-full flex-col overflow-hidden rounded-lg bg-gradient-to-br from-slate-950 via-slate-900 to-black">
      {/* Header con gradiente mejorado */}
      <div ref={headerRef} className="border-b border-cyan-500/20 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 px-6 py-4 shadow-xl backdrop-blur-sm max-md:px-4 max-md:py-3">
        <div className="flex items-center justify-between max-md:items-start max-md:gap-3">
          <div className="max-md:min-w-0">
            <h2 className="flex items-center gap-3 text-2xl font-bold text-transparent bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text max-md:gap-2 max-md:text-lg">
              🧠 Red Neuronal de Memoria
            </h2>
            <p className="mt-1.5 text-xs font-medium text-slate-400 max-md:hidden">
              Visualización cronológica: Categorías → Subcategorías → Memorias → Comentarios
            </p>
          </div>
          
          {/* Controles */}
          <div className="flex items-center gap-2 max-md:shrink-0 max-md:gap-1">
            <button
              onClick={() => setShowStats(!showStats)}
              className="rounded-lg border border-slate-700/50 bg-slate-800 p-2 transition-colors hover:bg-slate-700"
              title="Toggle estadísticas"
            >
              <Info className="w-4 h-4 text-cyan-400" />
            </button>
            <button
              onClick={handleZoomIn}
              className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700/50"
              title="Acercar"
            >
              <ZoomIn className="w-4 h-4 text-cyan-400" />
            </button>
            <button
              onClick={handleZoomOut}
              className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700/50"
              title="Alejar"
            >
              <ZoomOut className="w-4 h-4 text-cyan-400" />
            </button>
            <button
              onClick={handleCenterGraph}
              className="p-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 rounded-lg transition-colors shadow-lg shadow-cyan-500/20"
              title="Centrar y ajustar"
            >
              <Maximize2 className="w-4 h-4 text-white" />
            </button>
          </div>
        </div>
      </div>
      
      <div className="min-h-0 flex-1">
        <ForceGraph2D
          ref={graphRef}
          graphData={graphData}
          width={viewport.width}
          height={viewport.height}
        nodeLabel={(node: any) => {
          const layerNames = ['Categoría', 'Subcategoría', 'Memoria', 'Comentario'];
          const layerName = layerNames[node.layer] || 'Nodo';
          return `${node.name || 'Sin nombre'}\n[${layerName}]`;
        }}
        nodeColor={(node: any) => node.color || '#2196f3'}
        nodeVal={(node: any) => node.val || 6}
        nodeCanvasObject={(node: any, ctx, globalScale) => {
          const label = node.name || 'Nodo';
          const fontSize = 12/globalScale;
          ctx.font = `${fontSize}px Sans-Serif`;
          const textWidth = ctx.measureText(label).width;
          const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

          // Sombra del nodo
          ctx.shadowBlur = 15;
          ctx.shadowColor = node.color;
          
          // Dibujar nodo
          ctx.fillStyle = node.color;
          ctx.beginPath();
          ctx.arc(node.x!, node.y!, node.val || 5, 0, 2 * Math.PI, false);
          ctx.fill();
          
          ctx.shadowBlur = 0;
          
          // Etiqueta
          if (globalScale >= 0.8) {
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(node.x! - bckgDimensions[0] / 2, node.y! - bckgDimensions[1] / 2 + (node.val || 5) + 5, bckgDimensions[0], bckgDimensions[1]);
            
            ctx.fillStyle = 'white';
            ctx.fillText(label, node.x!, node.y! + (node.val || 5) + 5 + fontSize/2);
          }
        }}
        linkColor={(link: any) => {
          const sourceNode = graphData.nodes.find(n => n.id === link.source);
          return sourceNode?.color ? `${sourceNode.color}80` : 'rgba(33, 150, 243, 0.5)';
        }}
        linkWidth={2.5}
        linkDirectionalParticles={0}
        backgroundColor="transparent"
        // CONFIGURACIÓN PARA POSICIONES FIJAS
        enableNodeDrag={true}
        enableZoomInteraction={true}
        enablePanInteraction={true}
        warmupTicks={0}
        cooldownTicks={0}
        d3AlphaDecay={1}
        d3VelocityDecay={1}
        onNodeClick={(node: any) => {
          const fullName = node.name || 'Sin nombre';
          const emojiMatch = fullName.match(/^(\p{Emoji}+|\p{Emoji_Presentation}+)/u);
          const displayName = emojiMatch ? fullName.replace(emojiMatch[0], '').trim() : fullName;
          
          setSelectedNode({
            id: node.id,
            name: displayName,
            full_text: node.full_text,
            date: node.date,
            time: node.time,
            category: node.category,
            subcategory: node.subcategory,
            color: node.color || '#2196f3',
            layer: node.layer,
            user: node.user,
            type: node.type,
            important: node.important || false,
            has_reminder: node.has_reminder || false,
            archived: node.archived || false
          });
          setComment('');
          setShowReminderForm(false);
          setShowExpirationForm(false);
        }}
        />
      </div>
      
      {/* MODAL DE INFORMACIÓN MEJORADO */}
      {selectedNode && (
        <div className="absolute inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center z-50 p-4"
             onClick={() => setSelectedNode(null)}>
          <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl p-6 max-w-3xl w-full mx-4 shadow-2xl max-md:mx-0 max-md:max-h-[calc(100vh-2rem)] max-md:overflow-y-auto max-md:p-4"
               style={{ 
                 border: `2px solid ${selectedNode.color}`,
                 boxShadow: `0 0 40px ${selectedNode.color}40`
               }}
               onClick={(e) => e.stopPropagation()}>
            
            {/* Header Mejorado */}
            <div className="flex items-start justify-between mb-6 pb-4 border-b border-slate-700/50 max-md:mb-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-3 max-md:gap-2">
                  <div className="w-4 h-4 rounded-full animate-pulse shadow-lg" 
                       style={{ 
                         backgroundColor: selectedNode.color,
                         boxShadow: `0 0 20px ${selectedNode.color}`
                       }}></div>
                  <h3 className="text-2xl font-bold text-white break-words max-md:text-xl">{selectedNode.name}</h3>
                </div>
                <div className="flex items-center gap-3 flex-wrap">
                  {selectedNode.category && (
                    <span className="text-sm px-3 py-1 bg-slate-700/50 rounded-full text-slate-300 border border-slate-600/50">
                      📁 {selectedNode.category} → {selectedNode.subcategory}
                    </span>
                  )}
                  <span className="text-xs px-2 py-1 bg-slate-700/50 rounded-full text-slate-400 border border-slate-600/50">
                    Capa {selectedNode.layer}: {selectedNode.layer === 0 ? 'Categoría Principal' : selectedNode.layer === 1 ? 'Subcategoría' : selectedNode.type === 'comment' ? 'Comentario' : 'Memoria'}
                  </span>
                  {selectedNode.important && (
                    <span className="text-xs px-2 py-1 bg-yellow-500/20 rounded-full text-yellow-400 border border-yellow-500/30 font-semibold">
                      ⭐ Importante
                    </span>
                  )}
                  {selectedNode.has_reminder && (
                    <span className="text-xs px-2 py-1 bg-blue-500/20 rounded-full text-blue-400 border border-blue-500/30 font-semibold">
                      🔔 Con Recordatorio
                    </span>
                  )}
                </div>
              </div>
              <button 
                onClick={() => setSelectedNode(null)}
                className="p-2.5 hover:bg-slate-700/50 rounded-xl transition-all hover:scale-110 border border-slate-700/50">
                <X className="w-5 h-5 text-slate-400" />
              </button>
            </div>
            
            {/* Fecha y Hora Mejorada */}
            {selectedNode.date && selectedNode.time && (
              <div className="bg-gradient-to-r from-slate-800/80 to-slate-700/80 rounded-xl p-4 mb-4 border border-slate-600/50">
                <div className="flex items-center gap-8 text-sm max-md:flex-col max-md:items-start max-md:gap-3">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-cyan-500/20 rounded-lg border border-cyan-500/30">
                      <span className="text-2xl">📅</span>
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs font-medium mb-1">Fecha</p>
                      <p className="text-white font-bold">{selectedNode.date}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-500/20 rounded-lg border border-blue-500/30">
                      <span className="text-2xl">🕐</span>
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs font-medium mb-1">Hora</p>
                      <p className="text-white font-bold">{selectedNode.time}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Mensaje Completo Mejorado */}
            {selectedNode.full_text && (
              <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/50 rounded-xl p-5 mb-4 border border-slate-600/50">
                <div className="flex items-center gap-2 mb-3">
                  <div className="p-1.5 bg-purple-500/20 rounded-lg border border-purple-500/30">
                    <span className="text-lg">💬</span>
                  </div>
                  <p className="text-slate-300 text-sm font-bold">
                    {selectedNode.type === 'comment' ? 'Comentario Añadido' : 'Memoria Completa'}
                  </p>
                </div>
                <p className="text-white text-base leading-relaxed bg-slate-900/50 rounded-lg p-4 border border-slate-700/30">
                  {selectedNode.full_text}
                </p>
                {selectedNode.user && (
                  <p className="text-slate-400 text-xs mt-3 flex items-center gap-2">
                    <span className="px-2 py-1 bg-slate-700/50 rounded-full border border-slate-600/50">
                      👤 {selectedNode.user}
                    </span>
                  </p>
                )}
              </div>
            )}
            
            {/* Sección de Comentarios Mejorada */}
            {selectedNode.type === 'memory' && selectedNode.id && (
              <div className="bg-gradient-to-br from-cyan-900/20 to-blue-900/20 rounded-xl p-5 mb-4 border border-cyan-500/30">
                <div className="flex items-center gap-2 mb-3">
                  <div className="p-1.5 bg-cyan-500/20 rounded-lg border border-cyan-500/30">
                    <span className="text-lg">📝</span>
                  </div>
                  <p className="text-cyan-300 text-sm font-bold">
                    Añadir Comentario / Continuar Historia
                  </p>
                </div>
                <textarea
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Escribe tus pensamientos, actualizaciones o cómo evolucionó esta memoria..."
                  className="w-full bg-slate-800 text-white rounded-xl p-4 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500/50 border border-slate-700/50 placeholder-slate-500"
                  rows={3}
                  disabled={savingComment}
                />
                <div className="flex items-center justify-between mt-3 max-md:flex-col max-md:items-stretch max-md:gap-3">
                  <p className="text-xs text-slate-400 flex items-center gap-1.5 max-md:leading-relaxed">
                    <span className="w-1.5 h-1.5 bg-purple-400 rounded-full"></span>
                    Los comentarios aparecerán como nodos morados conectados a esta memoria
                  </p>
                  <button
                    onClick={() => handleSaveComment(selectedNode.id!)}
                    disabled={!comment.trim() || savingComment}
                    className="px-5 py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 text-white rounded-xl text-sm font-bold transition-all shadow-lg hover:shadow-cyan-500/30 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-none max-md:w-full"
                  >
                    {savingComment ? '⏳ Guardando...' : '💾 Guardar Comentario'}
                  </button>
                </div>
              </div>
            )}

            {/* GESTIÓN DE MEMORIA Mejorada */}
            {selectedNode.type === 'memory' && selectedNode.id && (
              <div className="bg-gradient-to-br from-yellow-900/20 to-orange-900/20 rounded-xl p-5 border border-yellow-500/30">
                <div className="flex items-center gap-2 mb-4">
                  <div className="p-1.5 bg-yellow-500/20 rounded-lg border border-yellow-500/30">
                    <span className="text-lg">⚙️</span>
                  </div>
                  <p className="text-yellow-300 text-sm font-bold">
                    Gestionar Memoria
                  </p>
                </div>
                
                <div className="grid grid-cols-2 gap-3 mb-3 max-md:grid-cols-1">
                  {/* Botón Importante */}
                  <button
                    onClick={() => handleToggleImportance(selectedNode.id!, selectedNode.important || false)}
                    className={`px-4 py-3 rounded-xl text-sm font-bold transition-all border ${
                      selectedNode.important
                        ? 'bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 text-white border-yellow-500/50 shadow-lg shadow-yellow-500/30'
                        : 'bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 hover:text-white border-slate-600/50'
                    }`}
                  >
                    {selectedNode.important ? '⭐ Quitar Importante' : '⭐ Marcar Importante'}
                  </button>
                  
                  {/* Botón Recordatorio */}
                  <button
                    onClick={() => setShowReminderForm(!showReminderForm)}
                    className="px-4 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white rounded-xl text-sm font-bold transition-all border border-blue-500/50 shadow-lg shadow-blue-500/30"
                  >
                    🔔 {selectedNode.has_reminder ? 'Cambiar' : 'Agregar'} Recordatorio
                  </button>
                  
                  {/* Botón Caducidad */}
                  <button
                    onClick={() => setShowExpirationForm(!showExpirationForm)}
                    className="px-4 py-3 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 text-white rounded-xl text-sm font-bold transition-all border border-orange-500/50 shadow-lg shadow-orange-500/30"
                  >
                    ⏰ Establecer Caducidad
                  </button>
                  
                  {/* Botón Eliminar */}
                  <button
                    onClick={() => handleDeleteMemory(selectedNode.id!)}
                    className="px-4 py-3 bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white rounded-xl text-sm font-bold transition-all border border-red-500/50 shadow-lg shadow-red-500/30"
                  >
                    🗑️ Eliminar Memoria
                  </button>
                </div>

                {/* Formulario Recordatorio Mejorado */}
                {showReminderForm && (
                  <div className="bg-slate-800/80 rounded-xl p-4 mb-3 border border-blue-500/30">
                    <p className="text-blue-300 text-sm mb-3 font-bold flex items-center gap-2">
                      <span>🔔</span> Configurar Recordatorio
                    </p>
                    <input
                      type="datetime-local"
                      value={reminderDate}
                      onChange={(e) => setReminderDate(e.target.value)}
                      className="w-full bg-slate-700 text-white rounded-lg px-3 py-2.5 text-sm mb-3 border border-slate-600/50 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                    />
                    <input
                      type="text"
                      value={reminderMessage}
                      onChange={(e) => setReminderMessage(e.target.value)}
                      placeholder="Mensaje personalizado (opcional)"
                      className="w-full bg-slate-700 text-white rounded-lg px-3 py-2.5 text-sm mb-3 border border-slate-600/50 focus:outline-none focus:ring-2 focus:ring-blue-500/50 placeholder-slate-500"
                    />
                    <div className="flex gap-2 max-md:flex-col">
                      <button
                        onClick={() => handleSetReminder(selectedNode.id!)}
                        className="flex-1 px-4 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white rounded-lg text-sm font-bold transition-all shadow-lg"
                      >
                        ✅ Guardar
                      </button>
                      <button
                        onClick={() => setShowReminderForm(false)}
                        className="px-4 py-2.5 bg-slate-600 hover:bg-slate-700 text-white rounded-lg text-sm font-semibold transition-colors max-md:w-full"
                      >
                        ✖️ Cancelar
                      </button>
                    </div>
                  </div>
                )}

                {/* Formulario Caducidad Mejorado */}
                {showExpirationForm && (
                  <div className="bg-slate-800/80 rounded-xl p-4 border border-orange-500/30">
                    <p className="text-orange-300 text-sm mb-3 font-bold flex items-center gap-2">
                      <span>⏰</span> Establecer Fecha de Caducidad
                    </p>
                    <input
                      type="datetime-local"
                      value={expirationDate}
                      onChange={(e) => setExpirationDate(e.target.value)}
                      className="w-full bg-slate-700 text-white rounded-lg px-3 py-2.5 text-sm mb-3 border border-slate-600/50 focus:outline-none focus:ring-2 focus:ring-orange-500/50"
                    />
                    <p className="text-xs text-slate-400 mb-3 bg-slate-900/50 rounded-lg p-2.5 border border-slate-700/30">
                      ℹ️ Las memorias caducadas se archivarán automáticamente y no aparecerán en búsquedas
                    </p>
                    <div className="flex gap-2 max-md:flex-col">
                      <button
                        onClick={() => handleSetExpiration(selectedNode.id!)}
                        className="flex-1 px-4 py-2.5 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 text-white rounded-lg text-sm font-bold transition-all shadow-lg"
                      >
                        ✅ Guardar
                      </button>
                      <button
                        onClick={() => setShowExpirationForm(false)}
                        className="px-4 py-2.5 bg-slate-600 hover:bg-slate-700 text-white rounded-lg text-sm font-semibold transition-colors max-md:w-full"
                      >
                        ✖️ Cancelar
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
      
      {/* Panel de Estadísticas */}
      {showStats && (
        <div className="absolute top-24 right-4 bg-gradient-to-br from-slate-900/95 to-slate-800/95 backdrop-blur-md p-5 rounded-xl border border-cyan-500/30 shadow-2xl shadow-cyan-500/10 min-w-[240px] max-md:left-3 max-md:right-3 max-md:top-16 max-md:min-w-0 max-md:max-h-[70%] max-md:overflow-y-auto max-md:p-3">
          <h3 className="text-sm font-bold text-cyan-300 mb-4 flex items-center gap-2">
            <span className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse"></span>
            Estadísticas de Red
          </h3>
          <div className="space-y-3">
            <div className="bg-slate-800/50 rounded-lg p-3 border border-cyan-500/20">
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">Total Neuronas</span>
                <span className="text-lg font-bold text-white">{graphData.nodes.length}</span>
              </div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 border border-blue-500/20">
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">Total Sinapsis</span>
                <span className="text-lg font-bold text-white">{graphData.links.length}</span>
              </div>
            </div>
            <div className="border-t border-slate-700/50 pt-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="flex items-center gap-2 text-cyan-400">
                  <span className="w-2 h-2 bg-cyan-400 rounded-full"></span>
                  Categorías
                </span>
                <span className="font-bold text-white">{stats.categories}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="flex items-center gap-2 text-blue-400">
                  <span className="w-2 h-2 bg-blue-400 rounded-full"></span>
                  Subcategorías
                </span>
                <span className="font-bold text-white">{stats.subcategories}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="flex items-center gap-2 text-green-400">
                  <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                  Memorias
                </span>
                <span className="font-bold text-white">{stats.memories}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="flex items-center gap-2 text-purple-400">
                  <span className="w-2 h-2 bg-purple-400 rounded-full"></span>
                  Comentarios
                </span>
                <span className="font-bold text-white">{stats.comments}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* LEYENDA Mejorada (oculta en móvil para no solaparse con el panel de estadísticas) */}
      <div className="absolute bottom-4 left-4 bg-gradient-to-br from-slate-900/95 to-slate-800/95 backdrop-blur-md p-5 rounded-xl border border-cyan-500/30 shadow-2xl shadow-cyan-500/10 max-md:hidden">
        <h3 className="text-sm font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent mb-4 flex items-center gap-2">
          <span className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse"></span>
          Guía Visual
        </h3>
        <div className="space-y-3">
          <div className="bg-slate-800/50 rounded-lg p-2.5 border border-slate-700/50">
            <p className="text-[10px] text-slate-400 uppercase tracking-wider mb-2 font-semibold">Flujo de Datos</p>
            <div className="flex items-center gap-2 text-xs text-slate-300">
              <span className="text-cyan-400 font-bold">←</span>
              <span>Izquierda a Derecha = Tiempo</span>
            </div>
          </div>
          
          <div className="space-y-2">
            <p className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Tipos de Nodos</p>
            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 bg-cyan-400 rounded-full shadow-lg shadow-cyan-400/50"></div>
                <span className="text-cyan-300 font-medium">Categorías Principales</span>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 bg-blue-400 rounded-full shadow-lg shadow-blue-400/50"></div>
                <span className="text-blue-300 font-medium">Subcategorías</span>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 bg-green-400 rounded-full shadow-lg shadow-green-400/50"></div>
                <span className="text-green-300 font-medium">Memorias Originales</span>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 bg-purple-400 rounded-full shadow-lg shadow-purple-400/50"></div>
                <span className="text-purple-300 font-medium">Comentarios/Historia</span>
              </div>
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 rounded-lg p-2.5 border border-yellow-500/30">
            <div className="flex items-center gap-2 text-xs">
              <span className="text-yellow-400 text-base">🖱️</span>
              <span className="text-yellow-300 font-semibold">Click en un nodo para ver detalles</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
