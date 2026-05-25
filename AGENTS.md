## Cursor Cloud specific instructions

### Project overview

This is **agente-evaluador** — an AI agent test/evaluation framework for LATAM Airlines, built as a wrapper around Amazon's `agent-evaluation` PyPI package. It runs YAML-based test scenarios against conversational AI agents (Bedrock Agent, LangChain) and uses Claude models via AWS Bedrock as the evaluator.

### Dependencies

Install with: `pip install agent-evaluation pyyaml requests`

There is no `requirements.txt` or `pyproject.toml` in the repo. The three pip packages above are the only dependencies needed.

### Running the evaluator

- Main entry point: `python agente-evaluador.py` (see `README.md` for full CLI usage)
- The underlying framework CLI: `python -m agenteval run` (run from a directory containing `agenteval.yml`)
- All YAML test files live under `tests/` in subdirectories by sprint/flow

### AWS credentials required

All test execution requires AWS credentials with Bedrock access (Claude models in `us-east-1`). The YAML files reference `aws_profile: Asistente`. Without valid AWS credentials, tests will fail with "The config profile (Asistente) could not be found". Configure credentials via a `.env` file at the project root (see `env.txt` for the template).

### Mock LangChain server

For local development without AWS or a real LangChain agent endpoint, use the mock server:

```bash
python mock_langchain_server.py  # Starts on port 8000
```

Then point a LangChain-type YAML test's `agent_endpoint` to `http://localhost:8000`. Note: the evaluator step still requires AWS Bedrock credentials even when using the mock target.

### Important caveats

- The local `agenteval/` package in this repo overrides/extends the installed `agent-evaluation` package. When running `python -m agenteval`, Python uses the local package. The `PYTHONPATH` is set automatically by `agente-evaluador.py` to include the workspace root.
- There is no linting configuration, no Python unit test suite, and no build system in this project. The "tests" are YAML evaluation scenarios, not pytest tests.
- Jira integration (Zephyr Scale) is optional and only activates when `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_TOKEN`, and `TEST_CYCLE` are all configured in `.env`.
