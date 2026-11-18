# Velaris — Project Rules for OpenCode

## Architecture (never violate these boundaries)

Context → Reasoning → Execution → Coordination.
Nothing flows backward except append-only outcome logs.

- **Context**: Obsidian vault + LightRAG. Read-only from Reasoning.
- **Reasoning**: LangGraph. Decides which function to call and why.
- **Execution**: Deterministic Python only. Never calls a model. Never decides.
- **Coordination**: OpenMausBot. Moves files and approvals. Never queries LightRAG.

## Build order (enforce this)

1. Contracts (`contracts/`) before templates.
2. Templates (`templates/`) before any fill script.
3. Golden sample (`samples/`) before validator or analysis scripts.
4. `validate_file.py` before `lap_delta.py`.
5. `lap_delta.py` + `sector_rank.py` before `template_fill.py`.
6. No LangGraph until the manual vertical slice produces a signed MVO.

## Rules for every script

- Execution scripts must have typed input/output and exit codes 0/1/2.
- No model calls inside `automations/analysis/` or `automations/intake/`.
- No hardcoded model IDs; read from `config/models.yaml`.
- Every failure path must write to `dead_letter/` with a timestamped JSON record.

## Verification

Run `uv run pytest tests/unit` before proposing a commit.
Do not edit `templates/` without updating the matching schema in `contracts/`.