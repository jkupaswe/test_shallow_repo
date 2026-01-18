from __future__ import annotations

from typing import Any

import main


EXAMPLES: list[dict[str, Any]] = [
    {
        "name": "text only",
        "params": {"text": "hello world"},
    },
    {
        "name": "number only",
        "params": {"number": 42},
    },
    {
        "name": "payload dict",
        "params": {"payload": {"user": "alice", "active": True, "score": 9.5}},
    },
    {
        "name": "items list",
        "params": {"items": ["apple", "banana", "carrot"]},
    },
    {
        "name": "all inputs",
        "params": {
            "text": "combo",
            "number": 3.14,
            "payload": {"nested": {"a": 1, "b": [1, 2, 3]}},
            "items": ["x", "y"],
        },
    },
]


def run_examples() -> None:
    for example in EXAMPLES:
        print(f"\n=== Example: {example['name']} ===")
        main.main(**example["params"])


if __name__ == "__main__":
    run_examples()
