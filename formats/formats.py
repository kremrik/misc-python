__all__ = ["Colors", "Styles"]


CLR = "0"
FMT_CHARS = "\033["
COLORS = {
    "black": "30",
    "red": "31",
    "green": "32",
    "brown": "33",
    "blue": "34",
    "purple": "35",
    "cyan": "36",
    "light_gray": "37",
}
STYLES = {
    "bold": "1",
    "underline": "4",
    "reverse_video": "7",
}


def format_factory(cls_name: str, fmt_map: dict) -> type:
    methods = {
        name: (lambda txt, code=code: apply(code, txt))
        for name, code in fmt_map.items()
    }

    obj = type(cls_name, (object,), methods)
    return obj


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


Colors = format_factory("Colors", COLORS)
Styles = format_factory("Styles", STYLES)
