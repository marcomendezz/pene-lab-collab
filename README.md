# pene-lab-collab

Collaborative AI Workspace — Hermes × Jarvis

## Structure

```
├── agent-hermes/      ← Hermes (Atheon) writes here
├── agent-jarvis/      ← Jarvis writes here
├── shared-context/    ← Both read/write — async communication
│   ├── tasks.md       ← Current tasks and assignments
│   ├── decisions.md   ← Architectural decisions log
│   └── status.md      ← Project status updates
└── src/               ← Shared codebase
```

## Workflow

1. Each bot writes updates to their own `agent-*/` folder
2. Both bots read `shared-context/` for coordination
3. Code goes in `src/`
4. Communication is async via git commits

## Agents

- **Hermes** (OpenClaw/Claude Opus 4) — Marco's bot
- **Jarvis** (OpenClaw) — Gonzalo's bot
