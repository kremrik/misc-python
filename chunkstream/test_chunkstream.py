from chunkstream import ChunkGen

import unittest
from io import BytesIO, StringIO
from textwrap import dedent


def buffered_char_stream(handler, size=16):
    segment = handler.read(size)

    if isinstance(segment, bytes):
        xformer = lambda x: chr(x)
    else:
        xformer = lambda x: x

    while segment:
        for char in segment:
            yield xformer(char)
        segment = handler.read(size)


class TestChunkGen(unittest.TestCase):
    def test_success(self):
        string = dedent(
            """\
        <root>
            <crap>
                <tag>hello world</tag>
            </crap>
            <crap>
                <tag>goodbye world</tag>
            </crap>
        </root>
        """
        ).strip()
        handler = StringIO(string)
        buffer = buffered_char_stream(handler)
        cg = ChunkGen("<tag>", "</tag>")

        expect = [
            "<tag>hello world</tag>",
            "<tag>goodbye world</tag>",
        ]
        actual = []
        for char in buffer:
            if chunk := cg(char):
                actual.append(chunk)
        self.assertEqual(expect, actual)

    def test_overflow(self):
        string = dedent(
            """\
        <root>
            <crap>
                <tag>hello world</tag>
            </crap>
            <crap>
                <tag>goodbye world</tag>
            </crap>
        </root>
        """
        ).strip()
        handler = StringIO(string)
        buffer = buffered_char_stream(handler)
        cg = ChunkGen("<tag>", "</tag>", 8)

        with self.assertRaises(IOError):
            for char in buffer:
                cg(char)

    def test_with_bytes(self):
        bytez = (
            dedent(
                """\
        <root>
            <crap>
                <tag>hello world</tag>
            </crap>
            <crap>
                <tag>goodbye world</tag>
            </crap>
        </root>
        """
            )
            .strip()
            .encode()
        )
        handler = BytesIO(bytez)
        buffer = buffered_char_stream(handler)
        cg = ChunkGen("<tag>", "</tag>")

        expect = [
            "<tag>hello world</tag>",
            "<tag>goodbye world</tag>",
        ]
        actual = []
        for char in buffer:
            if chunk := cg(char):
                actual.append(chunk)
        self.assertEqual(expect, actual)
