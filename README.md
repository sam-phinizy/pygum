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

So `pygum.ginput` will have the following docstring:

```text
    Get user entered input
    Args:
        placeholder:Placeholder value
        prompt:Prompt to display
        value:Initial value
        char_limit: Maximum value length (0 for no limit)
        width: Input width
        password: If true mask input characters
        detailed:If False return string, if True return CmdOutput
```

## Todo

- Tests
- Style attributes
