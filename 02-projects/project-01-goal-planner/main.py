MODEL_LABEL = "None (Lesson 1 uses a rule-based planner, not Ollama)"


def build_plan(goal: str) -> str:
    goal = goal.strip()
    if not goal:
        return "Please enter a goal."

    objective = f"Clarify what success looks like for: {goal}"
    steps = [
        "Restate the goal in simple words",
        "Break the goal into 3 small actions",
        "Identify one likely obstacle",
        "Choose the next concrete action",
    ]
    risks = [
        "The goal may be too broad",
        "Missing constraints may lead to weak plans",
    ]
    constraints = [
        "Keep the first version small and clear",
        "Avoid adding too many features at once",
    ]
    next_action = "Write one sentence describing the very first thing to do today"

    lowered_goal = goal.lower()

    if "file organizer" in lowered_goal or "organize files" in lowered_goal:
        objective = "Create a local tool that organizes files safely inside one chosen folder"
        steps = [
            "Inspect the folder structure and note the kinds of files present",
            "Decide categories such as documents, images, code, and archives",
            "Define safe move rules for each category",
            "Test the rules on a small sample before organizing everything",
        ]
        risks = [
            "Files could be moved into the wrong folder",
            "Rules may be unclear for mixed or duplicate file types",
        ]
        constraints = [
            "Only work inside one local root folder",
            "Avoid renaming or moving system files",
            "Keep a review step before large changes",
        ]
        next_action = "List 3 file categories and the file extensions that belong in each one"
    elif "snake" in lowered_goal and "game" in lowered_goal:
        objective = "Build a small playable Snake game with clear controls and restart flow"
        steps = [
            "Choose the game library and create a tiny project structure",
            "Implement movement, food spawning, and score tracking",
            "Add wall collision, self collision, and game over handling",
            "Test the loop and write short run instructions",
        ]
        risks = [
            "Game state logic may get messy if everything is written in one block",
            "Input handling and collision rules may be buggy at first",
        ]
        constraints = [
            "Keep the first version simple and playable",
            "Use minimal dependencies",
            "Focus on one working game loop before polish",
        ]
        next_action = "Choose the library for the first version and list the core game components"
    elif "expense" in lowered_goal or "budget" in lowered_goal or "finance" in lowered_goal:
        objective = "Create a simple system for tracking money clearly and consistently"
        steps = [
            "List the main categories like income, subscriptions, travel, rent, and savings",
            "Decide where the data will be stored",
            "Design how entries will be added and summarized",
            "Test the system with one week of sample data",
        ]
        risks = [
            "Expense categories may overlap and confuse reporting",
            "Manual entry may become inconsistent over time",
        ]
        constraints = [
            "Keep categories easy to understand",
            "Start with manual entry before automation",
            "Make totals easy to verify",
        ]
        next_action = "Write down the first 5 categories you want to track"

    steps_text = "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))
    risks_text = "\n".join(f"- {risk}" for risk in risks)
    constraints_text = "\n".join(f"- {constraint}" for constraint in constraints)

    return f"""GOAL PLANNER

Model:
- {MODEL_LABEL}

Objective:
- {objective}

Steps:
{steps_text}

Risks:
{risks_text}

Constraints:
{constraints_text}

Next action:
- {next_action}
"""


def main() -> None:
    goal = input("Enter a goal: ")
    print()
    print(build_plan(goal))


if __name__ == "__main__":
    main()
