# formats
Simple, composable, std-lib string colors and styles

### Examples
```python
from formats import Colors, Styles

Styles.bold("BOLD TEXT")
'\x1b[1mBOLD TEXT\x1b[0m'

Colors.red("RED TEXT")
'\x1b[31mRED TEXT\x1b[0m'

Styles.bold(Colors.red("BOLD RED TEXT"))
'\x1b[1;31mBOLD RED TEXT\x1b[0m'
```
