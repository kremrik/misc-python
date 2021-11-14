# simple_cli
As-advertised: a CLI that does the bare minimum

### Examples
```python
from simple_cli.cli import Arg, cli

opts = [
    Arg(
        arg="setup",
        callback=lambda: print("SETUP"),
        help="Set up db"
    )
]
desc = "Simple test CLI"

cli(['-h'], opts, desc)
# DESCRIPTION
#     Simple test CLI
# 
# COMMANDS
#     setup
#         Set up db
#     -h/--help
#         Print help and exit
```

```python
from simple_cli.cli import Arg, cli

opts = [
    Arg(
        arg="setup",
        callback=lambda: print("SETUP"),
        help="Set up db"
    )
]
desc = "Simple test CLI"

cli(['setup'], opts, desc)
# SETUP
```
