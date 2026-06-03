# AGENTS.md

Guía para agentes de Cursor que trabajan en este repositorio.

## Cursor Cloud specific instructions

### Qué es este repo

Herramienta de evaluación conversacional (**Agent Evaluation** / `agenteval`) para probar el VoiceBot LATAM. No incluye el agente en producción: orquesta pruebas YAML contra **Amazon Bedrock Agents** o un endpoint **LangChain** HTTP.

### Dependencias (automáticas en cada sesión Cloud)

El script de actualización de VM instala:

- `agent-evaluation` (CLI `agenteval`, evaluador en Bedrock)
- `pyyaml` (planes de prueba y claves Jira en YAML)
- `requests` (target `langchain-agent`)

Añade `~/.local/bin` al `PATH` si hace falta: `export PATH="$HOME/.local/bin:$PATH"`.

### Servicios para desarrollo local

| Servicio | Obligatorio | Cómo arrancar |
|----------|-------------|----------------|
| **Mock LangChain** | Solo para pruebas LangChain sin agente real | `python mock_langchain_server.py` (puerto 8000). Usar tmux para procesos en segundo plano. |
| **Amazon Bedrock** | Sí, para cualquier `agenteval run` / `agente-evaluador.py` | Credenciales en `.env` (plantilla `env.txt`). El **evaluador** siempre usa Bedrock aunque el target sea mock. |
| **Bedrock Agent / endpoint LangChain real** | Según el YAML | IDs en YAML (`bedrock-agent`) o `agent_endpoint` (LangChain). |

### Comandos habituales

Desde la raíz del repo (`/workspace`):

```bash
export PATH="$HOME/.local/bin:$PATH"

# Verificar sintaxis Python
python3 -m compileall -q agenteval agente-evaluador.py mock_langchain_server.py

# Servidor mock (terminal aparte / tmux)
python3 mock_langchain_server.py

# Probar el target LangChain contra el mock (sin Bedrock)
PYTHONPATH=. python3 -c "
from agenteval.targets.langchain_agent import LangChainAgentTarget
t = LangChainAgentTarget(agent_endpoint='http://localhost:8000')
t.start_new_session('test')
print(t.invoke('equipaje nacional').response[:200])
"

# Ejecutar un plan (necesita AWS + plan con agenteval.yml en el directorio de trabajo)
python3 -m agenteval run --plan-dir /ruta/al/plan --work-dir /ruta/salida --verbose

# Runner por lotes (carga .env si existe)
python3 agente-evaluador.py --archivos "HU611_langchain.yml" --dir-pruebas tests/Sprint6/
```

Para la ruta rápida con mock, ver `PRUEBA_RAPIDA_LANGCHAIN.md`: en el YAML usar `agent_endpoint: http://localhost:8000` y levantar `mock_langchain_server.py` antes del runner.

### Lint / tests

- No hay pipeline de lint ni `pytest` en el repo.
- Comprobación práctica: `python3 -m compileall` (arriba).
- Las pruebas “reales” son los YAML en `tests/` ejecutados vía `agente-evaluador.py` o `python -m agenteval run`.

### Variables de entorno

Copiar `env.txt` → `.env` y completar al menos:

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` (si aplica)
- `AWS_REGION` (p. ej. `us-east-1`)
- `AWS_PROFILE` (muchos YAML usan perfil `Asistente`)

Jira (opcional): `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_TOKEN`, `TEST_CYCLE`.

Sin credenciales AWS, `agenteval run` falla con `Unable to locate credentials` en el resumen/trace.

### Modo sin credenciales AWS (desarrollo local / Cloud)

Puedes validar el entorno sin secretos:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 mock_langchain_server.py   # en tmux o terminal aparte
./scripts/verify_local_env.sh
```

Eso comprueba dependencias, sintaxis, CLIs y (si el mock está arriba) el target LangChain. No sustituye una corrida E2E con Bedrock.

### Notas no obvias

- El paquete pip `agent-evaluation` coexiste con el código vendoreado en `./agenteval`. `agente-evaluador.py` importa el **local** y fija `PYTHONPATH` al invocar `python -m agenteval run`.
- Resultados de ejecución: `.agenteval_runs/` (runner) o el `--work-dir` indicado; trazas en `agenteval_traces/`.
- La mayoría de YAML en `tests/` apuntan a `bedrock-agent` y requieren agente desplegado en AWS, no solo el mock.
