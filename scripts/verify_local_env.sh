#!/usr/bin/env bash
# Verificación local sin credenciales AWS (mock LangChain opcional).
set -euo pipefail
export PATH="${HOME}/.local/bin:${PATH}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== Python =="
python3 --version

echo "== Dependencias =="
python3 -c "import agenteval, yaml, requests; print('imports OK')"

echo "== Sintaxis =="
python3 -m compileall -q agenteval agente-evaluador.py mock_langchain_server.py

echo "== CLIs =="
python3 -m agenteval --help >/dev/null && echo "agenteval OK"
python3 agente-evaluador.py --help >/dev/null && echo "agente-evaluador OK"

MOCK_URL="${MOCK_URL:-http://localhost:8000}"
if curl -sf -o /dev/null -m 2 -X POST "${MOCK_URL}/invoke" \
  -H 'Content-Type: application/json' \
  -d '{"input":"equipaje nacional","session_id":"verify","config":{}}'; then
  echo "== Mock LangChain (${MOCK_URL}) =="
  PYTHONPATH="$ROOT" python3 -c "
from agenteval.targets.langchain_agent import LangChainAgentTarget
t = LangChainAgentTarget(agent_endpoint='${MOCK_URL}')
t.start_new_session('verify')
r = t.invoke('equipaje nacional')
assert 'nacional' in r.response.lower(), r.response[:80]
print('LangChainAgentTarget OK')
"
else
  echo "== Mock LangChain =="
  echo "SKIP: no responde en ${MOCK_URL}. Inicia: python3 mock_langchain_server.py"
fi

echo ""
echo "Listo (modo sin AWS). Para E2E con Bedrock: copia env.txt a .env y completa AWS_*."
