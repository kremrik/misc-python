# watch
API for detecting file/directory changes (create/modify/remove)

### Examples
Let's say we have a directory that looks like:
```
$ ls
foo.txt bar.txt
```

We can watch for any changes to that directory like:
```python
from watch import Watch

watch = Watch()

watch.created
# []
watch.modified
# []
watch.removed
# []
```

No files create, modified, or removed yet.
But if we run something like

```
$ touch baz.txt
```

and then

```python
watch.created
# ['/abs/path/to/baz.txt']
```

In order to acknowledge the change, you must explicitly
acknowlede it. Without `ack`ing, all changes since the 
last `ack` (or instantiation) will accumulate, providing a
way to precisely control how (and when) you handle events.

```python
watch.created  # still here!
# ['/abs/path/to/baz.txt']

watch.ack()
watch.created  # now it's gone
# []
```
