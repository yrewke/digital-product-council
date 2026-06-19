# Model Routing Policy

Do not hardcode unavailable model names. The operator should inspect the active Codex environment before a real run and record available choices in the run charter.

## Economy Tier

Use for formatting, metadata, routing, anonymization, claim extraction, request deduplication, status updates, and schema validation.

## Standard Reasoning Tier

Use for ordinary executive memos, evidence synthesis, implementation analysis, and peer review.

## Frontier Reasoning Tier

Use only for difficult Contrarian or First-Principles analysis, major internal contradiction resolution, and high-stakes internal validation. External Chairman and Devil's Advocate work is not routed through Codex.

## Sub-Agent Dispatch

## Current Verification

`codex.cmd doctor` on 2026-06-17 reported Codex `0.131.0` with active model `gpt-5.5`. The local TOML agent profiles are available as separate role entry points, but this repository does not rely on unverified per-agent model keys.

For real runs, use visible isolated sub-agents for substantive role reasoning whenever the current Codex session exposes sub-agent tools. Model tier labels guide dispatch prompts and optional model overrides; they do not require hardcoded model keys in TOML.

Required real-run role dispatch:

- Standard or Frontier: `codex-council-v2-contrarian`, `codex-council-v2-first-principles`, `codex-council-v2-expansionist`, `codex-council-v2-outsider`, and `codex-council-v2-executor` for independent executive memos.
- Economy or Standard: `codex-council-v2-librarian` for evidence routing and cache/provenance packets.
- Standard or Frontier: `codex-council-v2-auditor` for substantive factual and numerical review.
- External Chairman and Devil's Advocate roles are not Codex sub-agents and must not be dispatched by this routing policy.

The operator keeps deterministic engine commands, state transitions, validation, and user-visible progress in the main Codex session.

## Explicit Manual Fallback

The run charter records tier assignments. If sub-agent spawning itself is unavailable, the `$codex-council-v2` operator must tell the user before continuing, label the run notes `MANUAL_SINGLE_SESSION_FALLBACK`, and use explicit tier labels in prompts:

- Economy: run engine commands, packet creation, metadata, and validation.
- Standard: ordinary executive memos, peer review, and evidence synthesis.
- Frontier: difficult Contrarian / First-Principles passes, major internal contradiction resolution, and final internal handoff validation.

Do not spend frontier reasoning on mechanical file operations.
