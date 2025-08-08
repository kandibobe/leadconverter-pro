import argparse
import json
import os
from collections import Counter
from pathlib import Path

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    openai = None


KNOWN_LEVELS = {"debug", "info", "warning", "error", "critical"}


def summarize_logs(paths):
    """Return a summary dictionary for the given log files."""
    level_counts: Counter[str] = Counter()
    message_counts: Counter[str] = Counter()
    error_messages: Counter[str] = Counter()
    unknown_levels: Counter[str] = Counter()

    for path in paths:
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    # Skip malformed lines
                    continue
                level = str(entry.get("level", "info")).lower()
                msg = str(entry.get("message", ""))
                level_counts[level] += 1
                message_counts[msg] += 1
                if level == "error":
                    error_messages[msg] += 1
                if level not in KNOWN_LEVELS:
                    unknown_levels[level] += 1

    total = sum(level_counts.values())
    frequent = {m: c for m, c in message_counts.items() if c > 5}
    rare = [m for m, c in message_counts.items() if c == 1][:5]

    return {
        "total_entries": total,
        "level_counts": level_counts,
        "error_messages": error_messages,
        "frequent_messages": frequent,
        "rare_messages": rare,
        "unknown_levels": unknown_levels,
    }


def format_summary(summary):
    lines = [f"Total entries: {summary['total_entries']}"]
    if summary["level_counts"]:
        lines.append("Level counts:")
        for level, count in summary["level_counts"].items():
            lines.append(f"  {level}: {count}")
    if summary["error_messages"]:
        lines.append("Error messages:")
        for msg, count in summary["error_messages"].items():
            lines.append(f"  ({count}) {msg}")
    if summary["frequent_messages"]:
        lines.append("Frequent messages (>5 occurrences):")
        for msg, count in summary["frequent_messages"].items():
            lines.append(f"  ({count}) {msg}")
    if summary["rare_messages"]:
        lines.append("Rare messages:")
        for msg in summary["rare_messages"]:
            lines.append(f"  {msg}")
    if summary["unknown_levels"]:
        lines.append("Unknown levels:")
        for level, count in summary["unknown_levels"].items():
            lines.append(f"  {level}: {count}")
    return "\n".join(lines)


def send_to_openai(text: str, model: str = "gpt-3.5-turbo") -> str:
    """Send the summary to OpenAI and return the AI response."""
    if openai is None:
        raise RuntimeError("openai package is not installed")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message["content"]


def cli():
    parser = argparse.ArgumentParser(description="Summarize JSON logs and optionally send to OpenAI.")
    parser.add_argument("logs", nargs="+", help="Path(s) to JSON log files.")
    parser.add_argument("--send", action="store_true", help="Send the summary to OpenAI and print the AI response.")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model to use when sending the summary.")
    args = parser.parse_args()

    files = [Path(p) for p in args.logs]
    summary = summarize_logs(files)
    summary_text = format_summary(summary)
    print(summary_text)

    if args.send:
        ai_response = send_to_openai(summary_text, model=args.model)
        print("\nAI response:\n")
        print(ai_response)


if __name__ == "__main__":
    cli()
