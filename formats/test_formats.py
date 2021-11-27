from formats import Colors, Styles
from formats.formats import COLORS, STYLES

import unittest


class TestColorsAndStyles(unittest.TestCase):
    TXT = "HELLO!"

    def test_all_colors(self):
        for color, code in COLORS.items():
            with self.subTest(msg=color):
                expected = f"\033[{code}m{self.TXT}\033[0m"
                actual = getattr(Colors, color)(self.TXT)
                self.assertEqual(expected, actual)

    def test_all_styles(self):
        for style, code in STYLES.items():
            with self.subTest(msg=style):
                expected = f"\033[{code}m{self.TXT}\033[0m"
                actual = getattr(Styles, style)(self.TXT)
                self.assertEqual(expected, actual)

    def test_color_and_style(self):
        expected = f"\033[31;4m{self.TXT}\033[0m"
        actual = Colors.red(Styles.underline(self.TXT))
        self.assertEqual(expected, actual)

    def test_print_sanity_check(self):
        for k, v in dict(Colors.__dict__).items():
            if k.startswith("_"):
                continue
            print(f"  {k}: {v(self.TXT)}")

        for k, v in dict(Styles.__dict__).items():
            if k.startswith("_"):
                continue
            print(f"  {k}: {v(self.TXT)}")
