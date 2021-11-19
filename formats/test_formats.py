from formats import Colors, Styles
from formats.formats import COLORS, STYLES

import unittest


class TestColors(unittest.TestCase):
    def test_all_colors(self):
        for color, code in COLORS.items():
            with self.subTest(msg=color):
                expected = f"\033[{code}mFOO\033[0m"
                actual = getattr(Colors, color)("FOO")
                self.assertEqual(expected, actual)


class TestStyles(unittest.TestCase):
    def test_all_styles(self):
        for style, code in STYLES.items():
            with self.subTest(msg=style):
                expected = f"\033[{code}mFOO\033[0m"
                actual = getattr(Styles, style)("FOO")
                self.assertEqual(expected, actual)


class TestComposition(unittest.TestCase):
    def test_color_and_style(self):
        expected = "\033[31;4mFOO\033[0m"
        actual = Colors.red(Styles.underline("FOO"))
        self.assertEqual(expected, actual)
