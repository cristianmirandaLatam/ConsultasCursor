# 📝 ¿Qué necesitas para probar LangChain?

## ✅ Checklist Completo

### **1. Software/Dependencias** ⚙️
```bash
- [x] Python 3.8+ ✅ (ya lo tienes)
- [ ] pip install requests
```

### **2. Endpoint de LangChain** 🔌
**Elige UNA opción:**

#### **Opción A: Servidor Mock** ⭐ MÁS FÁCIL
```bash
✅ No necesitas nada más
✅ Ya está incluido: mock_langchain_server.py
✅ Corre en local: http://localhost:8000
```

#### **Opción B: Endpoint Real**
```bash
❓ Necesitas preguntar al equipo:
   "¿Cuál es la URL del agente LangChain en STG?"
   
   Ejemplos:
   - https://api-stg.latam.com/langchain-agent
   - https://xxxxx.execute-api.us-east-1.amazonaws.com/stg
```

### **3. YAML Configurado** 📄
```bash
✅ Ya creado: tests/Sprint6/HU611_langchain.yml
⚠️ SOLO edita línea 10: agent_endpoint
```

---

## 🚀 Comandos para Probar (copia y pega)

### **Con Servidor Mock** (Probar en 2 minutos)

**Terminal 1:**
```powershell
# Editar YAML primero
# Abrir: tests/Sprint6/HU611_langchain.yml
# Línea 10: agent_endpoint: http://localhost:8000

# Iniciar mock
python mock_langchain_server.py
```

**Terminal 2:**
```powershell
# Instalar dependencia
pip install requests

# Ejecutar test
python agente-evaluador.py --archivos "HU611_langchain.yml" --dir-pruebas tests/Sprint6/ --detallado
```

---

### **Con Endpoint Real** (Cuando lo tengas)

```powershell
# 1. Editar YAML
# tests/Sprint6/HU611_langchain.yml línea 10:
# agent_endpoint: https://TU-URL-REAL

# 2. Probar conectividad
python test_langchain_connection.py --endpoint https://TU-URL-REAL --verbose

# 3. Ejecutar test
python agente-evaluador.py --archivos "HU611_langchain.yml" --dir-pruebas tests/Sprint6/ --detallado
```

---

## 📊 Qué Esperar

### **✅ Si funciona correctamente:**
```
Carpeta de esta ejecución: .agenteval_runs\20260113_143000
Encontrados 1 archivo(s). En paralelo: 1
[Passed] tests\Sprint6\HU611_langchain.yml -> .agenteval_runs\...

===== RESUMEN POR ARCHIVO =====
    Passed    45.32s  tests\Sprint6\HU611_langchain.yml

Total: 1 | OK: 1 | FAILED: 0
```

### **❌ Errores Comunes:**

**Error 1: Connection refused**
```
Error: Connection refused
```
👉 Solución: Asegúrate de que el mock esté corriendo o el endpoint sea correcto

**Error 2: Module not found**
```
ModuleNotFoundError: No module named 'requests'
```
👉 Solución: `pip install requests`

**Error 3: 404 Not Found**
```
HTTP Error 404
```
👉 Solución: Verifica que el endpoint incluya `/invoke` o ajusta en target.py

---

## 🎯 Flujo Visual

```
┌─────────────────────────────────────────┐
│  1. Instalar requests                   │
│     pip install requests                │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  2. Editar YAML                         │
│     agent_endpoint: http://localhost... │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  3. Iniciar mock (Terminal 1)           │
│     python mock_langchain_server.py     │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  4. Ejecutar test (Terminal 2)          │
│     python agente-evaluador.py ...      │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  5. ✅ Ver resultados                   │
│     [Passed] test exitoso!              │
└─────────────────────────────────────────┘
```

---

## 📁 Archivos Creados para Ti

| Archivo | Qué es | Para qué |
|---------|--------|----------|
| `tests/Sprint6/HU611_langchain.yml` | ✅ Test configurado | Úsalo para probar |
| `mock_langchain_server.py` | ✅ Servidor mock | Pruebas sin agente real |
| `test_langchain_connection.py` | ✅ Test de conectividad | Verificar endpoint |
| `PRUEBA_RAPIDA_LANGCHAIN.md` | ✅ Guía detallada | Instrucciones completas |

---

## ⏱️ Tiempo Estimado

| Actividad | Tiempo |
|-----------|--------|
| Instalar requests | 1 minuto |
| Editar YAML | 1 minuto |
| Iniciar mock | 30 segundos |
| Ejecutar test | 2-3 minutos |
| **TOTAL** | **5 minutos** |

---

## 🎓 Resumen Ultra-Corto

**Para probar AHORA mismo:**
1. `pip install requests`
2. Edita `tests/Sprint6/HU611_langchain.yml` línea 10: `agent_endpoint: http://localhost:8000`
3. Terminal 1: `python mock_langchain_server.py`
4. Terminal 2: `python agente-evaluador.py --archivos "HU611_langchain.yml" --dir-pruebas tests/Sprint6/ --detallado`

**Eso es TODO.** ✅

---

## 🆘 Si Algo Falla

Lee: `PRUEBA_RAPIDA_LANGCHAIN.md` (guía completa con debugging)

O dime qué error ves y te ayudo. 😊

