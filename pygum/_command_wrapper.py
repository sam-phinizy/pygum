from subprocess import CalledProcessError, check_output
from typing import List


class CmdOutput:
    def __init__(self, msg: str, status: int, cmd: List[str]) -> None:
        self.msg = str(msg).strip()
        self.status = status
        self.command: List[str] = cmd

    @property
    def failed(self):
        return self.status != 0

    @failed.setter
    def failed(self, _):
        pass

    @property
    def success(self):
        return self.status == 0

    @success.setter
    def success(self, _):
        pass


def command_wrapper(command: List[str]) -> CmdOutput:
    """A simple wrapper around check_checkpout"""
    try:
        cmd_joined = " ".join(command)
        cmd_output = check_output(cmd_joined, shell=True)
    except CalledProcessError as e:
        return CmdOutput(e.output, e.returncode, command)

    return CmdOutput(cmd_output.decode("utf-8"), 0, command)
