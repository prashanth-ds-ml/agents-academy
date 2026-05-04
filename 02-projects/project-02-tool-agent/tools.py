import datetime
import subprocess
from pathlib import Path

# Tools that run automatically (read-only, no side effects)
SAFE_TOOLS = {"get_time", "read_file", "list_files"}

# Tools that require user confirmation before running
CONFIRM_TOOLS = {"write_file", "create_folder", "run_shell"}


def get_time() -> str:
    """Return the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_file(path: str) -> str:
    """Read and return the contents of a text file."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Error reading {path}: {e}"


def list_files(path: str = ".") -> str:
    """List files and folders in a directory."""
    try:
        p = Path(path)
        if not p.exists():
            return f"Path does not exist: {path}"
        items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
        return "\n".join(
            f"{'📁' if item.is_dir() else '📄'} {item.name}" for item in items
        ) or "(empty directory)"
    except Exception as e:
        return f"Error listing {path}: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file, creating parent directories if needed."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"✓ Written {len(content)} chars to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"


def create_folder(path: str) -> str:
    """Create a folder (and any missing parent folders)."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return f"✓ Folder created: {path}"
    except Exception as e:
        return f"Error creating folder {path}: {e}"


def run_shell(cmd: str) -> str:
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        output = (result.stdout + result.stderr).strip()
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "Command timed out after 30s"
    except Exception as e:
        return f"Error running command: {e}"


TOOL_MAP = {
    "get_time": get_time,
    "read_file": read_file,
    "list_files": list_files,
    "write_file": write_file,
    "create_folder": create_folder,
    "run_shell": run_shell,
}
