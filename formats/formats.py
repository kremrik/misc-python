from enum import Enum


__all__ = ["Colors", "Styles"]


BLACK = "30"
RED = "31"
GREEN = "32"
BROWN = "33"
BLUE = "34"
PURPLE = "35"
CYAN = "36"
LIGHT_GRAY = "37"

BOLD = "1"
UNDERLINE = "4"
REVERSE_VIDEO = "7"

CLR = "0"

FMT_CHARS = "\033["


class Colors(Enum):
    black = lambda txt: apply(BLACK, txt)
    red = lambda txt: apply(RED, txt)
    green = lambda txt: apply(GREEN, txt)
    brown = lambda txt: apply(BROWN, txt)
    blue = lambda txt: apply(BLUE, txt)
    purple = lambda txt: apply(PURPLE, txt)
    cyan = lambda txt: apply(CYAN, txt)
    light_gray = lambda txt: apply(LIGHT_GRAY, txt)


class Styles(Enum):
    bold = lambda txt: apply(BOLD, txt)
    underline = lambda txt: apply(UNDERLINE, txt)
    reverse_video = lambda txt: apply(REVERSE_VIDEO, txt)


def apply(f: str, txt: str) -> str:
    if _is_formatted(txt):
        return _add_format(f, txt)

    bgn = _fmt(f)
    end = _fmt(CLR)
    return f"{bgn}{txt}{end}"


def _is_formatted(txt: str) -> bool:
    return FMT_CHARS in txt


def _fmt(f: str) -> str:
    return f"{FMT_CHARS}{f}m"


def _add_format(f: str, txt: str) -> str:
    parts = txt.split(FMT_CHARS)
    parts[1] = f"{f};{parts[1]}"
    return FMT_CHARS.join(parts)
