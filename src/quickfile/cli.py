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
    parser.add_argument(
        "-o", "--out",
        dest="output_dir",
        help="Output directory (created if it doesn't exist)"
    )
    parser.add_argument(
        "-c", "--content",
        help="Initial content for the file(s)"
    )
    parser.add_argument(
        "-t", "--template",
        help="Path to a template file to use for content"
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Don't create files, just show what would be created"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output except errors"
    )
    parser.add_argument(
        "-p", "--padding",
        type=int,
        help="Zero-padding for sequential numbers (e.g., 3 for 001)"
    )
    parser.add_argument(
        "-s", "--start",
        dest="start_index",
        type=int,
        help="Starting index for sequence (default: 1)"
    )

    args = parser.parse_args(argv)

    if args.count < 1:
        print("Error: Count must be at least 1.", file=sys.stderr)
        sys.exit(1)

    current_config = config.load_config()
    core.generate_files(
        args.filename, 
        args.count, 
        current_config,
        output_dir=args.output_dir,
        content=args.content,
        template=args.template,
        dry_run=args.dry_run,
        quiet=args.quiet,
        padding=args.padding if args.padding is not None else 0,
        start_index=args.start_index if args.start_index is not None else 1
    )

def print_help():
    """Print the top-level help message."""
    help_text = (
        "usage: mk [-h] [--version] [-o OUT] [-c CONTENT] [-t TEMPLATE] [-d] [-q] [-p PADDING] [-s START] <filename> [count]\n"
        "       mk config {show,set,reset} ...\n"
        "\n"
        "QuickFile — Rapidly generate files with sequential naming.\n"
        "\n"
        "commands:\n"
        "  mk <ext>              Create a file (e.g., mk txt)\n"
        "  mk <ext> <count>      Create multiple files (e.g., mk txt 5)\n"
        "  mk <name.ext>         Create a named file (e.g., mk report.pdf)\n"
        "  mk undo               Undo the last file generation\n"
        "  mk config show        Show current configuration\n"
        "  mk config set <k> <v> Set a configuration value\n"
        "  mk config reset       Reset configuration to defaults\n"
        "\n"
        "options:\n"
        "  -h, --help            Show this help message and exit\n"
        "  --version             Show program's version number and exit\n"
        "  -o, --out <dir>       Output directory (created if it doesn't exist)\n"
        "  -c, --content <str>   Initial content for the file(s)\n"
        "  -t, --template <path> Path to a template file\n"
        "  -d, --dry-run         Don't create files, just show what would be created\n"
        "  -q, --quiet           Suppress output except errors\n"
        "  -p, --padding <num>   Zero-padding for numbers (e.g., 3 for 001)\n"
        "  -s, --start <num>     Starting index for sequence (default: 1)\n"
    )
    print(help_text)

def interactive_mode():
    """Run QuickFile in interactive mode."""
    print("Welcome to QuickFile Interactive Mode!")
    print("Press Ctrl+C to exit at any time.")
    
    try:
        filename = input("Enter extension (e.g., txt) or full name (e.g., report.pdf): ").strip()
        if not filename:
            print("Error: Filename or extension is required.")
            return

        count_str = input("How many files? (default: 1): ").strip()
        count = int(count_str) if count_str else 1
        
        output_dir = input("Output directory? (press Enter for current): ").strip()
        content = input("Initial content? (press Enter for empty): ").strip()
        
        current_config = config.load_config()
        core.generate_files(
            filename, 
            count, 
            current_config,
            output_dir=output_dir if output_dir else None,
            content=content if content else None
        )
        print("\nDone!")
    except KeyboardInterrupt:
        print("\nExiting interactive mode.")
    except ValueError:
        print("Error: Invalid input.")

def handle_undo():
    """Handle the `mk undo` command."""
    last_files = config.load_last_run()
    if not last_files:
        print("Nothing to undo.")
        return

    print(f"Found {len(last_files)} files from the last operation.")
    confirm = input("Are you sure you want to delete them? [y/N]: ").strip().lower()
    if confirm == 'y':
        for file_path_str in last_files:
            path = Path(file_path_str)
            if path.exists():
                try:
                    path.unlink()
                    print(f"Deleted: {path}")
                except OSError as e:
                    print(f"Error deleting {path}: {e}")
            else:
                print(f"File already gone: {path}")
        config.clear_last_run()
        print("Undo complete.")
    else:
        print("Undo cancelled.")

def main():
    # Handle --version and --help before anything else
    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"mk {__version__}")
        sys.exit(0)

    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)

    # If no arguments, enter interactive mode
    if len(sys.argv) < 2:
        interactive_mode()
        sys.exit(0)

    # Dispatch based on first positional argument
    command = sys.argv[1]

    if command == "config":
        handle_config(sys.argv[2:])
    elif command == "undo":
        handle_undo()
    else:
        handle_generate(sys.argv[1:])

if __name__ == "__main__":
    main()

