# chunkstream
A mechanism for chunking data in-stream

### Examples
If we have an giant XML file like the one in `string` below
that is too large for in-memory processing, and if we only
care about the `tag` element, we can pull out said element
by doing something like:

```python
from chunkstream import ChunkGen
from io import StringIO
from textwrap import dedent

string = dedent("""\
<root>
    <crap>
        <tag>hello world</tag>
    </crap>
    <crap>
        <tag>goodbye world</tag>
    </crap>
</root>
""").strip()

def buffered_char_stream(
    handler, size: int = 1024
):
    segment = handler.read(size)
    while segment:
        for char in segment:
            yield char
        segment = handler.read(size)

handler = StringIO(string)
buffer = buffered_char_stream(handler, 16)


cg = ChunkGen("<tag>", "</tag>")
for char in buffer:
    if chunk := cg(char):
        print(chunk)
# <tag>hello world</tag>
# <tag>goodbye world</tag>
```
