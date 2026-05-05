# Next Steps

When you reopen the vault, start here.

## Current focus — Project 2 done, CodeMitra phase 4 is next

### Agents Academy

| Item | Status |
|---|---|
| Lesson 1 — Foundations | ✅ Done |
| Lesson 2 — Tools | ✅ Done |
| Project 1 — Goal Planner | ✅ Done |
| Project 2 — ReAct Tool Agent | ✅ Done |
| Lesson 3 — Code Reader patterns | 🔲 Next |
| Lesson 4 — Memory | 🔲 Planned |
| Project 3 — Code Reader Agent | 🔲 Next |

### CodeMitra (→ local-codex repo)

| Phase | Description | Status |
|---|---|---|
| 1–3 | Foundation, chat, filesystem agent | ✅ Done |
| 4 | Routing end-to-end test | ⚠️ Needs test |
| 5 | Code reader agent | 🔲 Next |
| 6 | Shell agent | 🔲 Planned |
| 7 | Planner agent | 🔲 Planned |
| 8 | Memory | 🔲 Planned |

---

## How academy and CodeMitra connect

```
Academy lesson/project    →    CodeMitra phase
──────────────────────────────────────────────
Project 1 (goal planner)  →    Conversation Agent + Planner Agent
Project 2 (ReAct tools)   →    Filesystem Agent execution loop
Project 3 (code reader)   →    Phase 5 — Code Reader Agent
Project 4 (memory)        →    Phase 8 — Memory layer
```

Learn the pattern in the academy → implement it properly in CodeMitra.

---

## Run Project 1

```powershell
cd C:\Users\prash\Projects\agents-academy
.venv\Scripts\Activate.ps1
cd 02-projects\project-01-goal-planner
python main.py
```

## Run Project 2

```powershell
cd C:\Users\prash\Projects\agents-academy
.venv\Scripts\Activate.ps1
cd 02-projects\project-02-tool-agent
python main.py
```

## Run CodeMitra

```powershell
cd C:\Users\prash\Projects\local-codex
.venv\Scripts\Activate.ps1
codemitra
```

---

## Rule for smooth learning

Never finish a session without:

- one exercise attempt
- one memory note
- one reflection update
