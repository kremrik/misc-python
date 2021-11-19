from simple_cli.cli import Arg, cli


opts = [Arg("setup", lambda: print("SETUP"), "Set up db")]
args = ['-h']
desc = "Simple test CLI"


# cli(['-h'], opts, desc)
cli(['setup'], opts, desc)
# cli(args, opts)
