from os import getenv

# default 4MiB
MAX_CHUNK_SIZE = getenv("MAX_CHUNK_SIZE", 4 * (1024**2))


class ChunkGen:
    def __init__(
        self,
        open_tag, 
        close_tag,
        max_chunk_size = None
    ) -> None:
        self.open_tag = open_tag
        self.close_tag = close_tag
        self.max_chunk_size = (
            max_chunk_size or MAX_CHUNK_SIZE
        )
        self._ot = TagGen(open_tag)
        self._ct = TagGen(close_tag)
        self._in_tag = False
        self._chunk = None

    def checksize(self):
        if self._chunk is None:
            return
        if len(self._chunk) >= self.max_chunk_size:
            size = self.max_chunk_size
            msg = f"Chunk larger than max_chunk_size ({size}b)"
            raise IOError(msg)

    def __call__(self, char):
        if o := self._ot(char):
            self.checksize()
            self._in_tag = True
            if not self._chunk:
                self._chunk = o
            else:
                self._chunk += o
            return

        if c := self._ct(char):
            self.checksize()
            self._chunk += char
            self._in_tag = False

        if self._in_tag:
            self.checksize()
            self._chunk += char

        if self._chunk and not self._in_tag:
            output = self._chunk
            self._chunk = ""
            return output


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
