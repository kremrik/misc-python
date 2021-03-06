from typecheck.typecheck import (
    check_types,
    parse_inputs,
    typecheck,
    Input,
    Args,
    Kwargs,
    TypeCheckError,
)

import unittest
from typing import List, Optional, Union


class test_typecheck(unittest.TestCase):
    def test_ignores_without_hints(self):
        @typecheck
        def fnc(a):
            pass

        with self.subTest("int value"):
            self.assertIsNone(fnc(1))
        with self.subTest("str value"):
            self.assertIsNone(fnc("1"))

    def test_args(self):
        @typecheck
        def fnc(a: int):
            pass

        self.assertIsNone(fnc(1))

    def test_args_with_default(self):
        @typecheck
        def fnc(a: int, b: int = 2):
            pass

        self.assertIsNone(fnc(1))

    def test_args_varargs(self):
        @typecheck
        def fnc(a: int, *args: str):
            pass

        self.assertIsNone(fnc(1, "hi"))

    def test_args_no_varargs(self):
        @typecheck
        def fnc(a: int, *args: str):
            pass

        self.assertIsNone(fnc(1))

    def test_args_kwonlyargs(self):
        @typecheck
        def fnc(a: int, *, b: float):
            pass

        self.assertIsNone(fnc(1, b=3.14))

    def test_args_varargs_kwonlyargs(self):
        @typecheck
        def fnc(a: int, *args: str, b: float):
            pass

        self.assertIsNone(fnc(1, "hi", b=3.14))

    def test_args_varargs_kwonlyargs_with_default(self):
        @typecheck
        def fnc(
            a: int, *args: str, b: float, c: str = "hi"
        ):
            pass

        self.assertIsNone(fnc(1, "hi", b=3.14))

    def test_args_varargs_kwonlyargs_varkw(self):
        @typecheck
        def fnc(
            a: int, *args: str, b: float, **kwargs: bytes
        ):
            pass

        self.assertIsNone(fnc(1, "hi", b=3.14, c=b"1"))

    def test_optional(self):
        @typecheck
        def fnc(a: Optional[int] = None):
            pass

        self.assertIsNone(fnc(1))
        self.assertIsNone(fnc())

    def test_union(self):
        @typecheck
        def fnc(a: Union[int, float] = None):
            pass

        self.assertIsNone(fnc(1))
        self.assertIsNone(fnc(1.1))

    def test_generic_list(self):
        @typecheck
        def fnc(a: list):
            pass

        self.assertIsNone(fnc([1, 2]))
        self.assertIsNone(fnc(["a", "b"]))

    def test_hint_list(self):
        @typecheck
        def fnc(a: List[int]):
            pass

        self.assertIsNone(fnc([1, 2]))


class test_typecheck_exceptions(unittest.TestCase):
    def test_missing_args(self):
        @typecheck
        def fnc(a: int):
            pass

        with self.assertRaises(TypeCheckError):
            fnc()

    def test_missing_kwonlyargs(self):
        @typecheck
        def fnc(a: int, *args, b: float):
            pass

        with self.assertRaises(TypeCheckError):
            fnc(1)

    def test_wrong_optional_type(self):
        @typecheck
        def fnc(a: Optional[str] = None):
            pass

        with self.assertRaises(TypeCheckError):
            fnc(1)

    def test_wrong_list_element(self):
        @typecheck
        def fnc(a: List[str] = None):
            pass

        with self.assertRaises(TypeCheckError):
            fnc(["a", "b", 3])


# implementation tests below
# =========================================================
class test_check_types_happy_path(unittest.TestCase):
    def test_no_values_no_typehints(self):
        values = Input()
        typehints = {}
        expect = None
        actual = check_types(values, typehints)
        self.assertEqual(expect, actual)

    def test_values_no_typehints(self):
        values = Input(args={"x": 1})
        typehints = {}
        expect = None
        actual = check_types(values, typehints)
        self.assertEqual(expect, actual)

    def test_values_and_typehints(self):
        values = Input(
            args={"a": 1, "b": 2.0},
            varargs=Args(
                name="args", values=["hi", "hello"]
            ),
            kwonlyargs={"c": 3, "d": b"4"},
            varkw=Kwargs(
                name="kwargs", values={"e": 5, "f": 6}
            ),
        )
        typehints = {
            "a": int,
            "b": float,
            "args": str,
            "c": int,
            "d": bytes,
            "kwargs": int,
        }
        expect = None
        actual = check_types(values, typehints)
        self.assertEqual(expect, actual)


class test_check_types_exceptions(unittest.TestCase):
    def test_missing_positional_arg(self):
        values = Input(args={"x": 1})
        typehints = {"x": float}
        with self.assertRaises(TypeCheckError):
            check_types(values, typehints)


# ---------------------------------------------------------
class test_parse_inputs_happy_path(unittest.TestCase):
    def test_no_params(self):
        def fnc():
            pass

        expect = Input()
        actual = parse_inputs(fnc)
        self.assertEqual(expect, actual)

    def test_one_arg(self):
        def fnc(x):
            pass

        expect = Input(args={"x": 1})
        actual = parse_inputs(fnc, args=[1])
        self.assertEqual(expect, actual)

    def test_mult_arg(self):
        def fnc(x, y, z):
            pass

        expect = Input(args={"x": 1, "y": 2, "z": 3})
        actual = parse_inputs(fnc, args=[1, 2, 3])
        self.assertEqual(expect, actual)

    def test_one_varargs(self):
        def fnc(*args):
            pass

        expect = Input(
            varargs=Args(name="args", values=[1])
        )
        actual = parse_inputs(fnc, args=[1])
        self.assertEqual(expect, actual)

    def test_mult_varargs(self):
        def fnc(*args):
            pass

        expect = Input(
            varargs=Args(name="args", values=[1, 2, 3])
        )
        actual = parse_inputs(fnc, args=[1, 2, 3])
        self.assertEqual(expect, actual)

    def test_args_and_varargs(self):
        def fnc(x, y, *args):
            pass

        expect = Input(
            args={"x": 1, "y": 2},
            varargs=Args(name="args", values=[3, 4]),
        )
        actual = parse_inputs(fnc, args=[1, 2, 3, 4])
        self.assertEqual(expect, actual)

    def test_one_kwonlyargs(self):
        def fnc(*, x):
            pass

        expect = Input(kwonlyargs={"x": 1})
        actual = parse_inputs(fnc, kwargs={"x": 1})
        self.assertEqual(expect, actual)

    def test_mult_kwonlyargs(self):
        def fnc(*, x, y, z):
            pass

        expect = Input(kwonlyargs={"x": 1, "y": 2, "z": 3})
        actual = parse_inputs(
            fnc, kwargs={"x": 1, "y": 2, "z": 3}
        )
        self.assertEqual(expect, actual)

    def test_one_varkw(self):
        def fnc(**kwargs):
            pass

        expect = Input(
            varkw=Kwargs(name="kwargs", values={"x": 1})
        )
        actual = parse_inputs(fnc, kwargs={"x": 1})
        self.assertEqual(expect, actual)

    def test_mult_varkw(self):
        def fnc(**kwargs):
            pass

        expect = Input(
            varkw=Kwargs(
                name="kwargs",
                values={"x": 1, "y": 2, "z": 3},
            )
        )
        actual = parse_inputs(
            fnc, kwargs={"x": 1, "y": 2, "z": 3}
        )
        self.assertEqual(expect, actual)

    def test_kwonlyargs_and_varkw(self):
        def fnc(*, i, j, **kwargs):
            pass

        expect = Input(
            kwonlyargs={"i": -1, "j": 0},
            varkw=Kwargs(
                name="kwargs", values={"x": 1, "y": 2}
            ),
        )
        actual = parse_inputs(
            fnc, kwargs={"i": -1, "j": 0, "x": 1, "y": 2}
        )
        self.assertEqual(expect, actual)

    def test_one_default_arg(self):
        def fnc(x=None):
            pass

        expect = Input(args={"x": None})
        actual = parse_inputs(fnc)
        self.assertEqual(expect, actual)

    def test_mult_default_arg(self):
        def fnc(x=1, y=2, z=3):
            pass

        expect = Input(args={"x": 1, "y": 2, "z": 3})
        actual = parse_inputs(fnc)
        self.assertEqual(expect, actual)

    def test_one_arg_one_default_arg(self):
        def fnc(x, y=None):
            pass

        expect = Input(args={"x": 1, "y": None})
        actual = parse_inputs(fnc, args=(1,))
        self.assertEqual(expect, actual)

    def test_one_default_kwonlyargs(self):
        def fnc(*, x=None):
            pass

        expect = Input(kwonlyargs={"x": None})
        actual = parse_inputs(fnc)
        self.assertEqual(expect, actual)

    def test_mult_default_kwonlyargs(self):
        def fnc(*, x=1, y=2, z=3):
            pass

        expect = Input(kwonlyargs={"x": 1, "y": 2, "z": 3})
        actual = parse_inputs(fnc)
        self.assertEqual(expect, actual)

    def test_one_kwonlyargs_one_default_kwonlyargs(self):
        def fnc(*, x, y=2):
            pass

        expect = Input(kwonlyargs={"x": 1, "y": 2})
        actual = parse_inputs(fnc, kwargs={"x": 1})
        self.assertEqual(expect, actual)

    def test_everything(self):
        def fnc(a, b, *args, c, d=4, **kwargs):
            pass

        expect = Input(
            args={"a": 1, "b": 2},
            varargs=Args(name="args", values=[3, 4]),
            kwonlyargs={"c": 3, "d": 4},
            varkw=Kwargs(
                name="kwargs", values={"e": 5, "f": 6}
            ),
        )
        actual = parse_inputs(
            fnc,
            args=[1, 2, 3, 4],
            kwargs={"c": 3, "e": 5, "f": 6},
        )
        self.assertEqual(expect, actual)


class test_parse_inputs_exceptions(unittest.TestCase):
    def test_no_params_and_given_args(self):
        def fnc():
            pass

        with self.assertRaises(TypeCheckError):
            parse_inputs(fnc, args=[1])

    def test_no_params_and_given_args_and_kwargs(self):
        def fnc():
            pass

        with self.assertRaises(TypeCheckError):
            parse_inputs(fnc, args=[1], kwargs={"a": 1})

    def test_extra_args(self):
        def fnc(x):
            pass

        with self.assertRaises(TypeCheckError):
            parse_inputs(fnc, args=[1, 2])

    def test_missing_args(self):
        def fnc(x, y):
            pass

        with self.assertRaises(TypeCheckError):
            parse_inputs(fnc, args=[1])

    def test_all_kwonlyargs_no_kwargs(self):
        def fnc(*, x):
            pass

        with self.assertRaises(TypeCheckError):
            parse_inputs(fnc)

    def test_missing_kwonlyargs(self):
        def fnc(*, x):
            pass

        with self.assertRaises(TypeCheckError):
            parse_inputs(fnc)

    def test_extra_kwonlyargs(self):
        def fnc(*, x):
            pass

        with self.assertRaises(TypeCheckError):
            parse_inputs(fnc, kwargs={"x": 1, "y": 2})
