"""
Entry point for rdc-tools command
"""

import sys


def main():
    """Main entry point for rdc-tools command"""
    from renderdoc_tools.cli.main import main as cli_main
    sys.exit(cli_main())


if __name__ == "__main__":
    main()

