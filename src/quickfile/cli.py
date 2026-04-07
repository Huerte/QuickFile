import argparse
import sys
from . import __version__
from . import config
from . import core

def handle_config(args):
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

def main():
    parser = argparse.ArgumentParser(
        prog="mk",
        description="QuickFile — Rapidly generate files with sequential naming."
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(help="Manage default settings (show, set, reset)", dest="subcommand")

    # Config Subcommand
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_subparsers = config_parser.add_subparsers(dest="action", required=True)
    
    # config show
    config_subparsers.add_parser("show", help="Show current config")
    
    # config reset
    config_subparsers.add_parser("reset", help="Reset config to defaults")
    
    # config set
    set_parser = config_subparsers.add_parser("set", help="Set a config value")
    set_parser.add_argument("key", help="Configuration key")
    set_parser.add_argument("value", help="Configuration value")

    # Main arguments (Positional)
    parser.add_argument(
        "filename", 
        nargs="?", 
        help="Extension (e.g., txt) or full name (e.g., report.pdf)"
    )
    parser.add_argument(
        "count", 
        nargs="?", 
        type=int, 
        default=1,
        help="Number of files to create (default: 1)"
    )

    args = parser.parse_args()

    # Route based on chosen subcommand vs default file generation behavior
    if args.subcommand == "config":
        handle_config(args)
    else:
        if not args.filename:
            parser.print_help()
            sys.exit(1)
            
        if args.count < 1:
            print("Error: Count must be at least 1", file=sys.stderr)
            sys.exit(1)
            
        current_config = config.load_config()
        core.generate_files(args.filename, args.count, current_config)

if __name__ == "__main__":
    main()
