-- Schema para Cerebro Digital con pgvector
-- PostgreSQL 14+ con extensión pgvector

-- Activar extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de memorias (almacenamiento principal)
CREATE TABLE IF NOT EXISTS memories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    short_content VARCHAR(255),
    embedding vector(384),  -- Dimensión para all-MiniLM-L6-v2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    importance FLOAT DEFAULT 0.5,
    confidence FLOAT DEFAULT 1.0,
    memory_type VARCHAR(50) DEFAULT 'general'  -- FACT, OPINION, GOAL, EVENT, etc.
);

-- Tabla de entidades (personas, lugares, eventos)
CREATE TABLE IF NOT EXISTS entities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,  -- PERSONA, LUGAR, EVENTO, EMOCION
    icon VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, entity_type)
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    icon VARCHAR(10),
    color VARCHAR(20),
    description TEXT
);

-- Tabla de subcategorías
CREATE TABLE IF NOT EXISTS subcategories (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(10),
    UNIQUE(category_id, name)
);

-- Relación memoria-entidad
CREATE TABLE IF NOT EXISTS memory_entities (
    memory_id INTEGER REFERENCES memories(id) ON DELETE CASCADE,
    entity_id INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    PRIMARY KEY (memory_id, entity_id)
);

-- Relación memoria-subcategoría
CREATE TABLE IF NOT EXISTS memory_subcategories (
    memory_id INTEGER REFERENCES memories(id) ON DELETE CASCADE,
    subcategory_id INTEGER REFERENCES subcategories(id) ON DELETE CASCADE,
    PRIMARY KEY (memory_id, subcategory_id)
);

-- Relaciones entre entidades (grafo de conocimiento)
CREATE TABLE IF NOT EXISTS entity_relationships (
    id SERIAL PRIMARY KEY,
    source_entity_id INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    target_entity_id INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    relationship_type VARCHAR(100),  -- "pareja_de", "hermano_de", "trabajo_en", etc.
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comentarios/hilos sobre memorias
CREATE TABLE IF NOT EXISTS memory_comments (
    id SERIAL PRIMARY KEY,
    memory_id INTEGER REFERENCES memories(id) ON DELETE CASCADE,
    parent_comment_id INTEGER REFERENCES memory_comments(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    user_name VARCHAR(100) DEFAULT 'Usuario',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    layer INTEGER DEFAULT 3
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_memories_embedding ON memories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_memories_user_id ON memories(user_id);
CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_memory_entities_memory ON memory_entities(memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_entities_entity ON memory_entities(entity_id);

-- Insertar usuario por defecto
INSERT INTO users (name, email) VALUES ('Usuario', 'usuario@cerebrodigital.local')
ON CONFLICT (email) DO NOTHING;

-- Insertar categorías base
INSERT INTO categories (name, icon, color, description) VALUES
    ('Familia', '👨‍👩‍👧‍👦', '#ff6b6b', 'Personas y relaciones familiares'),
    ('Lugares', '🏠', '#4ecdc4', 'Sitios y ubicaciones importantes'),
    ('Eventos', '🎂', '#ffd93d', 'Momentos y acontecimientos especiales'),
    ('Emociones', '💭', '#a855f7', 'Sentimientos y estados emocionales')
ON CONFLICT (name) DO NOTHING;
