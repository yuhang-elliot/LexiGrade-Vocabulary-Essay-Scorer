"""Vocabulary processing for the coursework text-analysis application."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterator


class TextProcessor:
    """Build, update, inspect, and persist a vocabulary from CSV text corpora."""

    def __init__(self, stopwords_filepath: str | Path, corpus_filepath: str | Path, idx2label_filepath: str | Path) -> None:
        self.stopwords = self._load_stopwords(Path(stopwords_filepath))
        self.idx2label = self._load_labels(Path(idx2label_filepath))
        self.corpus_filepath = Path(corpus_filepath)
        self.word_freq: Counter[str] = self._count_csv(self.corpus_filepath)
        self.word2idx: dict[str, int] = {}
        self.idx2word: dict[int, str] = {}
        self._update_indices()

    @staticmethod
    def _load_stopwords(path: Path) -> set[str]:
        with path.open(encoding="utf-8-sig") as source:
            return {line.strip().lower() for line in source if line.strip()}

    @staticmethod
    def _load_labels(path: Path) -> dict[int, str]:
        with path.open(encoding="utf-8") as source:
            return {int(key): value for key, value in json.load(source).items()}

    def tokenize(self, text: str) -> list[str]:
        """Return normalised, non-stopword alphabetic tokens from *text*."""
        words = re.findall(r"[^\W\d_]+", text.lower(), flags=re.UNICODE)
        return [word for word in words if len(word) >= 2 and word not in self.stopwords]

    @staticmethod
    def _text_values(row: dict[str, str | None]) -> Iterator[str]:
        if row.get("text"):
            yield row["text"] or ""
            return
        for field, value in row.items():
            if field not in {"label", "label_name"} and value:
                yield value

    def _count_csv(self, path: Path) -> Counter[str]:
        counts: Counter[str] = Counter()
        with path.open(encoding="utf-8-sig", newline="") as source:
            for row in csv.DictReader(source):
                for value in self._text_values(row):
                    counts.update(self.tokenize(value))
        return counts

    def _update_indices(self) -> None:
        words = sorted(self.word_freq)
        self.word2idx = {word: index for index, word in enumerate(words)}
        self.idx2word = {index: word for word, index in self.word2idx.items()}

    def add_file(self, path: str | Path) -> None:
        """Add token frequencies from a CSV file to the current vocabulary."""
        self.word_freq.update(self._count_csv(Path(path)))
        self._update_indices()

    def delete_file(self, path: str | Path) -> None:
        """Subtract token frequencies found in a CSV file from the vocabulary."""
        self.word_freq.subtract(self._count_csv(Path(path)))
        self.word_freq = Counter({word: count for word, count in self.word_freq.items() if count > 0})
        self._update_indices()

    def most_common(self, count: int = 10) -> list[tuple[str, int]]:
        """Return words ordered by frequency, then alphabetically for ties."""
        return sorted(self.word_freq.items(), key=lambda item: (-item[1], item[0]))[:count]

    def least_common(self, count: int = 10) -> list[tuple[str, int]]:
        """Return least frequent words, ordered alphabetically for ties."""
        return sorted(self.word_freq.items(), key=lambda item: (item[1], item[0]))[:count]

    def save(self, output_dir: str | Path = "generated") -> Path:
        """Write vocabulary reports to *output_dir* and return that directory."""
        destination = Path(output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        with (destination / "word_freq.txt").open("w", encoding="utf-8") as target:
            for word, frequency in self.most_common(len(self.word_freq)):
                target.write(f"{word} {frequency}\n")
        with (destination / "word2idx.txt").open("w", encoding="utf-8") as target:
            for word, index in self.word2idx.items():
                target.write(f"{word} {index}\n")
        with (destination / "idx2word.txt").open("w", encoding="utf-8") as target:
            for index, word in self.idx2word.items():
                target.write(f"{index} {word}\n")
        return destination
