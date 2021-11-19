from formats import Colors, Styles

import unittest


class TestColors(unittest.TestCase):
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

    def test_all_colors(self):
        for color, code in self.COLORS.items():
            with self.subTest(msg=color):
                expected = f"\033[{code}mFOO\033[0m"
                actual = getattr(Colors, color)("FOO")
                self.assertEqual(expected, actual)


class TestStyles(unittest.TestCase):
    STYLES = {
        "bold": "1",
        "underline": "4",
        "reverse_video": "7",
    }

    def test_all_styles(self):
        for style, code in self.STYLES.items():
            with self.subTest(msg=style):
                expected = f"\033[{code}mFOO\033[0m"
                actual = getattr(Styles, style)("FOO")
                self.assertEqual(expected, actual)


class TestComposition(unittest.TestCase):
    def test_color_and_style(self):
        expected = "\033[31;4mFOO\033[0m"
        actual = Colors.red(Styles.underline("FOO"))
        self.assertEqual(expected, actual)
