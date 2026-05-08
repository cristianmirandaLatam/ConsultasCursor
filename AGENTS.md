## Cursor Cloud specific instructions

### Overview

This is an AI agent evaluation framework ("agente-evaluador") for testing conversational AI agents (voicebots/chatbots). It is a customized fork of [Amazon's agent-evaluation](https://github.com/awslabs/agent-evaluation). The main entry point is `agente-evaluador.py`, and the core library lives in `agenteval/`.

### Running the application

- **CLI help:** `PYTHONPATH=. python3 agente-evaluador.py --help`
- **Run all tests:** `PYTHONPATH=. python3 agente-evaluador.py`
- **Run specific test:** `PYTHONPATH=. python3 agente-evaluador.py --archivos "HU611_langchain.yml" --dir-pruebas tests/Sprint6/`
- **Verbose mode:** add `--detallado`
- **Parallel execution:** `PYTHONPATH=. python3 agente-evaluador.py -j 4`

`PYTHONPATH=.` is required so Python resolves the local `agenteval/` package instead of the upstream PyPI `agent-evaluation` package.

### External service dependencies

All tests require **AWS credentials** for the Bedrock Runtime evaluator (LLM judge). Without valid AWS credentials the tests will always fail with `Unable to locate credentials`. Configure via a `.env` file (see `env.txt` for the template) or standard AWS environment variables.

**Jira/Zephyr Scale** integration is optional and configured via `.env` variables (`JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_TOKEN`, `TEST_CYCLE`).

### Local testing with mock server

For testing the LangChain target integration without real AWS endpoints, use the mock server:

1. Terminal 1: `python3 mock_langchain_server.py` (starts on port 8000)
2. Terminal 2: Set `agent_endpoint: http://localhost:8000` in the test YAML, then run

Note: the evaluator step still requires AWS Bedrock credentials even when using the mock target.

### Key gotchas

- The local `agenteval/` directory shadows the upstream `agent-evaluation` PyPI package. Always set `PYTHONPATH=.` (or the workspace root) when running.
- Test YAML files reference AWS profiles (e.g., `aws_profile: Asistente`) in the evaluator section. These must exist in the AWS config or be removed/overridden.
- There is no `requirements.txt` or `pyproject.toml` in the repo. Dependencies are: `agent-evaluation`, `boto3`, `click`, `pydantic`, `rich`, `requests`, `pyyaml`.
- Test results are written to `.agenteval_runs/` directory.
