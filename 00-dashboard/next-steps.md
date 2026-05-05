# Next Steps

When you reopen the vault, start here.

## Current focus — CodeMitra phases 1–9 done, next: diff preview + test loop

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
| 1–4 | Foundation, chat, filesystem agent, routing | ✅ Done |
| 5 | Code reader agent | ✅ Done |
| 6 | Shell agent | ✅ Done |
| 7 | Planner agent | ✅ Done |
| 8 | Memory vault | ✅ Done |
| 9 | Brainstorm loop (from Academy Project 1) | ✅ Done |
| 10 | Diff preview before writes + test loop | 🔲 **Next** |
| 11 | `/explain` and `/fix` slash commands | 🔲 Planned |
| 12 | Project auto-detect on startup | 🔲 Planned |

---

## How academy and CodeMitra connect

```
Academy lesson/project    →    CodeMitra phase
──────────────────────────────────────────────
Project 1 (goal planner)  →    Brainstorm Agent + Planner Agent ✅
Project 2 (ReAct tools)   →    Filesystem Agent execution loop  ✅
Project 3 (code reader)   →    Code Reader Agent                ✅
Project 4 (memory)        →    Memory vault                     ✅
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
