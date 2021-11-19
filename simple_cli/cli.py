from formats import Colors, Styles

from dataclasses import dataclass
from typing import Callable, List, Optional


__all__ = ["Arg", "cli"]


HELP_ARGS = ["-h", "--help"]


@dataclass
class Arg:
    arg: str
    callback: Callable[[], None]
    help: str


def cli(
    cli_args: List[str],
    opts: List[Arg],
    description: Optional[str] = None,
) -> None:
    hlp = generate_help(opts, description)

    if not cli_args:
        print(hlp)
        exit(0)

    for d in HELP_ARGS:
        if d in cli_args:
            print(hlp)
            exit(0)

    arg_names = [a.arg for a in opts]
    bad_args = list(set(cli_args) - set(arg_names))
    if bad_args:
        msg = Colors.red(
            f"Incorrect argument(s): {bad_args}"
        )  # type: ignore
        print(msg)
        exit(1)

    arg = cli_args[0]
    callback = [o for o in opts if o.arg == arg][
        0
    ].callback

    return callback()


def generate_help(
    args: List[Arg], description: Optional[str]
) -> str:
    help_arg = Arg(
        "-h/--help", lambda: None, "Print help and exit"
    )
    args.append(help_arg)

    header = Styles.bold("COMMANDS")  # type: ignore

    if description:
        desc = generate_description(description) + "\n\n"
    else:
        desc = ""

    hlp = "\n".join(map(_format_argument, args))
    output = desc + header + "\n" + hlp
    return output


def generate_description(description: str) -> str:
    header = Styles.bold("DESCRIPTION")  # type: ignore
    output = f"{header}\n    {description}"
    return output


def _format_argument(arg: Arg) -> str:
    opt = Styles.bold(arg.arg)  # type: ignore
    hlp = arg.help
    output = f"    {opt}\n        {hlp}"
    return output
