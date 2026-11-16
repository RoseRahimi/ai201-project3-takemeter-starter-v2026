"""
Turn a copy-pasted Reddit thread into rows for labels.csv.

Select-all a thread page on reddit.com, paste it into a text or CSV file,
then run:

    python clean_thread.py data/raw_threads/harden_thread.csv

Each comment becomes one row with an empty label and note, appended to
labels.csv. Usernames, flair, vote counts, buttons, ads and duplicates are
dropped. You still label every row yourself.
"""

import argparse
import csv
import re
from pathlib import Path

TIME = re.compile(r"^(\d+\s?(m|h|d|mo|y|min|hr)|just now)( ago)?$", re.I)
UPVOTE = re.compile(r"^Upvote")
NOISE = re.compile(
    r"^(\d+ more repl(y|ies)|Profile Badge.*|Edited .*|•|OP|Reply|Award|Share|"
    r"Downvote|Continue this thread.*|View more comments.*|Thread)$"
)
TEAMS = {
    "Hawks", "Celtics", "Nets", "Hornets", "Bulls", "Cavaliers", "Mavericks",
    "Nuggets", "Pistons", "Warriors", "Rockets", "Pacers", "Clippers", "Lakers",
    "Grizzlies", "Heat", "Bucks", "Timberwolves", "Pelicans", "Knicks",
    "Thunder", "Magic", "76ers", "Suns", "Trail Blazers", "Blazers", "Kings",
    "Spurs", "Raptors", "Jazz", "Wizards", "NBA", "Supersonics",
}


def is_flair(line):
    return (line.startswith("emoji:") or line in TEAMS
            or re.match(r"^\[[A-Z]{2,3}\] ", line) is not None)


def read_raw(path):
    """Return a list of pasted blocks, each a list of lines.

    A CSV file can hold one pasted thread per cell; each cell is kept separate
    so the end of one thread never runs into the start of the next.
    """
    text = Path(path).read_text(encoding="utf-8-sig")
    blocks = [text]
    if text.startswith("text,label,note"):          # pasted into the CSV template
        rows = list(csv.DictReader(text.splitlines(keepends=True)))
        blocks = [r["text"] for r in rows
                  if r.get("text") and r["text"] != "Another post."
                  and not r["text"].startswith("Paste one post here")]
    return [[line.strip() for line in b.splitlines()] for b in blocks]


def find_headers(lines):
    """Index of every comment header: [u/x avatar] name [OP] • <time>."""
    headers = []
    for i in range(1, len(lines) - 1):
        if lines[i] != "•" or not (TIME.match(lines[i + 1]) or lines[i + 1] == "Ad"):
            continue
        start = i - 1
        if lines[start] == "OP":
            start -= 1
        if start > 0 and lines[start - 1].endswith(" avatar"):
            start -= 1
        headers.append((start, i + 2, lines[i + 1] == "Ad"))
    return headers


def extract(lines):
    headers = find_headers(lines)
    comments = []
    for n, (start, body_start, is_ad) in enumerate(headers):
        end = headers[n + 1][0] if n + 1 < len(headers) else len(lines)
        # Ads, and the thread's own post (its footer says "Go to comments").
        if is_ad or "Go to comments" in lines[body_start:end]:
            continue
        body = []
        for line in lines[body_start:end]:
            if UPVOTE.match(line):
                break
            if not line or NOISE.match(line):
                continue
            if not body and is_flair(line):
                continue
            body.append(line)
        if body:                                    # collapsed comments have none
            comments.append(" ".join(body))
    return comments


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("raw", help="file with the pasted thread")
    parser.add_argument("--out", default="labels.csv")
    parser.add_argument("--min-chars", type=int, default=10)
    args = parser.parse_args()

    out = Path(args.out)
    existing = []
    if out.exists():
        with out.open(encoding="utf-8") as f:
            existing = list(csv.DictReader(f))
    seen = {row["text"] for row in existing}

    new = []
    comments = [c for block in read_raw(args.raw) for c in extract(block)]
    for text in comments:
        if len(text) >= args.min_chars and text not in seen:
            seen.add(text)
            new.append({"text": text, "label": "", "note": ""})

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label", "note"])
        writer.writeheader()
        writer.writerows(existing + new)

    print(f"added {len(new)} comments to {out} (now {len(existing) + len(new)} rows)")


if __name__ == "__main__":
    main()
