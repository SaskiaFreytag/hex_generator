#!/usr/bin/env python3
"""Generate random hex codes for CLI or Slack-style invocations."""

from __future__ import annotations

import argparse
import secrets


def generate_hex_code(length: int = 8) -> str:
    """Return a random lowercase hex code of the requested length."""
    if length <= 0:
        raise ValueError("length must be positive")
    # Each byte produces two hex characters, so request enough bytes and trim.
    byte_count = (length + 1) // 2
    return secrets.token_hex(byte_count)[:length]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one or more random hex codes.",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=1,
        help="Number of codes to generate (default: 1).",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=8,
        help="Length of each hex code (default: 8).",
    )
    parser.add_argument(
        "slack_args",
        nargs="*",
        help="Optional Slack-style input like: @hex_generator 10 codes",
    )
    args = parser.parse_args()
    return normalize_slack_args(args)


def normalize_slack_args(args: argparse.Namespace) -> argparse.Namespace:
    if not args.slack_args:
        return args
    tokens = [token for token in args.slack_args if token != "@hex_generator"]
    if not tokens:
        return args
    if tokens[0].isdigit():
        args.count = int(tokens[0])
    if len(tokens) > 1 and tokens[1].isdigit():
        args.length = int(tokens[1])
    return args


def main() -> None:
    args = parse_args()
    if args.count <= 0:
        raise ValueError("count must be positive")
    for _ in range(args.count):
        print(generate_hex_code(args.length))


if __name__ == "__main__":
    main()
