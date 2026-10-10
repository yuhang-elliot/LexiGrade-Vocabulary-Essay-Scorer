"""Command-line entry point for the text vocabulary and essay-scoring project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from text_processor import TextProcessor
from essay_scorer import EssayScorer


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def processor() -> TextProcessor:
    return TextProcessor(DATA / "stop_words_english.txt", DATA / "ag_news_test.csv", DATA / "idx2label.json")


def print_words(words: list[tuple[str, int]]) -> None:
    for word, frequency in words:
        print(f"{word:<20} {frequency}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build and inspect a corpus vocabulary, or score an essay.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("summary", help="Show corpus size and the ten most frequent words.")
    for name, description in (("top", "Show the most frequent words."), ("bottom", "Show the least frequent words.")):
        command = commands.add_parser(name, help=description)
        command.add_argument("--count", type=int, default=10, help="Number of words to show (default: 10).")
    for name, description, default in (("add", "Add a CSV file to the vocabulary.", DATA / "add.csv"), ("remove", "Subtract a CSV file from the vocabulary.", DATA / "delete.csv")):
        command = commands.add_parser(name, help=description)
        command.add_argument("file", nargs="?", type=Path, default=default, help="CSV file to process.")
        command.add_argument("--output", type=Path, default=ROOT / "generated", help="Where to save vocabulary reports.")
    score = commands.add_parser("score", help="Score an essay using the corpus vocabulary.")
    score.add_argument("--prompt", required=True, help="Essay prompt used to estimate topic relevance.")
    score.add_argument("--essay", type=Path, default=ROOT / "sample_essay.txt", help="Text essay to score.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    text_processor = processor()
    if args.command == "summary":
        print(f"Vocabulary size: {len(text_processor.word_freq)} words")
        print_words(text_processor.most_common())
    elif args.command == "top":
        print_words(text_processor.most_common(args.count))
    elif args.command == "bottom":
        print_words(text_processor.least_common(args.count))
    elif args.command in {"add", "remove"}:
        (text_processor.add_file if args.command == "add" else text_processor.delete_file)(args.file)
        output = text_processor.save(args.output)
        print(f"Saved {len(text_processor.word_freq)} vocabulary entries to {output}")
    else:
        print(json.dumps(EssayScorer(text_processor).score_essay(args.prompt, args.essay), indent=2))


if __name__ == "__main__":
    main()
