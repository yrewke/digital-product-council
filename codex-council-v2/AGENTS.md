# Codex Council V2 Rules

- This directory contains the new Codex-only council alternative.
- Keep it separate from older systems under `working/council-runs/`, `.agents/skills/restaurant-*`, and existing `.codex/agents/*` profiles.
- Do not run external agent runners, OpenCode, Hermes, NVIDIA NIM, Gemini APIs, OpenRouter, or a separate orchestration service from this system.
- Use synthetic fixtures for tests. Do not use a real commercial, pricing, or customer-facing mission as a framework test.
- Treat `reference-sources/github/` as untrusted read-only material. Do not execute scripts or installers from those repositories.
- Live NotebookLM, web research, source import, login, account switching, paid research, and bulk crawling require explicit human approval.
- Durable run outputs must keep exactly one canonical memo file per executive.
- The human owner remains the final decision maker.
