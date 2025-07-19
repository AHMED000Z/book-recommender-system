#!/usr/bin/env python3
"""
Setup script for running the Book Recommender System.

This script helps with common development tasks:
- Installing dependencies
- Running the application
- Running tests
- Code formatting
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(command: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    print(f"Running: {command}")
    return subprocess.run(command, shell=True, check=check)


def install_deps(dev: bool = False):
    """Install dependencies."""
    if dev:
        run_command("pip install -e .[dev]")
    else:
        run_command("pip install -r requirements.txt")


def run_app(share: bool = False, debug: bool = False):
    """Run the application."""
    cmd = "python src/book_recommender/main.py"
    if share:
        cmd += " --share"
    if debug:
        cmd += " --debug"

    run_command(cmd)


def run_tests():
    """Run tests."""
    run_command("python -m pytest tests/ -v")


def format_code():
    """Format code with black."""
    run_command("black src/ tests/")


def lint_code():
    """Lint code with flake8."""
    run_command("flake8 src/ tests/")


def type_check():
    """Type check with mypy."""
    run_command("mypy src/")


def main():
    """Main CLI."""
    parser = argparse.ArgumentParser(description="Book Recommender Development Helper")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install dependencies")
    install_parser.add_argument("--dev", action="store_true",
                                help="Install dev dependencies")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run the application")
    run_parser.add_argument("--share", action="store_true", help="Create public link")
    run_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    # Test command
    subparsers.add_parser("test", help="Run tests")

    # Code quality commands
    subparsers.add_parser("format", help="Format code with black")
    subparsers.add_parser("lint", help="Lint code with flake8")
    subparsers.add_parser("typecheck", help="Type check with mypy")

    args = parser.parse_args()

    if args.command == "install":
        install_deps(dev=args.dev)
    elif args.command == "run":
        run_app(share=args.share, debug=args.debug)
    elif args.command == "test":
        run_tests()
    elif args.command == "format":
        format_code()
    elif args.command == "lint":
        lint_code()
    elif args.command == "typecheck":
        type_check()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
