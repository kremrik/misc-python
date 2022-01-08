from os import getenv
from typing import Generator, IO

# default 4MiB
MAX_CHUNK_SIZE = getenv("MAX_CHUNK_SIZE", 4 * (1024**2))


def chunkstream(
    buffer: Generator,
    open_tag: str,
    close_tag: str,
    max_chunk_size: int = None
) -> Generator:
    # TODO: can this just act like TagGen, accepting a char
    #  and maintaining its own little state per __call__?
    if not max_chunk_size:
        max_chunk_size = MAX_CHUNK_SIZE

    ot = TagGen(open_tag)
    ct = TagGen(close_tag)
    in_tag = False
    chunk = ""

    for char in buffer:
        if o := ot(char):
            in_tag = True
            chunk += o
            continue

        if c := ct(char):
            chunk += char
            in_tag = False

        if in_tag:
            chunk += char

        if chunk and not in_tag:
            output = chunk
            chunk = ""
            yield output


class TagGen:
    def __init__(self, tag) -> None:
        self.tag = tag
        self.pos = 0
        self.chars = None

    def inside_tag(self):
        if self.chars is None:
            return False
        return len(self.chars) > 0

    def char_in_tag(self, char):
        return char == self.tag[self.pos]

    def reset(self):
        self.pos = 0
        self.chars = None

    def __call__(self, char):
        if self.char_in_tag(char):
            if not self.inside_tag():
                self.chars = char
            elif self.inside_tag():
                self.chars += char
            self.pos += 1
        elif not self.char_in_tag(char):
            if not self.inside_tag():
                pass
            elif self.inside_tag():
                self.reset()

        if self.tag == self.chars:
            output = self.chars
            self.reset()
            return output
        else:
            return None


def buffered_char_stream(
    handler: IO, size: int = 1024
) -> Generator:
    segment = handler.read(size)

    while segment:
        for char in segment:
            yield char
        segment = handler.read(size)
