from typing import List, Optional, Union

from pygum._command_wrapper import CmdOutput, command_wrapper


def _gum_runner(
    command: str,
    choices: Optional[str] = None,
    detailed: Optional[bool] = False,
    **kwargs,
) -> Union[CmdOutput, str, None]:

    if command != "filter":
        cmd_args: List[str] = ["gum", command]
    else:
        cmd_args = ["echo", f"'{choices}'", "|", "gum", command]

    for k, v in kwargs.items():
        if v is None:
            continue
        k = k.replace("_", "-")
        cmd_args.append(f"--{k}")
        cmd_args.append(str(v))
    if command != "filter" and choices:
        cmd_args.append(choices)

    result = command_wrapper(cmd_args)

    if detailed:
        return result
    else:
        return result.msg or None


def input(
    placeholder: Optional[str] = None,
    prompt: Optional[str] = None,
    value: Optional[str] = None,
    char_limit: Optional[int] = None,
    width: Optional[int] = None,
    password: Optional[bool] = None,
    detailed: Optional[bool] = False,
) -> CmdOutput:
    """Runs gum input"""

    return _gum_runner(
        "input",
        placeholder=placeholder,
        prompt=prompt,
        char_limit=char_limit,
        value=value,
        width=width,
        password=password,
        detailed=detailed,
    )


def choose(
    choices: List[str],
    *,
    height: Optional[int] = None,
    cursor: Optional[str] = None,
    cursor_prefix: Optional[str] = None,
    selected_prefix: Optional[str] = None,
    unselected_prefix: Optional[str] = None,
    limit: Optional[int] = None,
    no_limit: Optional[bool] = None,
    detailed: Optional[bool] = False,
) -> CmdOutput:
    """Runs gum choice"""
    joined_choices = " ".join(f'"{str(c)}"' for c in choices)
    return _gum_runner(
        "choose",
        choices=joined_choices,
        height=height,
        cursor=cursor,
        cursor_prefix=cursor_prefix,
        selected_prefix=selected_prefix,
        unselected_prefix=unselected_prefix,
        limit=limit,
        no_limit=no_limit,
        detailed=detailed,
    )


def filter(
    choices: List[str],
    *,
    indicator: Optional[str] = None,
    placeholder: Optional[str] = None,
    prompt: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    detailed: Optional[bool] = False,
) -> CmdOutput:
    joined_choices = "\n".join(f"{str(c)}" for c in choices)

    return _gum_runner(
        "filter",
        choices=joined_choices,
        indicator=indicator,
        placeholder=placeholder,
        prompt=prompt,
        width=width,
        height=height,
        detailed=detailed,
    )


def write(
    width: Optional[int] = None,
    height: Optional[int] = None,
    placeholder: Optional[str] = None,
    prompt: Optional[str] = None,
    show_cursor_line: Optional[bool] = None,
    show_line_numbers: Optional[bool] = None,
    value: Optional[str] = None,
    char_limit: Optional[int] = None,
    detailed: Optional[bool] = False,
) -> CmdOutput:
    return _gum_runner(
        "write",
        width=width,
        height=height,
        placeholder=placeholder,
        prompt=prompt,
        show_cursor_line=show_cursor_line,
        show_line_numbers=show_line_numbers,
        value=value,
        char_limit=char_limit,
        detailed=detailed,
    )
