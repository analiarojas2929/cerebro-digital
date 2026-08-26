# 🤖 Cómo Activar la IA para Conversación (Kostra AI)

## ✅ Ya Instalado

Tu sistema ya tiene todo lo necesario instalado:
- ✅ OpenAI SDK (v3.3.1) - compatible con Kostra
- ✅ Código de conversación con IA
- ✅ Servidor mejorado

## 🔑 Configura tu API Key de Kostra

### ¿Qué es Kostra?

Kostra es un proveedor de IA que ofrece acceso a modelos avanzados como **DeepSeek v3.2**:
- Compatible con la API de OpenAI
- Más económico que OpenAI
- Excelente rendimiento en español

### Paso 1: Obtener API Key de Kostra

1. **Regístrate en Kostra**:
   - Ve a: https://kostra.cloud
   - Crea tu cuenta
   - Ve a la sección de API Keys

2. **Crea tu API key**:
   - Copia tu API key de Kostra

### Paso 2: Configurar tu Sistema

Abre el archivo `backend/.env` y reemplaza:

```env
KOSTRA_KEY=tu-kostra-key-aqui
```

Por tu API key real:

```env
KOSTRA_KEY=TU-KEY-REAL-DE-KOSTRA
```

### Paso 3: Reiniciar el Servidor

```powershell
# Detener servidor actual (Ctrl+C en la terminal del backend)

# Reiniciar
cd backend
python server.py
```

## 🎉 ¡Listo!

Ahora tu Cerebro Digital tendrá conversación inteligente con OpenAI GPT-3.5.

### Ejemplo de Conversación

**Sin IA:**
```
Usuario: "Mi pareja se llama Sebastián"
Bot: "📝 Personas mencionadas: Pareja"
```

**Con IA (Kostra - DeepSeek v3.2):**
```
Usuario: "Mi pareja se llama Sebastián"
Bot: "Qué bonito nombre. ¿Cuánto tiempo llevan juntos? Me encantaría conocer más sobre tu relación para poder recordar esos momentos especiales."

Usuario: "Llevamos 3 años"
Bot: "¡Tres años juntos! Eso es especial. Cuéntame, ¿cómo se conocieron Sebastián y tú? Me gustaría guardar esa historia."
```

## 💰 Costos

Kostra es más económico que OpenAI:
- Precios competitivos
- Modelo DeepSeek v3.2 de alto rendimiento
- Excelente en español

## ⚠️ Sin API Key

Si no tienes Kostra configurado, el sistema funcionará con respuestas básicas:
- Detecta personas, lugares, eventos
- Categoriza automáticamente
- Guarda todo en memoria
- Red neuronal visual
- Solo las respuestas son simples

## 🔒 Seguridad

- Tu API key NUNCA se comparte
- Solo tú la ves en tu archivo `.env`
- Las conversaciones van directo de tu PC a Kostra
- Nadie más tiene acceso

---

**¿Listo para activar la IA?**

1. Obtén tu API key de Kostra: https://kostra.cloud
2. Edita `backend/.env` y agrega `KOSTRA_KEY=tu-key`
3. Reinicia el servidor
4. ¡Conversa con tu Cerebro Digital inteligente!
