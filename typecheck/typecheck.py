from dataclasses import dataclass, field
from functools import lru_cache
from inspect import getfullargspec, FullArgSpec
from typing import Any, Callable, Optional
from warnings import warn


@dataclass(frozen=True)
class Args:
    name: str
    values: list = field(default_factory=list)


@dataclass(frozen=True)
class Kwargs:
    name: str
    values: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Input:
    args: dict = field(default_factory=dict)
    varargs: Args = None
    kwonlyargs: dict = field(default_factory=dict)
    varkw: Kwargs = None


class TypeCheckError(TypeError):
    pass


# ---------------------------------------------------------
def check_types(values: Input, typehints: dict) -> None:
    if not typehints:
        return True

    errors = []
    if errors:
        msg = "\n".join(
            [
                f"Param {p} expected {typehints[p]} given {values[p]}"
                for p in errors
            ]
        )
        raise TypeCheckError(msg)

    return True


def check_type(value: Any, typehint) -> bool:
    if isinstance(typehint, type):
        return _pyobject_validator(value, typehint)
    else:
        msg = f"Type check for {typehint} is not yet supported, ignoring"
        warn(msg)
        return True


def _pyobject_validator(
    value: Any, typehint: type
) -> Callable:
    return isinstance(value, typehint)


# ---------------------------------------------------------
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
    output = {
        "args": {},
        "varargs": None,
    }

    s_args = spec.args
    s_varargs = spec.varargs
    s_req_args = s_args

    defaults = _default_args_map(spec)
    if defaults:
        output["args"].update(defaults)
        pos = len(defaults)
        s_req_args = s_args[pos:]

    err_msg = f"Callable takes positional argument(s) {s_args}, but was given {args}"

    if not args and s_req_args:
        raise TypeCheckError(err_msg)
    elif not args and not s_req_args:
        return output

    if len(args) < len(s_req_args):
        raise TypeCheckError(err_msg)

    if len(args) > len(s_args) and not s_varargs:
        raise TypeCheckError(err_msg)

    if len(s_req_args) <= len(args) <= len(s_args):
        o_args = dict(zip(s_args, args))
        output["args"].update(o_args)
        return output

    if len(args) > len(s_args) and s_varargs:
        cutoff = len(s_args)
        o_args = dict(zip(s_args, args[:cutoff]))
        o_varargs = Args(
            name=s_varargs, values=list(args[cutoff:])
        )
        output["args"].update(o_args)
        output["varargs"] = o_varargs
        return output


def _default_args_map(spec: FullArgSpec) -> dict:
    defaults = spec.defaults
    if not defaults:
        return {}

    args = spec.args
    pos = len(defaults)
    default_args = args[pos:] or args
    default_vals = defaults

    return dict(zip(default_args, default_vals))


def process_kwargs(
    spec: FullArgSpec, kwargs: Optional[dict]
) -> dict:
    output = {
        "kwonlyargs": {},
        "varkw": None,
    }

    s_kwonlyargs = spec.kwonlyargs
    s_varkw = spec.varkw
    req_s_kwonlyargs = s_kwonlyargs

    defaults = _default_kwargs_map(spec)
    if defaults:
        output["kwonlyargs"].update(defaults)
        req_s_kwonlyargs = [
            a for a in s_kwonlyargs if a not in defaults
        ]

    err_msg = f"Callable takes keyword argument(s) {s_kwonlyargs}, but was given {kwargs}"

    if not kwargs and req_s_kwonlyargs:
        raise TypeCheckError(err_msg)
    elif not kwargs and not req_s_kwonlyargs:
        return output

    missing = list(set(req_s_kwonlyargs) - set(kwargs))
    extra = list(set(kwargs) - set(s_kwonlyargs))

    if missing:
        raise TypeCheckError(err_msg)

    if not missing and not extra:
        output["kwonlyargs"].update(kwargs)
        return output

    if extra and not s_varkw:
        raise TypeCheckError(err_msg)

    if extra and s_varkw:
        o_kwonlyargs = {
            k: v
            for k, v in kwargs.items()
            if k in s_kwonlyargs
        }
        o_varkw = Kwargs(
            name=s_varkw,
            values={
                k: v
                for k, v in kwargs.items()
                if k in extra
            },
        )
        output["kwonlyargs"].update(o_kwonlyargs)
        output["varkw"] = o_varkw
        return output


def _default_kwargs_map(spec: FullArgSpec) -> dict:
    defaults = spec.kwonlydefaults
    if not defaults:
        return {}
    return defaults


# ---------------------------------------------------------
@lru_cache(maxsize=None)
def get_fnc_spec(fnc: Callable) -> FullArgSpec:
    return getfullargspec(fnc)
