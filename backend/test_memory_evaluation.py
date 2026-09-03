#!/usr/bin/env python3
"""
Script de prueba para el nuevo sistema de evaluación inteligente de memoria
Demuestra cómo funciona la puntuación de importancia y clasificación de tipos
"""

import sys
sys.path.insert(0, '.')

from dynamic_learning import evaluate_message

# Lista de mensajes de prueba
test_messages = [
    # TRIVIAL - No debe guardarse
    ("hola", "Saludo simple"),
    ("ok", "Respuesta trivial"),
    ("gracias", "Agradecimiento corto"),
    ("jaja", "Risa"),
    
    # TEMPORARY - Información temporal durante la sesión
    ("Ahora estoy probando una nueva función", "Trabajo temporal"),
    ("En este momento estoy trabajando en el login", "Tarea puntual"),
    ("Hoy quiero hacer una publicación en LinkedIn", "Meta del día"),
    
    # DUPLICATE - Información que ya existe
    ("Mi nombre es Juan y trabajo con React", "Primera vez guardada"),
    ("También trabajo con React", "Similar a anterior"),
    
    # MEMORY - Debe guardarse
    ("Nací en Santiago en 1990 y siempre he vivido en Chile", "Información personal importante"),
    ("Trabajo como desarrollador full-stack en una startup de IA", "Información laboral relevante"),
    ("Mi padre es ingeniero y mi hermana es médica", "Información familiar"),
    ("Recuerda que mi color favorito es el azul y me encanta leer", "Solicitud explícita"),
    ("Mi proyecto Digital Brain busca preservar memorias usando IA", "Contexto de proyecto importante"),
    ("Tengo la meta de aprender machine learning este año", "Objetivo a largo plazo"),
    ("Mi cumpleaños es el 15 de mayo", "Evento importante"),
    ("Vivo en La Providencia, el barrio más bonito de Santiago", "Información geográfica personal"),
]

print("=" * 80)
print("🧠 SISTEMA DE EVALUACIÓN INTELIGENTE DE MEMORIA")
print("=" * 80)
print()

# Agrupar resultados por categoría
results_by_decision = {}

for message, description in test_messages:
    evaluation = evaluate_message(message)
    
    decision = evaluation['decision']
    importance = evaluation['importance']
    action = evaluation['action']
    
    if decision not in results_by_decision:
        results_by_decision[decision] = []
    
    results_by_decision[decision].append({
        'message': message,
        'description': description,
        'importance': importance,
        'action': action,
        'reason': evaluation['reason']
    })
    
    # Mostrar cada resultado
    icon_map = {
        'TRIVIAL': '❌',
        'TEMPORARY': '⏱️',
        'MEMORY': '💾',
        'DUPLICATE': '🔁',
        'UPDATE': '✏️'
    }
    
    icon = icon_map.get(decision, '❓')
    print(f"{icon} {decision} (Score: {importance}/100) | {action}")
    print(f"   Mensaje: '{message}'")
    print(f"   Contexto: {description}")
    print(f"   Razón: {evaluation['reason']}")
    print()

print("=" * 80)
print("📊 RESUMEN POR CATEGORÍA")
print("=" * 80)
print()

for decision in ['MEMORY', 'TEMPORARY', 'TRIVIAL', 'DUPLICATE', 'UPDATE']:
    if decision in results_by_decision:
        count = len(results_by_decision[decision])
        print(f"\n{decision}: {count} mensaje(s)")
        for item in results_by_decision[decision]:
            print(f"  - {item['message'][:50]}... (Score: {item['importance']})")

print()
print("=" * 80)
print("✅ Test completado")
print("=" * 80)
