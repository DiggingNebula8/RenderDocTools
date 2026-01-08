"""Main CLI entry point"""

import sys
from pathlib import Path

# Simple CLI implementation - can be enhanced with Click/Typer later
def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h'):
        print("RenderDoc Tools CLI")
        print("\nUsage:")
        print("  rdc-tools workflow <file.rdc> --preset <preset>")
        print("  rdc-tools parse <file.rdc> -o <output.json>")
        print("\nPresets: quick, full, csv-only, performance")
        return 0  # Return 0 for help (not an error)
    
    command = sys.argv[1]
    
    if command == "workflow":
        from renderdoc_tools.cli.commands.workflow import workflow_command
        workflow_command(sys.argv[2:])
    elif command == "parse":
        from renderdoc_tools.cli.commands.parse import parse_command
        parse_command(sys.argv[2:])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()

