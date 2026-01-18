from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def main(
    *,
    text: str | None = None,
    number: float | None = None,
    payload: dict[str, Any] | None = None,
    items: list[str] | None = None,
) -> int:
    """Prints provided inputs to stdout in a consistent format.

    This is intentionally parameter-driven so other modules (like `interface.py`)
    can call it without spawning a subprocess.
    """

    print("--- OUTPUT START ---")

    if text is not None:
        print(f"text: {text}")

    if number is not None:
        print(f"number: {number}")

    if payload is not None:
        print("payload:")
        print(json.dumps(payload, indent=2, sort_keys=True))

    if items is not None:
        print(f"items ({len(items)}): {items}")

    if text is None and number is None and payload is None and items is None:
        # If nothing was provided via parameters/CLI, echo stdin (if any).
        if not sys.stdin.isatty():
            stdin_value = sys.stdin.read()
            print("stdin:")
            print(stdin_value.rstrip("\n"))
        else:
            print("No inputs provided.")

    print("--- OUTPUT END ---")
    return 0


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Echo various inputs to the console")
    parser.add_argument("--text", type=str, default=None, help="Text to print")
    parser.add_argument("--number", type=float, default=None, help="Number to print")
    parser.add_argument(
        "--json",
        dest="json_value",
        type=str,
        default=None,
        help='JSON string to print (e.g. \'{"a":1}\')',
    )
    parser.add_argument(
        "--items",
        type=str,
        default=None,
        help="Comma-separated items (e.g. a,b,c)",
    )
    return parser.parse_args(argv)


def _parse_json(json_value: str | None) -> dict[str, Any] | None:
    if json_value is None:
        return None
    try:
        parsed = json.loads(json_value)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid --json value: {e}") from e

    if isinstance(parsed, dict):
        return parsed

    # Wrap non-dict JSON values so output stays structured.
    return {"value": parsed}


def _parse_items(items_value: str | None) -> list[str] | None:
    if items_value is None:
        return None
    if items_value.strip() == "":
        return []
    return [part.strip() for part in items_value.split(",")]


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    payload = _parse_json(args.json_value)
    items = _parse_items(args.items)
    raise SystemExit(
        main(
            text=args.text,
            number=args.number,
            payload=payload,
            items=items,
        )
    )
