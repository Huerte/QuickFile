import argparse
import sys
from . import __version__
from . import config
from . import core

def handle_config(argv):
    """Parse and handle `mk config <action>` subcommands."""
    parser = argparse.ArgumentParser(
        prog="mk config",
        description="Manage QuickFile configuration."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    # config show
    subparsers.add_parser("show", help="Show current config")

    # config reset
    subparsers.add_parser("reset", help="Reset config to defaults")

    # config set
    set_parser = subparsers.add_parser("set", help="Set a config value")
    set_parser.add_argument("key", help="Configuration key (e.g., prefix)")
    set_parser.add_argument("value", help="Configuration value")

    args = parser.parse_args(argv)

    if args.action == "show":
        current_config = config.load_config()
        print("Current Configuration:")
        for k, v in current_config.items():
            print(f"  {k} = {v}")
    elif args.action == "set":
        try:
            config.set_value(args.key, args.value)
            print(f"Configuration updated: {args.key} = {args.value}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.action == "reset":
        config.reset_config()
        print("Configuration reset to defaults.")

def handle_generate(argv):
    """Parse and handle `mk <filename> [count]` file generation."""
    parser = argparse.ArgumentParser(
        prog="mk",
        description="QuickFile — Rapidly generate files with sequential naming."
    )
    parser.add_argument(
        "filename",
        help="Extension (e.g., txt) or full name (e.g., report.pdf)"
    )
    parser.add_argument(
        "count",
        nargs="?",
        type=int,
        default=1,
        help="Number of files to create (default: 1)"
    )

    args = parser.parse_args(argv)

    if args.count < 1:
        print("Error: Count must be at least 1.", file=sys.stderr)
        sys.exit(1)

    current_config = config.load_config()
    core.generate_files(args.filename, args.count, current_config)

def print_help():
    """Print the top-level help message."""
    help_text = (
        "usage: mk [-h] [--version] <filename> [count]\n"
        "       mk config {show,set,reset} ...\n"
        "\n"
        "QuickFile — Rapidly generate files with sequential naming.\n"
        "\n"
        "commands:\n"
        "  mk <ext>              Create a file (e.g., mk txt)\n"
        "  mk <ext> <count>      Create multiple files (e.g., mk txt 5)\n"
        "  mk <name.ext>         Create a named file (e.g., mk report.pdf)\n"
        "  mk config show        Show current configuration\n"
        "  mk config set <k> <v> Set a configuration value\n"
        "  mk config reset       Reset configuration to defaults\n"
        "\n"
        "options:\n"
        "  -h, --help            Show this help message and exit\n"
        "  --version             Show program's version number and exit\n"
    )
    print(help_text)

def main():
    # Handle --version and --help before anything else
    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"mk {__version__}")
        sys.exit(0)

    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    # Dispatch based on first positional argument
    command = sys.argv[1]

    if command == "config":
        handle_config(sys.argv[2:])
    else:
        handle_generate(sys.argv[1:])

if __name__ == "__main__":
    main()

