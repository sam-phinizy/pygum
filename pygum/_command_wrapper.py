import subprocess
from typing import List, Optional


class CmdOutput:
    def __init__(self, msg: str, status: int, cmd: List[str]) -> None:
        self.msg = str(msg).strip()
        self.status = status
        self.command: List[str] = cmd

    @property
    def failed(self) -> bool:
        return self.status != 0

    @property
    def success(self) -> bool:
        return self.status == 0


def command_wrapper(command: List[str], stdin_data: Optional[str] = None) -> CmdOutput:
    """Executes a command using subprocess.run, optionally passing stdin."""
    try:
        process = subprocess.run(
            command,
            input=stdin_data.encode('utf-8') if stdin_data else None,
            capture_output=True,
            check=False,  # Handle non-zero exits manually
            text=False  # Get bytes for stdout/stderr
        )
        stdout = process.stdout.decode('utf-8', errors='replace')
        stderr = process.stderr.decode('utf-8', errors='replace')

        # Prioritize stdout; if empty, use stderr.
        # This mirrors how e.output might have behaved (containing either stdout or stderr).
        output_msg = stdout if stdout else stderr
        
        return CmdOutput(output_msg, process.returncode, command)

    except Exception as e:
        # Fallback for unexpected errors during subprocess execution (e.g., command not found)
        # Note: subprocess.run with check=False and capture_output=True should be quite robust
        # and typically not raise for many common issues like non-zero exit codes.
        # FileNotFoundError (if command[0] is not found) is a primary candidate here.
        return CmdOutput(str(e), -1, command) # Using -1 as a generic error status
