# 🔄 Guía Rápida: Migración a LangChain

## ✅ Archivos Creados

Ya tienes todo listo para la migración:

```
agenteval/targets/langchain_agent/
├── __init__.py           ✅ Módulo de Python
└── target.py             ✅ Implementación del target

tests/ejemplos_langchain/
└── HU611_langchain_ejemplo.yml  ✅ Ejemplo de YAML migrado
```

---

## 🎯 ¿Qué cambió en los YAMLs?

### ANTES (Bedrock):
```yaml
target:
  type: bedrock-agent
  bedrock_agent_id: LO6UKFHFZP
  bedrock_agent_alias_id: Y1UT4SVWGL
  bedrock_session_attributes:
    entityId: "..."
    country: "CL"
  bedrock_prompt_session_attributes:
    date: "2026-01-07"
    locale: "es-US"
```

### DESPUÉS (LangChain):
```yaml
target:
  type: langchain-agent
  agent_endpoint: https://tu-api-langchain.com/agent
  session_attributes:
    # Todos los atributos juntos
    entityId: "..."
    country: "CL"
    date: "2026-01-07"
    locale: "es-US"
```

---

## 🚀 Pasos para Migrar

### 1️⃣ Configurar el Endpoint

Edita tus YAMLs y cambia:
```yaml
target:
  type: langchain-agent
  agent_endpoint: https://TU-URL-REAL/agent  # ← Cambia esto
```

### 2️⃣ Ajustar el Target (si tu API es diferente)

Si tu API de LangChain tiene una estructura diferente, edita:
```
agenteval/targets/langchain_agent/target.py
```

Busca la línea ~38 donde se prepara el payload:
```python
payload = {
    "input": prompt,          # ← Ajusta según tu API
    "session_id": self.session_id,
    "config": { ... }
}
```

### 3️⃣ Migrar tus YAMLs

**Opción A: Manual** (para 1-2 archivos)
- Abre el YAML
- Reemplaza la sección `target:`
- Guarda

**Opción B: Ver ejemplo**
- Mira: `tests/ejemplos_langchain/HU611_langchain_ejemplo.yml`
- Copia la estructura del `target`

### 4️⃣ Probar

```bash
# Instalar dependencia
pip install requests

# Probar un test
python agente-evaluador.py \
  --archivos "tu_test.yml" \
  --detallado
```

---

## 🔍 Verificar que Funciona

### ✅ Checklist:

- [ ] El test se ejecuta sin errores de conexión
- [ ] Las conversaciones se completan
- [ ] Los resultados (A/B) se capturan correctamente
- [ ] Los JSON traces se generan en `.agenteval_runs/`
- [ ] Jira se actualiza correctamente (si está configurado)

---

## 🆘 Problemas Comunes

### Error: `ModuleNotFoundError: No module named 'requests'`
```bash
pip install requests
```

### Error: `Connection refused`
- Verifica que el `agent_endpoint` sea correcto
- Verifica conectividad (VPN, security groups)
- Prueba con curl:
  ```bash
  curl -X POST https://tu-endpoint/invoke \
    -H "Content-Type: application/json" \
    -d '{"input": "test"}'
  ```

### Error: `404 Not Found`
- Verifica la ruta del endpoint
- ¿Es `/invoke`, `/agent`, u otra?
- Ajusta en el `target.py` línea ~54

### La respuesta no se captura bien
- Revisa los logs en `.agenteval_runs/*/logs/stdout.log`
- Ajusta el parsing en `target.py` línea ~60:
  ```python
  agent_response = data.get("tu_campo_respuesta", "")
  ```

---

## 📚 Documentación Adicional

Para más detalles, consulta los archivos completos de documentación en el repositorio de GitHub:

- `MIGRACION_LANGCHAIN.md` - Guía completa
- `RESUMEN_MIGRACION_LANGCHAIN.md` - Resumen ejecutivo
- `migrar_yamls_a_langchain.py` - Script automático
- `test_langchain_connection.py` - Test de conectividad

---

## 💡 Ejemplo Completo

Ver: `tests/ejemplos_langchain/HU611_langchain_ejemplo.yml`

Este archivo muestra:
- ✅ Configuración del target para LangChain
- ✅ Session attributes combinados
- ✅ Variables globales (sin cambios)
- ✅ Tests (sin cambios)
- ✅ Integración con Jira (sin cambios)

---

## 🎓 Resumen

**Lo que NO cambia (90%):**
- ✅ Steps de los tests
- ✅ Expected results
- ✅ Variables globales
- ✅ Integración Jira
- ✅ Scripts de ejecución

**Lo que SÍ cambia (10%):**
- 🔧 Sección `target` en YAMLs
- 🔧 Endpoint de invocación

**Tiempo estimado:** 2-3 horas para migrar todo.

---

¿Dudas? Revisa los archivos de documentación completos o consulta con el equipo de desarrollo. 🚀

