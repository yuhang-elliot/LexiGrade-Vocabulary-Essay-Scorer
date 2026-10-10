"""Heuristic essay scoring built on the project vocabulary."""

from __future__ import annotations

import math
from collections import Counter
from pathlib import Path

from text_processor import TextProcessor


class EssayScorer:
    """Score an essay's length, topic coverage, vocabulary, and variety."""

    def __init__(self, text_processor: TextProcessor) -> None:
        self.text_processor = text_processor

    def _words(self, text: str) -> list[str]:
        return self.text_processor.tokenize(text)

    @staticmethod
    def _length_score(word_count: int) -> float:
        if 300 <= word_count <= 500:
            return 10.0
        distance = 300 - word_count if word_count < 300 else word_count - 500
        return max(0.0, 10.0 - distance / 20)

    @staticmethod
    def _relevance_score(words: list[str], topic_words: list[str]) -> float:
        if not topic_words:
            return 0.0
        counts = Counter(words)
        mentions = sum(min(counts[word], 3) for word in topic_words)
        return 40 * mentions / (3 * len(topic_words))

    def _rarity_score(self, unique_words: set[str]) -> float:
        if not unique_words:
            return 0.0
        points = 0
        for word in unique_words:
            frequency = self.text_processor.word_freq.get(word, 0)
            if frequency == 0:
                points -= 1
            elif frequency <= 3:
                points += 5
            elif frequency <= 20:
                points += 4
            elif frequency <= 50:
                points += 3
            elif frequency <= 100:
                points += 2
            else:
                points += 1
        return max(0.0, min(30.0, 30 * points / (3 * len(unique_words))))

    @staticmethod
    def _variety_score(unique_words: set[str], total_words: int) -> float:
        return 20 * math.sqrt(len(unique_words) / total_words) if total_words else 0.0

    def score_essay(self, prompt_text: str, essay_filepath: str | Path) -> dict[str, float]:
        """Return transparent heuristic scores for the essay at *essay_filepath*."""
        essay_words = self._words(Path(essay_filepath).read_text(encoding="utf-8"))
        topic_words = list(dict.fromkeys(self._words(prompt_text)))
        unique_words = set(essay_words)
        length = self._length_score(len(essay_words))
        relevance = self._relevance_score(essay_words, topic_words)
        rarity = self._rarity_score(unique_words)
        variety = self._variety_score(unique_words, len(essay_words))
        total = min(100.0, max(0.0, length + relevance + rarity + variety))
        return {"length": round(length, 2), "relevance": round(relevance, 2), "rarity": round(rarity, 2), "variety": round(variety, 2), "total_score": round(total, 2)}
