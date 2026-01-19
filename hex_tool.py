#!/usr/bin/env python3
"""Generate an 8-character hex code."""

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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.count <= 0:
        raise ValueError("count must be positive")
    for _ in range(args.count):
        print(generate_hex_code(args.length))


if __name__ == "__main__":
    main()
