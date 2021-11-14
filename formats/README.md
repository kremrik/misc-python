# Formats
Simple, composable, std-lib string colors and styles

### Examples
```python
from formats import Colors, Styles

txt = Styles.bold(Colors.red("BOLD RED TEXT"))
type(txt)
# formats.formats.FormattedText
```

### Notes
As you can see from the above example, the return type is
_not_ a Python `str`, but an instance of `FormattedText`.
This was done for two reasons:
1. it implements `__repr__` and `__str__`, thereby appearing exactly as you'd expect in the REPL
2. it allows for composability without having to split strings, resort to regex, etc
