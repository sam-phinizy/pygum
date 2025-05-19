# pygum
A Python wrapper around [Gum](https://github.com/charmbracelet/gum). This lets you use Gum for Python shell script and getting input, filtering choices and confirming choices etc.

It currently supports the following subcommands:
- input as `pygum.ginput`
- choose
- filter
- write
- confirm


## Docs

### Installation

To install just use pip/poetry/pdm:

#### [Pip](https://pip.pypa.io/en/stable/cli/pip_install/)
`pip install pygum`

#### [Poetry](https://python-poetry.org/docs/cli/#add)
`poetry add pygum`

#### [PDM](https://pdm.fming.dev/latest/usage/dependency/)
`pdm add pygum`



### How to use

```python
import pygum
choice = pygum.choose(["First Choice","Second Choice","Third Choice"])
print(f"You chose: {choice}")
```

Each command mirrors the command line arguments/flags for the respective `Gum` command. For example `gum input` has the following help:

```text
Usage: gum input

Prompt for some input

Flags:
  -h, --help                               Show context-sensitive help.
  -v, --version                            Print the version number

      --placeholder="Type something..."    Placeholder value ($GUM_INPUT_PLACEHOLDER)
      --prompt="> "                        Prompt to display ($GUM_INPUT_PROMPT)
      --value=""                           Initial value (can also be passed via stdin)
      --char-limit=400                     Maximum value length (0 for no limit)
      --width=40                           Input width ($GUM_INPUT_WIDTH)
      --password                           Mask input characters

```

The `pygum.ginput` (note: it's ginput not input to avoid shadowing) function exposes each of these as kwargs. In addition each function has a 'detailed' kwarg. If `False` it'll just return the parsed text, if `True` it returns the command argument.

### Style Attributes and Other Flags

`pygum` allows you to pass arbitrary `gum` styling flags (and other flags not explicitly defined as parameters in the Python functions) directly as keyword arguments. This provides flexibility to use all of `gum`'s styling capabilities.

The convention for these flags is:
- Python keyword arguments with double underscores (`__`) are translated into `gum` flags with dots (`.`). For example, `prompt__foreground="#FFA500"` becomes `--prompt.foreground "#FFA500"`.
- Python keyword arguments with single underscores (`_`) are translated into `gum` flags with hyphens (`-`). For example, `char_limit=10` becomes `--char-limit 10`.
- If a flag is a boolean `True` (e.g., `prompt__bold=True`), it's passed as just the flag (e.g., `--prompt.bold`). If `False`, the flag is omitted.

**Examples:**

```python
import pygum

# Example for ginput with style attributes
user_input = pygum.ginput(
    prompt="Enter value:",
    placeholder="type here...",
    # Style attributes for the prompt itself
    prompt__foreground="magenta", # Sets --prompt.foreground
    prompt__bold=True,            # Sets --prompt.bold
    # Style attributes for the cursor
    cursor__foreground="cyan"     # Sets --cursor.foreground
)
print(f"You entered: {user_input}")

# Example for choose with style attributes
choice = pygum.choose(
    ["Option 1", "Option 2"],
    header="Select an option:",
    header__foreground="blue",        # Sets --header.foreground
    selected__foreground="green",     # Sets --selected.foreground
    cursor__align="left"              # Sets --cursor.align
)
print(f"You chose: {choice}")
```

So `pygum.ginput` will have the following docstring:

```text
    Get user entered input
    Args:
        placeholder: Placeholder value.
        prompt: Prompt to display.
        value: Initial value.
        char_limit: Maximum value length (0 for no limit).
        width: Input width.
        password: If true mask input characters.
        detailed: Optional. If False (default), returns the string output.
                 If True, returns the full CmdOutput object.
                 Returns None if the command fails and produces no message.
        **kwargs: Additional keyword arguments for gum flags, including style attributes
                 (e.g., `prompt__foreground="red"`, `cursor__bold=True`).

    Returns:
        Union[str, CmdOutput, None]: The user's input as a string (if detailed=False),
                                     or a CmdOutput object (if detailed=True),
                                     or None if the operation is cancelled or fails
                                     without a message.
```

## Todo

(All major todos completed!)
