# Analysis scripts — deterministic only

- No imports from `graph/` or any LLM SDK.
- Input must be a validated MoTeC CSV per `contracts/telemetry_input.md`.
- Output must match the JSON schema in `contracts/lap_delta_output.schema.json`.
- If a channel is missing or all-zero, exit code 1 and write a dead-letter record.
- Never invent a corner name that is not in the track metadata.