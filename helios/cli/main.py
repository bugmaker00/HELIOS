"""Command-line interface for HELIOS."""

import argparse
import sys
import logging
from pathlib import Path

# TODO: replace argparse with a richer CLI framework (e.g. click or typer)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="helios",
        description="High-Efficiency Library for Intelligent Operations and Systems",
    )
    sub = parser.add_subparsers(dest="command")

    run_p = sub.add_parser("run", help="Run a pipeline")
    run_p.add_argument("pipeline", help="Path to pipeline YAML config")
    run_p.add_argument("--dry-run", action="store_true")
    run_p.add_argument("--workers", type=int, default=1)
    # TODO: add --output-format flag (json, text, csv)

    sub.add_parser("version", help="Print version and exit")

    return parser


def cmd_run(args) -> int:
    config_path = Path(args.pipeline)
    if not config_path.exists():
        print(f"Error: config file not found: {config_path}", file=sys.stderr)
        return 1
    # TODO: parse the YAML config and delegate to Engine.start()
    print(f"Running pipeline: {config_path}")
    return 0


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO)
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return cmd_run(args)
    elif args.command == "version":
        # TODO: read version from importlib.metadata instead of hard-coding
        print("helios 0.1.0")
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
