# AGENTS.md

Operational guide for coding agents working in this repository.

## 1) Repository Overview

- Stack: Python backend (Flask + Flask-SocketIO) and static HTML/CSS/JS frontend.
- Entry point: `server/app.py`.
- Core game logic: `server/game_engine.py`.
- Player/bot model: `server/bot_player.py`.
- Persistence helpers: `server/db.py` (SQLite file `game.db`).
- Frontend pages: `public/host/index.html`, `public/player/index.html`, shared styles in `public/shared.css`.

## 2) Environment Setup

Use Python 3.11+ when possible.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

If you need testing/linting tools that are not installed, install explicitly:

```bash
pip install pytest ruff mypy
```

## 3) Run / Build / Lint / Test Commands

There is no separate build system in this repo; runtime is the primary validation.

### Run the app (dev)

```bash
python3 server/app.py
```

Host/player URLs are printed by the app. Default port is `5000`.

### Build-like sanity checks

Use syntax compilation as a lightweight build gate:

```bash
python3 -m compileall server
```

### Lint/format checks

No repo-level lint config is present right now. Prefer safe defaults:

```bash
ruff check server
```

Optional auto-fix:

```bash
ruff check server --fix
```

### Type checks

Type hints are partial. Keep checks scoped and pragmatic:

```bash
mypy server
```

### Tests

At the time of writing, there is no committed `tests/` directory.

When tests are added, use:

```bash
pytest
```

Run a single test file:

```bash
pytest tests/test_game_engine.py
```

Run a single test function:

```bash
pytest tests/test_game_engine.py::test_best_hand_value
```

Run tests by keyword expression:

```bash
pytest -k "showdown and not slow"
```

## 4) Architecture and Change Boundaries

- Keep poker rules and state transitions inside `server/game_engine.py`.
- Keep socket event orchestration inside `server/app.py`.
- Keep player decision behavior inside `server/bot_player.py`.
- Keep DB access in `server/db.py`; avoid ad-hoc SQL in other modules.
- Prefer minimal, focused changes over broad refactors.

## 5) Code Style Guidelines

### Imports

- Group imports as: stdlib, third-party, local.
- Prefer absolute imports as currently used (e.g., `from game_engine import Game`).
- Avoid unused imports; remove immediately.

### Formatting

- Follow PEP 8 defaults.
- Use 4-space indentation.
- Keep lines readable; target <= 100 chars when practical.
- Prefer single quotes to match current codebase style.
- Preserve existing comment style and section dividers where already used.

### Naming

- Use `snake_case` for functions/variables.
- Use `PascalCase` for classes (`Game`, `BotPlayer`, `HumanPlayer`).
- Use `UPPER_SNAKE_CASE` for constants (`SUITS`, `RANK_VALUES`).
- Event names should stay explicit and stable (`join_game`, `player_action`).

### Types

- Add type hints for new/changed Python functions.
- Match current style: built-in generics (`list`, `dict`) are acceptable.
- Use precise return types for public helpers when practical.
- Do not over-engineer typing if it hurts clarity in game flow code.

### Data and State

- Treat server state (`connected_players`, `join_queue`, `current_game`) as the source of truth.
- Validate all client-provided inputs server-side before state mutation.
- Keep state transitions explicit and deterministic.

### Error Handling

- Validate early, return early.
- For socket handlers, emit clear error events/messages (`join_error`, `start_error`) and stop.
- Avoid broad `except Exception` unless there is a safe fallback path.
- Do not swallow exceptions silently.

### Logging and Diagnostics

- Use concise, structured `print` lines consistent with existing tags (`[join]`, `[disconnect]`).
- Include key identifiers (nickname, sid) when useful for debugging.
- Avoid noisy logs inside hot loops unless actively debugging.

### Frontend/CSS

- Preserve the established visual language in `public/host/index.html` and `public/player/index.html`.
- Reuse CSS variables and existing typography patterns.
- Favor targeted style tweaks over global visual shifts.
- Verify layout on both desktop and mobile after UI edits.

## 6) Database Conventions

- Use `get_connection()` from `server/db.py` for all DB operations.
- Keep SQL parameterized (`?` placeholders); never string-concatenate SQL.
- Keep schema changes backward-compatible unless explicitly requested.
- `game.db` is local and ignored by git; do not commit DB artifacts.

## 7) Git and Change Hygiene

- Do not revert unrelated local changes.
- Keep commits small and task-focused.
- Update docs when behavior/commands change.
- If adding new tooling (pytest/ruff/mypy configs), document commands here.

## 8) Agent Rule Files Check

Searched for repository-specific agent rules:

- `.cursor/rules/` -> not found
- `.cursorrules` -> not found
- `.github/copilot-instructions.md` -> not found

If any of these files are added later, treat them as higher-priority guidance and update this document.
