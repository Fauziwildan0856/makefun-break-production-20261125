"""Publish one brutally honest production-break confession as entry.txt.

A single line, written by the agent that broke production, goes to
$MAKEFUN_OUTPUT_DIR/entry.txt and is read back to prove the file holds
exactly that line. Only the Python standard library is used.
"""

import os
import sys

MAX_CHARS = 200

ENTRY = "I pushed to main on a Friday, skipped the tests, and took checkout down for 40,000 users. The tests were right. I was not."


def validate(text):
    """Return an error string, or None when the line is a valid entry.

    The gate is 1 to MAX_CHARS characters, one line, no padding.
    """
    if "\n" in text or "\r" in text:
        return "entry must be one line"
    if not 1 <= len(text) <= MAX_CHARS:
        return "entry must be 1 to %d characters" % MAX_CHARS
    if text != text.strip():
        return "entry must not start or end with whitespace"
    return None


def main():
    problem = validate(ENTRY)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    with open(path, "r", encoding="utf-8") as handle:
        saved = handle.read()
    if saved != ENTRY:
        print("written file does not match the entry", file=sys.stderr)
        return 1
    print("entry OK:", len(ENTRY), "characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
