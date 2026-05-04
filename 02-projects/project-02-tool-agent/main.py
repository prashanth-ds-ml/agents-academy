import re
import time
import datetime
from pathlib import Path

import ollama as ollama_client
from langchain_ollama import OllamaLLM
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from prompts import BRAINSTORM_PROMPT, PLAN_PROMPT, REACT_PROMPT, FOLLOWUP_PROMPT
from router import parse_react_step, call_tool, needs_confirm, format_args

console = Console()

MAX_REACT_STEPS = 15

# ─── Helpers ──────────────────────────────────────────────────────────────────

def strip_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    return text.strip()


def invoke_with_spinner(chain, inputs: dict, msg: str = "Thinking") -> tuple:
    t0 = time.time()
    with console.status(f"  [dim italic]{msg}...[/dim italic]", spinner="dots"):
        result = chain.invoke(inputs)
    return result.strip(), round(time.time() - t0, 1)


def stream_response(chain, inputs: dict) -> str:
    chunks = []
    for chunk in chain.stream(inputs):
        console.print(chunk, end="", highlight=False)
        chunks.append(chunk)
    console.print()
    return "".join(chunks)

# ─── Model picker ─────────────────────────────────────────────────────────────

def pick_model() -> str:
    try:
        models = ollama_client.list().models
    except Exception:
        console.print("[yellow]  Could not reach Ollama. Using mistral:latest.[/yellow]")
        return "mistral:latest"

    if not models:
        return "mistral:latest"

    table = Table(show_header=False, box=None, pad_edge=False, padding=(0, 2))
    table.add_column("num", style="dim cyan", width=4)
    table.add_column("name", style="bold white")
    table.add_column("size", style="dim")
    for i, m in enumerate(models, start=1):
        size_gb = f"{m.size / 1e9:.1f} GB" if m.size else ""
        table.add_row(f"[{i}]", m.model, size_gb)

    console.print()
    console.print("  [dim]Available models:[/dim]")
    console.print()
    console.print(table)
    console.print()

    while True:
        raw = console.input("  [dim]Pick a model (number or name, Enter for mistral:latest):[/dim] ").strip()
        if not raw:
            chosen = "mistral:latest"
            break
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(models):
                chosen = models[idx].model
                break
            console.print(f"  [red]Enter a number between 1 and {len(models)}.[/red]")
        else:
            names = [m.model for m in models]
            if raw in names:
                chosen = raw
                break
            console.print(f"  [red]Model '{raw}' not found. Try the number instead.[/red]")

    console.print(f"\n  [green]Using:[/green] [bold]{chosen}[/bold]\n")
    return chosen

# ─── Phase 1: Brainstorm ──────────────────────────────────────────────────────

def parse_brainstorm_response(response: str) -> tuple[str, str, bool]:
    ready = "READY_TO_PLAN" in response
    thinking, questions = "", ""
    if "THINKING:" in response:
        ts = response.index("THINKING:") + len("THINKING:")
        if "QUESTIONS:" in response:
            thinking = response[ts : response.index("QUESTIONS:")].strip()
            questions = response[response.index("QUESTIONS:") + len("QUESTIONS:") :].strip()
        elif "READY_TO_PLAN" in response:
            thinking = response[ts : response.index("READY_TO_PLAN")].strip()
        else:
            thinking = response[ts:].strip()
    else:
        questions = response.strip()
    return thinking, questions, ready


def run_brainstorm_loop(goal: str, llm: OllamaLLM) -> str:
    history_entries: list[str] = []
    round_num = 0

    console.print(Rule("[bold cyan]Brainstorming[/bold cyan]", style="cyan"))
    console.print()

    while True:
        round_num += 1
        history_text = "\n\n".join(history_entries) if history_entries else "None yet."
        chain = BRAINSTORM_PROMPT | llm
        response, elapsed = invoke_with_spinner(chain, {"goal": goal, "history": history_text})
        thinking, questions_text, ready = parse_brainstorm_response(response)

        if thinking:
            console.print(
                Panel(
                    Text(strip_markdown(thinking), style="dim"),
                    border_style="dim",
                    padding=(0, 2),
                    title=f"[dim]thinking  {elapsed}s[/dim]",
                    title_align="right",
                )
            )
            console.print()

        if ready:
            console.print(Text("  ✓ Agent has enough context. Moving to planning...", style="green bold"))
            console.print()
            console.print(Rule(style="dim cyan"))
            console.print()
            break

        question_lines = [
            line.strip()
            for line in questions_text.splitlines()
            if re.match(r"^\d+[\.\)]\s+.+", line.strip())
        ]

        if not question_lines:
            console.print(Text("  ✓ Ready to plan.", style="green bold"))
            console.print()
            console.print(Rule(style="dim cyan"))
            console.print()
            break

        if round_num > 1:
            console.print(Rule(f"[dim]Round {round_num}[/dim]", style="dim"))
            console.print()

        round_qa: list[str] = []
        for line in question_lines:
            console.print(f"  [bold white]{line}[/bold white]", highlight=False)
            try:
                answer = console.input("  [dim cyan]›[/dim cyan] ")
            except EOFError:
                answer = "no answer given"
            round_qa.append(f"{line}\nAnswer: {answer or 'no answer given'}")
            console.print()

        history_entries.append("\n\n".join(round_qa))

    return "\n\n".join(history_entries)

# ─── Phase 2: ReAct Execution ─────────────────────────────────────────────────

def run_react_loop(plan: str, llm: OllamaLLM) -> None:
    history_entries: list[str] = []

    console.print(Rule("[bold cyan]Executing Plan[/bold cyan]", style="cyan"))
    console.print()
    console.print("  [dim]The agent will work through the plan step by step.[/dim]")
    console.print("  [dim]You will be asked to confirm before any file or shell action.[/dim]")
    console.print()

    for step in range(1, MAX_REACT_STEPS + 1):
        history_text = "\n\n".join(history_entries) if history_entries else "None yet."
        chain = REACT_PROMPT | llm
        response, elapsed = invoke_with_spinner(
            chain, {"plan": plan, "history": history_text}, msg=f"Step {step}"
        )

        parsed = parse_react_step(response)

        # Show thought panel
        thought = parsed.get("thought", "")
        if thought:
            console.print(
                Panel(
                    Text(strip_markdown(thought), style="dim"),
                    border_style="dim",
                    padding=(0, 2),
                    title=f"[dim]thought  step {step}  {elapsed}s[/dim]",
                    title_align="right",
                )
            )
            console.print()

        # Parse error — model didn't follow format
        if parsed["type"] == "error":
            console.print(f"  [yellow]Could not parse model output at step {step}. Stopping.[/yellow]")
            console.print(f"  [dim]{parsed['raw'][:200]}[/dim]\n")
            break

        # Done
        if parsed["type"] == "final":
            console.print(Rule("[bold green]Execution complete[/bold green]", style="green"))
            console.print()
            console.print(parsed["answer"])
            console.print()
            break

        # Tool call
        tool = parsed["tool"]
        args = parsed["args"]
        args_display = format_args(args)

        console.print(f"  [cyan]◆ {tool}[/cyan]([dim]{args_display}[/dim])")

        # Confirm destructive actions
        if needs_confirm(tool):
            try:
                confirm = console.input("    [yellow]confirm? [y/n][/yellow] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                confirm = "n"
            if confirm != "y":
                observation = "User declined. Skipped."
                console.print(f"  [dim]Skipped.[/dim]\n")
                history_entries.append(
                    f"Step {step}:\nThought: {thought}\n"
                    f"Action: {tool}({args_display})\nObservation: {observation}"
                )
                continue

        # Run the tool
        observation = call_tool(tool, args)
        truncated = observation[:300] + "..." if len(observation) > 300 else observation
        console.print(f"  [dim green]→ {truncated}[/dim green]\n")

        history_entries.append(
            f"Step {step}:\nThought: {thought}\n"
            f"Action: {tool}({args_display})\nObservation: {observation}"
        )

    else:
        console.print(f"  [yellow]Reached max steps ({MAX_REACT_STEPS}). Stopping.[/yellow]\n")

# ─── Commands ─────────────────────────────────────────────────────────────────

COMMANDS = {
    "/help":    "Show available commands",
    "/model":   "Switch the AI model",
    "/new":     "Start a new goal (clears current session)",
    "/execute": "Run the ReAct execution loop on the current plan",
    "/save":    "Save the current plan to a markdown file",
    "/clear":   "Clear the screen",
    "/exit":    "Exit",
}


def show_help() -> None:
    console.print()
    table = Table(show_header=False, box=None, pad_edge=False, padding=(0, 2))
    table.add_column("cmd", style="bold cyan", width=12)
    table.add_column("desc", style="dim white")
    for cmd, desc in COMMANDS.items():
        table.add_row(cmd, desc)
    console.print(table)
    console.print()


def save_plan(goal: str, plan_text: str) -> None:
    plans_dir = Path(__file__).parent / "plans"
    plans_dir.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    slug = re.sub(r"[^\w\s-]", "", goal[:40]).strip().replace(" ", "-").lower()
    filename = plans_dir / f"{timestamp}-{slug}.md"
    content = (
        f"# Goal Plan\n\n"
        f"**Goal:** {goal}\n\n"
        f"**Generated:** {timestamp}\n\n"
        f"---\n\n"
        f"{plan_text}\n"
    )
    filename.write_text(content, encoding="utf-8")
    console.print(f"\n  [green]✓ Saved →[/green] [bold]{filename.relative_to(Path(__file__).parent)}[/bold]\n")


def show_welcome() -> None:
    console.print()
    console.print(Rule("[bold cyan]Goal Planner + Execution Agent[/bold cyan]", style="cyan"))
    console.print()
    console.print("  [dim]Phase 1 — Describe a goal. The agent brainstorms and builds a plan.[/dim]")
    console.print("  [dim]Phase 2 — The agent executes the plan step by step using real tools.[/dim]")
    console.print()
    console.print("  Type [cyan]/help[/cyan] for commands.")
    console.print()

# ─── Main REPL ────────────────────────────────────────────────────────────────

def main() -> None:
    show_welcome()
    model_name = pick_model()
    llm = OllamaLLM(model=model_name)

    goal = ""
    context = ""
    plan_text = ""
    conversation: list[str] = []

    console.print(Rule(style="dim"))
    console.print()

    while True:
        if plan_text:
            prompt = "  [dim cyan]◆[/dim cyan] "
        else:
            prompt = "  [bold]Goal[/bold] [dim cyan]›[/dim cyan] "

        try:
            user_input = console.input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n  [dim]Goodbye.[/dim]\n")
            break

        if not user_input:
            continue

        # ── Slash commands ──────────────────────────────────────────────────
        if user_input.startswith("/"):
            cmd = user_input.lower().split()[0]

            if cmd in ("/exit", "/quit"):
                console.print("\n  [dim]Goodbye.[/dim]\n")
                break

            elif cmd == "/help":
                show_help()

            elif cmd == "/clear":
                console.clear()
                show_welcome()
                console.print(f"  [dim]Model: {model_name}[/dim]\n")

            elif cmd == "/model":
                console.print(Rule(style="dim"))
                model_name = pick_model()
                llm = OllamaLLM(model=model_name)
                console.print(Rule(style="dim"))
                console.print()

            elif cmd == "/new":
                goal, context, plan_text, conversation = "", "", "", []
                console.print()
                console.print(Rule(style="dim"))
                console.print()
                console.print("  [green]✓ Session cleared.[/green]  Enter a new goal.\n")

            elif cmd == "/save":
                if not plan_text:
                    console.print("\n  [yellow]No plan to save yet.[/yellow]\n")
                else:
                    save_plan(goal, plan_text)

            elif cmd == "/execute":
                if not plan_text:
                    console.print("\n  [yellow]No plan yet. Enter a goal first.[/yellow]\n")
                else:
                    console.print()
                    run_react_loop(plan_text, llm)
                    console.print(Rule(style="dim"))
                    console.print(f"  [dim]◆ ask a follow-up  ·  /execute to run again  ·  /new  ·  /exit[/dim]")
                    console.print()

            else:
                console.print(f"\n  [red]Unknown command:[/red] {cmd}   (try /help)\n")

            continue

        # ── Follow-up conversation ───────────────────────────────────────────
        if plan_text:
            history_text = "\n".join(conversation) if conversation else "None yet."
            chain = FOLLOWUP_PROMPT | llm
            console.print()
            response = stream_response(chain, {
                "goal": goal,
                "context": context,
                "plan": plan_text,
                "history": history_text,
                "message": user_input,
            })
            conversation.append(f"User: {user_input}")
            conversation.append(f"Assistant: {response.strip()}")
            console.print()
            console.print(Rule(style="dim"))
            console.print(f"  [dim]◆ ask follow-up  ·  /execute to act on plan  ·  /save  ·  /new  ·  /exit[/dim]")
            console.print()
            continue

        # ── New goal: brainstorm → plan ──────────────────────────────────────
        goal = user_input
        console.print()

        try:
            context = run_brainstorm_loop(goal, llm)

            console.print(Rule("[bold cyan]Planning[/bold cyan]", style="cyan"))
            console.print()

            chain = PLAN_PROMPT | llm
            plan_text = stream_response(chain, {"goal": goal, "context": context})

            console.print()
            console.print(Rule(style="dim"))
            console.print(
                f"  [dim]Model: {model_name}  ·  "
                f"/execute to act on this plan  ·  "
                f"/save to export  ·  "
                f"ask a follow-up  ·  /new[/dim]"
            )
            console.print()

        except Exception as err:
            console.print(f"\n  [yellow]Error: {err}[/yellow]\n")
            goal = ""


if __name__ == "__main__":
    main()
