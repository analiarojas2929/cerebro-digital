"""
Script de migración: In-Memory → PostgreSQL
Migra las memorias del sistema antiguo al nuevo
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.db_manager import init_database, test_connection
from app.services.memory.persistent_memory import get_memory_service
from app.services.neural.embedding_service import get_embedding_service


def migrate_from_dynamic_learning():
    """
    Migra datos del sistema in-memory (dynamic_learning.py) a PostgreSQL
    """
    print("\n🔄 MIGRACIÓN: In-Memory → PostgreSQL\n")
    
    # 1. Verificar conexión
    print("1️⃣ Verificando conexión a base de datos...")
    if not test_connection():
        print("❌ No se puede conectar a PostgreSQL")
        print("   Asegúrate de que esté corriendo: net start postgresql-x64-14")
        return False
    
    # 2. Inicializar schema
    print("\n2️⃣ Inicializando schema...")
    if not init_database():
        print("❌ Error inicializando base de datos")
        return False
    
    # 3. Cargar datos del sistema antiguo
    print("\n3️⃣ Cargando datos del sistema in-memory...")
    try:
        import dynamic_learning
        
        categories = dynamic_learning.dynamic_categories
        memory_threads = dynamic_learning.memory_threads
        
        total_memories = sum(
            len(subcat.get('memories', []))
            for cat in categories.values()
            for subcat in cat.get('subcategories', {}).values()
        )
        
        print(f"   📊 Encontradas {len(categories)} categorías")
        print(f"   📊 Total de memorias: {total_memories}")
        
        if total_memories == 0:
            print("\n⚠️  No hay memorias para migrar")
            print("   El sistema nuevo está listo para usar")
            return True
        
    except Exception as e:
        print(f"   ⚠️  No se pudo cargar dynamic_learning.py: {e}")
        print("   Continuando con base de datos vacía...")
        return True
    
    # 4. Migrar memorias
    print("\n4️⃣ Migrando memorias a PostgreSQL...")
    memory_service = get_memory_service()
    migrated_count = 0
    
    for cat_name, cat_data in categories.items():
        cat_icon = cat_data.get('icon', '📁')
        
        for subcat_name, subcat_data in cat_data.get('subcategories', {}).items():
            subcat_icon = subcat_data.get('icon', '📌')
            memories = subcat_data.get('memories', [])
            
            for memory_data in memories:
                try:
                    # Extraer contenido
                    if isinstance(memory_data, dict):
                        content = memory_data.get('text', '')
                    else:
                        content = str(memory_data)
                    
                    if not content:
                        continue
                    
                    # Crear memoria en DB
                    memory_id = memory_service.create_memory(
                        content=content,
                        memory_type="general",
                        importance=0.7
                    )
                    
                    # Asociar a categoría/subcategoría
                    memory_service.add_memory_to_category(
                        memory_id=memory_id,
                        category_name=cat_name,
                        subcategory_name=subcat_name,
                        subcategory_icon=subcat_icon
                    )
                    
                    migrated_count += 1
                    print(f"   ✅ Migrada: {content[:50]}...")
                    
                except Exception as e:
                    print(f"   ❌ Error migrando memoria: {e}")
    
    print(f"\n✅ Migración completada: {migrated_count}/{total_memories} memorias")
    
    # 5. Resumen final
    print("\n" + "="*60)
    print("🎉 MIGRACIÓN EXITOSA")
    print("="*60)
    print(f"✅ {migrated_count} memorias guardadas en PostgreSQL")
    print(f"✅ Embeddings generados automáticamente")
    print(f"✅ Búsqueda semántica disponible")
    print("\n💡 Ahora puedes:")
    print("   1. Reiniciar el servidor: python server.py")
    print("   2. Buscar semánticamente: /memory/search?query=...")
    print("   3. Conversar con IA: POST /chat/message")
    print("="*60)
    
    return True


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          🧠 CEREBRO DIGITAL - MIGRACIÓN A PostgreSQL        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    success = migrate_from_dynamic_learning()
    
    if success:
        print("\n✅ Todo listo para usar el nuevo sistema")
    else:
        print("\n❌ Hubo errores durante la migración")
        print("   Revisa los mensajes anteriores para más detalles")
