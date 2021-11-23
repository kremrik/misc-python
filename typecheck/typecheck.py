from dataclasses import dataclass, field
from inspect import getfullargspec, FullArgSpec
from typing import Callable, Optional


@dataclass(frozen=True)
class Input:
    args: dict = field(default_factory=dict)
    varargs: list = field(default_factory=list)
    kwonlyargs: dict = field(default_factory=dict)
    varkw: dict = field(default_factory=dict)


class TypeCheckError(TypeError):
    pass


def parse_inputs(
    fnc: Callable,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> Input:
    spec = get_fnc_spec(fnc)

    args_and_varargs = process_args(spec, args)
    kwonlyargs_and_varkw = process_kwargs(spec, kwargs)

    all_inputs = {
        **args_and_varargs,
        **kwonlyargs_and_varkw,
    }

    return Input(**all_inputs)


def process_args(
    spec: FullArgSpec, args: Optional[tuple]
) -> dict:
    s_args = spec.args
    s_varargs = spec.varargs

    output = {
        "args": {},
        "varargs": [],
    }

    err_msg = f"Callable takes positional argument(s) {s_args}, but was given {args}"

    if not args and s_args:
        raise TypeCheckError(err_msg)
    elif not args and not s_args:
        return output

    if len(args) < len(s_args):
        raise TypeCheckError(err_msg)

    if len(args) == len(s_args):
        output["args"] = dict(zip(s_args, args))
        return output

    if len(args) > len(s_args) and not s_varargs:
        raise TypeCheckError(err_msg)

    if len(args) > len(s_args) and s_varargs:
        cutoff = len(s_args)
        o_args = dict(zip(s_args, args[:cutoff]))
        o_varargs = list(args[cutoff:])
        output["args"] = o_args
        output["varargs"] = o_varargs
        return output


def process_kwargs(
    spec: FullArgSpec, kwargs: Optional[dict]
) -> dict:
    s_kwonlyargs = spec.kwonlyargs
    s_varkw = spec.varkw

    output = {
        "kwonlyargs": {},
        "varkw": {},
    }

    err_msg = f"Callable takes keyword argument(s) {s_kwonlyargs}, but was given {kwargs}"

    if not kwargs and s_kwonlyargs:
        raise TypeCheckError(err_msg)
    elif not kwargs and not s_kwonlyargs:
        return output

    missing = list(set(s_kwonlyargs) - set(kwargs))
    extra = list(set(kwargs) - set(s_kwonlyargs))

    if missing:
        raise TypeCheckError(err_msg)

    if not missing and not extra:
        output["kwonlyargs"] = kwargs
        return output

    if extra and not s_varkw:
        raise TypeCheckError(err_msg)

    if extra and s_varkw:
        o_kwonlyargs = {
            k: v
            for k, v in kwargs.items()
            if k in s_kwonlyargs
        }
        o_varkw = {
            k: v for k, v in kwargs.items() if k in extra
        }
        output["kwonlyargs"] = o_kwonlyargs
        output["varkw"] = o_varkw
        return output


# ---------------------------------------------------------
def get_fnc_spec(fnc: Callable) -> FullArgSpec:
    return getfullargspec(fnc)
