# 🧪 Prueba Rápida de LangChain

## ✅ Requisitos Previos (Checklist)

- [ ] Python 3.8+ instalado
- [ ] pip funcional
- [ ] Repositorio clonado

---

## 🚀 Opción 1: Probar con Servidor Mock (SIN necesitar el agente real)

### **Paso 1: Instalar dependencia**
```bash
pip install requests
```

### **Paso 2: Editar el YAML**
Abre `tests/Sprint6/HU611_langchain.yml` y cambia la línea 10:
```yaml
agent_endpoint: http://localhost:8000  # ← Cambia a localhost
```

### **Paso 3: Iniciar el servidor mock** (Terminal 1)
```bash
python mock_langchain_server.py
```

Deberías ver:
```
🚀 Servidor Mock de LangChain iniciado
📍 URL: http://localhost:8000
```

### **Paso 4: Ejecutar el test** (Terminal 2 - nueva ventana)
```bash
python agente-evaluador.py \
  --archivos "HU611_langchain.yml" \
  --dir-pruebas tests/Sprint6/ \
  --detallado
```

### **Paso 5: Verificar resultados**
Revisa:
- ✅ La consola debe mostrar la ejecución
- ✅ En el Terminal 1 verás las peticiones llegando
- ✅ Resultados en `.agenteval_runs/TIMESTAMP/`

---

## 🌐 Opción 2: Probar con Endpoint Real

### **Paso 1: Obtener el endpoint**
Pregunta al equipo de infra/desarrollo:
```
¿Cuál es la URL del agente LangChain en STG?
```

Ejemplos comunes:
- `https://api-stg.latam.com/langchain-agent`
- `https://xxxxx.execute-api.us-east-1.amazonaws.com/stg`

### **Paso 2: Configurar el YAML**
Edita `tests/Sprint6/HU611_langchain.yml` línea 10:
```yaml
agent_endpoint: https://TU-URL-REAL-AQUI
```

### **Paso 3: Probar conectividad**
```bash
python test_langchain_connection.py \
  --endpoint https://TU-URL-REAL-AQUI \
  --verbose
```

Si funciona, verás:
```
✅ Conexión exitosa!
✅ Campo 'output' encontrado
```

### **Paso 4: Ejecutar el test**
```bash
python agente-evaluador.py \
  --archivos "HU611_langchain.yml" \
  --dir-pruebas tests/Sprint6/ \
  --detallado
```

---

## 📊 Entender los Resultados

### **✅ Test Exitoso**
```
[Passed] tests/Sprint6/HU611_langchain.yml -> .agenteval_runs/...
```

### **❌ Test Fallido - Connection Error**
```
Error: Connection refused
```

**Solución:**
- Verifica que el endpoint sea correcto
- Si usas mock, verifica que esté corriendo
- Verifica firewall/VPN si es endpoint real

### **❌ Test Fallido - 404 Not Found**
```
HTTP Error 404
```

**Solución:**
- Verifica la ruta del endpoint
- Puede ser `/invoke`, `/agent`, `/chat`
- Ajusta en `agenteval/targets/langchain_agent/target.py` línea 54

### **❌ Test Fallido - Response parsing**
```
Error: 'output' key not found
```

**Solución:**
- Tu API devuelve la respuesta con otro nombre
- Ajusta en `agenteval/targets/langchain_agent/target.py` línea 60:
  ```python
  agent_response = data.get("tu_campo", "")  # Cambia "tu_campo"
  ```

---

## 🔍 Debugging

### **Ver logs detallados:**
```bash
# Busca el directorio de ejecución
ls -la .agenteval_runs/

# Entra al más reciente
cd .agenteval_runs/20260113_XXXXXX/hu611_langchain/

# Ver logs
cat logs/stdout.log
cat logs/stderr.log

# Ver traces
cat agenteval_traces/*.json
```

### **Ver peticiones en el mock:**
Si usas el servidor mock, verás cada petición en tiempo real:
```
==========================================
[14:30:45] Nueva consulta
Session ID: abc123...
Input: quiero saber sobre mi equipaje
Config: {...}
Response: Hola! Con gusto te ayudo...
==========================================
```

---

## ⚙️ Ajustar el Target (si tu API es diferente)

Si tu API de LangChain tiene estructura diferente:

### **1. Ver qué envía actualmente:**
Edita `agenteval/targets/langchain_agent/target.py` línea 38:
```python
# Agregar print para debug
print(f"DEBUG - Enviando payload: {json.dumps(payload, indent=2)}")
```

### **2. Ver qué responde:**
Línea 58:
```python
# Agregar print para debug
print(f"DEBUG - Respuesta recibida: {json.dumps(data, indent=2)}")
```

### **3. Ajustar según tu API:**
```python
# Si tu API usa "message" en lugar de "input":
payload = {
    "message": prompt,  # ← Cambio aquí
    "session_id": self.session_id,
    ...
}

# Si tu API devuelve "answer" en lugar de "output":
agent_response = data.get("answer", "")  # ← Cambio aquí
```

---

## 📋 Resumen de Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `tests/Sprint6/HU611_langchain.yml` | Test configurado para LangChain |
| `mock_langchain_server.py` | Servidor mock para pruebas sin agente real |
| `test_langchain_connection.py` | Verifica conectividad con endpoint |
| `agenteval/targets/langchain_agent/target.py` | Implementación del target (ajustar aquí si API es diferente) |

---

## 🎯 Siguiente Paso: Probar AHORA

**Opción más fácil (5 minutos):**
```bash
# Terminal 1
python mock_langchain_server.py

# Terminal 2
pip install requests
python agente-evaluador.py --archivos "HU611_langchain.yml" --dir-pruebas tests/Sprint6/ --detallado
```

**Si funciona:** ¡Felicidades! Ya tienes la integración lista. Solo falta cambiar a la URL real cuando esté disponible.

**Si no funciona:** Revisa la sección de debugging arriba o avísame qué error ves.

---

## 🆘 Ayuda Rápida

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: requests` | `pip install requests` |
| `Connection refused` | ¿Mock corriendo? ¿URL correcta? |
| `404 Not Found` | Verifica ruta `/invoke` en target.py |
| `KeyError: 'output'` | Ajusta parsing en target.py línea 60 |
| Tests muy lentos | Normal, Claude evalúa cada respuesta |

---

¿Listo para probar? ¡Adelante! 🚀

