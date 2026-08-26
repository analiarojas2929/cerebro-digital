export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  category?: string;
  timestamp: Date;
  relatedMemories?: RelatedMemory[];
}

export interface RelatedMemory {
  content: string;
  similarity: number;
  category?: string;
}

export interface MessageInput {
  message: string;
  session_id?: string;
  user_id?: string;
}

export interface MessageResponse {
  response: string;
  session_id: string;
  category?: string;
  sentiment?: string;
  related_memories: RelatedMemory[];
  confidence: number;
}

export interface MemoryStats {
  total_conversations: number;
  total_memories: number;
  categories: CategoryStat[];
}

export interface CategoryStat {
  name: string;
  count: number;
}

export interface Category {
  id: number;
  name: string;
  description?: string;
  keywords: string[];
  color?: string;
  icon?: string;
  conversation_count: number;
}
