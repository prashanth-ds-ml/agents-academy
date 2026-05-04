import re
import time
import datetime
from pathlib import Path

import ollama as ollama_client
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

console = Console()

# ─── Prompts ──────────────────────────────────────────────────────────────────

BRAINSTORM_PROMPT = PromptTemplate.from_template(
    "You are a sharp goal analyst helping someone clarify their goal before planning.\n\n"
    "Goal: {goal}\n\n"
    "Previous Q&A:\n{history}\n\n"
    "INSTRUCTIONS:\n"
    "- Think through what you already understand and what you can reasonably assume.\n"
    "- Only ask questions you genuinely cannot answer yourself — true blockers.\n"
    "- Do NOT re-summarize previous answers. Do NOT repeat context already given.\n"
    "- Max 1-3 high-value questions per round. If you have enough context, output READY_TO_PLAN.\n"
    "- Do NOT include any template labels or instructions in your output.\n\n"
    "OUTPUT — choose one of these two forms only:\n\n"
    "Form A (need more info):\n"
    "THINKING:\n"
    "[your brief reasoning about what is still unclear]\n"
    "QUESTIONS:\n"
    "1. [first question]\n"
    "2. [second question]\n\n"
    "Form B (enough context):\n"
    "THINKING:\n"
    "[one sentence on what you understand]\n"
    "READY_TO_PLAN\n\n"
    "Output only Form A or Form B. Nothing else."
)

PLAN_PROMPT = PromptTemplate.from_template(
    "You are a practical goal planning assistant.\n"
    "Use the goal and clarifying context to produce a specific, actionable plan.\n\n"
    "Goal: {goal}\n\n"
    "Clarifying context:\n{context}\n\n"
    "Respond in exactly this format:\n\n"
    "Objective:\n"
    "- <one clear sentence stating what success looks like>\n\n"
    "Steps:\n"
    "1. <step 1>\n"
    "2. <step 2>\n"
    "3. <step 3>\n"
    "4. <step 4>\n\n"
    "Risks:\n"
    "- <risk 1>\n"
    "- <risk 2>\n\n"
    "Constraints:\n"
    "- <constraint 1>\n"
    "- <constraint 2>\n\n"
    "Next action:\n"
    "- <the very first concrete thing to do today>\n\n"
    "Be specific to the context given. No generic advice. No extra sections."
)

FOLLOWUP_PROMPT = PromptTemplate.from_template(
    "You are a planning assistant in an ongoing session. The user has received a plan and is asking follow-up questions.\n\n"
    "Goal: {goal}\n\n"
    "Context gathered during brainstorm:\n{context}\n\n"
    "Plan generated:\n{plan}\n\n"
    "Conversation so far:\n{history}\n\n"
    "User: {message}\n\n"
    "Respond concisely and helpfully. Stay focused on the goal and plan. "
    "Only repeat parts of the plan if directly asked."
)

# ─── Helpers ──────────────────────────────────────────────────────────────────

def strip_markdown(text: str) -> str:
    """Remove markdown syntax that renders poorly in a plain terminal."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    return text.strip()


def invoke_with_spinner(chain, inputs: dict, msg: str = "Thinking") -> tuple:
    """Invoke chain with a spinner. Returns (response_text, elapsed_seconds)."""
    t0 = time.time()
    with console.status(f"  [dim italic]{msg}...[/dim italic]", spinner="dots"):
        result = chain.invoke(inputs)
    return result.strip(), round(time.time() - t0, 1)


def stream_response(chain, inputs: dict) -> str:
    """Stream chain output live. Returns the full response text."""
    chunks = []
    for chunk in chain.stream(inputs):
        console.print(chunk, end="", highlight=False)
        chunks.append(chunk)
    console.print()
    return "".join(chunks)

# ─── Model picker ─────────────────────────────────────────────────────────────

def pick_model() -> str:
    """List available Ollama models and let the user choose one."""
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

# ─── Brainstorm loop ──────────────────────────────────────────────────────────

def parse_brainstorm_response(response: str) -> tuple[str, str, bool]:
    """Split model response into (thinking, questions, ready_to_plan)."""
    ready = "READY_TO_PLAN" in response
    thinking = ""
    questions = ""

    if "THINKING:" in response:
        thinking_start = response.index("THINKING:") + len("THINKING:")
        if "QUESTIONS:" in response:
            thinking = response[thinking_start:response.index("QUESTIONS:")].strip()
            questions = response[response.index("QUESTIONS:") + len("QUESTIONS:"):].strip()
        elif "READY_TO_PLAN" in response:
            thinking = response[thinking_start:response.index("READY_TO_PLAN")].strip()
        else:
            thinking = response[thinking_start:].strip()
    else:
        questions = response.strip()

    return thinking, questions, ready


def run_brainstorm_loop(goal: str, llm: OllamaLLM) -> str:
    """Ask clarifying questions until the model has enough context, then return Q&A history."""
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

# ─── Commands ─────────────────────────────────────────────────────────────────

COMMANDS = {
    "/help":  "Show available commands",
    "/model": "Switch the AI model",
    "/new":   "Start a new goal (clears current session)",
    "/save":  "Save the current plan to a markdown file",
    "/clear": "Clear the screen",
    "/exit":  "Exit",
}


def show_help() -> None:
    console.print()
    table = Table(show_header=False, box=None, pad_edge=False, padding=(0, 2))
    table.add_column("cmd", style="bold cyan", width=10)
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

# ─── Welcome ──────────────────────────────────────────────────────────────────

def show_welcome() -> None:
    console.print()
    console.print(Rule("[bold cyan]Goal Planner[/bold cyan]", style="cyan"))
    console.print()
    console.print("  [dim]Describe any goal and get a structured, actionable plan[/dim]")
    console.print("  [dim]after a quick AI-powered brainstorm. Ask follow-up questions[/dim]")
    console.print("  [dim]after your plan — the session stays alive.[/dim]")
    console.print()
    console.print("  Type [cyan]/help[/cyan] for commands.")
    console.print()

# ─── Main REPL ────────────────────────────────────────────────────────────────

def main() -> None:
    show_welcome()
    model_name = pick_model()
    llm = OllamaLLM(model=model_name)

    # Session state
    goal = ""
    context = ""
    plan_text = ""
    conversation: list[str] = []

    console.print(Rule(style="dim"))
    console.print()

    while True:
        # Prompt changes once we have an active plan (chat mode)
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
                    console.print("\n  [yellow]No plan to save yet. Enter a goal first.[/yellow]\n")
                else:
                    save_plan(goal, plan_text)

            else:
                console.print(f"\n  [red]Unknown command:[/red] {cmd}   (try /help)\n")

            continue

        # ── Follow-up conversation (plan already exists) ─────────────────────
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
            console.print(f"  [dim]◆ ask another question  ·  /save  ·  /new  ·  /model  ·  /exit[/dim]")
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
            console.print(f"  [dim]Model: {model_name}  ·  /save to export  ·  /new for another goal  ·  ask a follow-up below[/dim]")
            console.print()

        except Exception as err:
            console.print(f"\n  [yellow]Error: {err}[/yellow]\n")
            goal = ""


if __name__ == "__main__":
    main()
