"""
Configuración de base de datos PostgreSQL con pgvector
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Configuración de base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/cerebro_digital"
)

# Motor de base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False  # Cambiar a True para debug SQL
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos ORM
Base = declarative_base()


@contextmanager
def get_db():
    """Context manager para sesiones de base de datos"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_database():
    """Inicializa la base de datos ejecutando schema.sql"""
    try:
        # Verificar si pgvector está instalado
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM pg_extension WHERE extname = 'vector'"))
            if not result.fetchone():
                print("⚠️  Instalando extensión pgvector...")
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
                print("✅ Extensión pgvector instalada")
        
        # Ejecutar schema
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            with engine.connect() as conn:
                # Ejecutar cada statement por separado
                for statement in schema_sql.split(';'):
                    statement = statement.strip()
                    if statement:
                        conn.execute(text(statement))
                conn.commit()
            
            print("✅ Base de datos inicializada correctamente")
        else:
            print("⚠️  schema.sql no encontrado")
        
        return True
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False


def test_connection():
    """Prueba la conexión a la base de datos"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Conexión exitosa a PostgreSQL")
            print(f"   Versión: {version[:50]}...")
            
            # Verificar pgvector
            result = conn.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'"))
            if result.fetchone():
                print("✅ Extensión pgvector disponible")
            else:
                print("⚠️  Extensión pgvector NO encontrada")
            
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False


if __name__ == "__main__":
    print("🔍 Probando conexión a base de datos...")
    if test_connection():
        print("\n🚀 Inicializando schema...")
        init_database()
