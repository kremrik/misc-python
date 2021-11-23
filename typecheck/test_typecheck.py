from typecheck.typecheck import (
    parse_inputs,
    Input,
    TypeCheckError,
)

import unittest


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

        expect = Input(varargs=[1])
        actual = parse_inputs(fnc, args=[1])
        self.assertEqual(expect, actual)

    def test_mult_varargs(self):
        def fnc(*args):
            pass

        expect = Input(varargs=[1, 2, 3])
        actual = parse_inputs(fnc, args=[1, 2, 3])
        self.assertEqual(expect, actual)

    def test_args_and_varargs(self):
        def fnc(x, y, *args):
            pass

        expect = Input(
            args={"x": 1, "y": 2}, varargs=[3, 4]
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

        expect = Input(varkw={"x": 1})
        actual = parse_inputs(fnc, kwargs={"x": 1})
        self.assertEqual(expect, actual)

    def test_mult_varkw(self):
        def fnc(**kwargs):
            pass

        expect = Input(varkw={"x": 1, "y": 2, "z": 3})
        actual = parse_inputs(
            fnc, kwargs={"x": 1, "y": 2, "z": 3}
        )
        self.assertEqual(expect, actual)

    def test_kwonlyargs_and_varkw(self):
        def fnc(*, i, j, **kwargs):
            pass

        expect = Input(
            kwonlyargs={"i": -1, "j": 0},
            varkw={"x": 1, "y": 2},
        )
        actual = parse_inputs(
            fnc, kwargs={"i": -1, "j": 0, "x": 1, "y": 2}
        )
        self.assertEqual(expect, actual)

    def test_args_varargs_kwonlyargs_and_varkw(self):
        def fnc(a, b, *args, c, d, **kwargs):
            pass

        expect = Input(
            args={"a": 1, "b": 2},
            varargs=[3, 4],
            kwonlyargs={"c": 3, "d": 4},
            varkw={"e": 5, "f": 6},
        )
        actual = parse_inputs(
            fnc,
            args=[1, 2, 3, 4],
            kwargs={"c": 3, "d": 4, "e": 5, "f": 6},
        )
        print(actual)
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
