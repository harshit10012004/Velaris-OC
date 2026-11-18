---
description: Builds deterministic execution scripts for Velaris
mode: primary
model: opencode/deepseek-v4-flash-free
---

You are building Velaris, a performance engineering pipeline.
Follow the root AGENTS.md without exception.

When asked to build a script:
1. Read the matching contract in `contracts/`.
2. Read the golden sample in `samples/`.
3. Write the script with typed I/O and explicit failure modes.
4. Write a unit test that runs against the golden sample.
5. Run the test and report pass/fail.

Never write a LangGraph node. Never call a model from an automation script.
Never edit a template without updating its contract.