from enum import Enum
from typing import List, Union


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


class Colors(Enum):
    black = lambda txt: fmt(BLACK, txt)
    red = lambda txt: fmt(RED, txt)
    green = lambda txt: fmt(GREEN, txt)
    brown = lambda txt: fmt(BROWN, txt)
    blue = lambda txt: fmt(BLUE, txt)
    purple = lambda txt: fmt(PURPLE, txt)
    cyan = lambda txt: fmt(CYAN, txt)
    light_gray = lambda txt: fmt(LIGHT_GRAY, txt)


class Styles(Enum):
    bold = lambda txt:fmt(BOLD, txt)
    underline = lambda txt: fmt(UNDERLINE, txt)
    reverse_video = lambda txt: fmt(REVERSE_VIDEO, txt)


class FormattedText:
    def __init__(self, code: List[str], text: str) -> None:
        self.code = code
        self.text = text

    def __str__(self) -> str:
        code = ";".join(self.code)
        text = self.text
        return f"\033[{code}m{text}\033[{CLR}"

    def __repr__(self) -> str:
        return self.__str__()


def fmt(f, txt: Union[str, FormattedText]):
    if isinstance(txt, str):
        return FormattedText([f], txt)
    
    text = txt.text
    code = txt.code
    code.append(f)
    return FormattedText(code, text)
