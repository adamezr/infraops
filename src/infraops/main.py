#!/usr/bin/env python3

import argparse
import sys

from infraops.commands.health import run_health


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="infraops",
        description="Lightweight Linux operations toolkit for monitoring and troubleshooting.",
    )

    subparsers = parser.add_subparsers(dest="command")

    health_parser = subparsers.add_parser(
        "health",
        help="Run a system health check",
    )

    health_parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored terminal output",
    )

    health_parser.set_defaults(func=run_health)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
