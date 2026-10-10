# LexiGrade — Vocabulary & Essay Scorer

LexiGrade is a command-line Python project that builds a vocabulary from a news corpus, analyses word frequencies, and scores essays for length, topic relevance, vocabulary rarity, and variety.

This project consolidates the final stages of a school programming assignment into one runnable program. Earlier exercises are retained as learning history; the application itself is provided by `app.py`, `text_processor.py`, and `essay_scorer.py`.

> The essay score is an educational heuristic, not a substitute for human assessment.

## Features

- Builds a case-normalised vocabulary from the included CSV corpus.
- Removes stop words and single-character or numeric tokens.
- Shows the most or least frequent vocabulary items.
- Adds or subtracts vocabulary counts from additional CSV files.
- Writes word-frequency, word-to-index, and index-to-word reports.
- Scores a text essay for length, prompt relevance, vocabulary rarity, and variety.
- Uses only the Python standard library.

## Project layout

```text
.
├── app.py                 # Unified command-line application
├── text_processor.py      # Vocabulary processing module
├── essay_scorer.py        # Essay-scoring module
├── data/
│   ├── ag_news_test.csv   # Sample corpus
│   ├── add.csv            # Sample vocabulary addition
│   ├── delete.csv         # Sample vocabulary removal
│   ├── idx2label.json     # Corpus label names
│   └── stop_words_english.txt
├── sample_essay.txt       # Example essay input
├── marks_parser.py        # Mark parsing exercise
├── marks_console.py       # Interactive mark-system exercise
├── vocabulary_basics.py   # Basic vocabulary exercise
├── corpus_vocabulary.py   # Corpus vocabulary exercise
├── vocabulary_storage.py  # Vocabulary persistence exercise
├── cli.py                 # Alternate CLI entry point
└── home (1).zip ...       # Original submission snapshots
```

## Requirements

- Python 3.10 or later
- No third-party dependencies

## Quick start

Clone the repository, enter the project folder, and run:

```bash
python app.py summary
```

## Commands

View the ten most or least frequent vocabulary items:

```bash
python app.py top --count 10
python app.py bottom --count 10
```

Create an updated vocabulary report after adding or removing a CSV file. Reports are saved to `generated/` by default:

```bash
python app.py add
python app.py remove
python app.py add path/to/new_articles.csv --output results
```

Score an essay against a prompt:

```bash
python app.py score --prompt "The impact of technology on education"
python app.py score --prompt "Renewable energy policy" --essay path/to/essay.txt
```

The scoring command prints a JSON result with a maximum total of 100 points:

| Component | Points | Description |
| --- | ---: | --- |
| Length | 10 | Best range is 300–500 tokenised words. |
| Relevance | 40 | Capped prompt-keyword coverage. |
| Rarity | 30 | Rewards vocabulary that is less frequent in the corpus. |
| Variety | 20 | Rewards a higher ratio of unique words. |

## CSV format

The application reads a CSV column named `text`. If that column is not available, it processes non-label text columns. An optional `label` column is supported for the included AG News-style data.

```csv
text,label
"Example article text",2
```

## Notes for public publication

- The included data is sample coursework material. Check data licensing before replacing it with a new corpus.
- Generated reports are excluded from Git by `.gitignore`.
- The original ZIP files are preserved as submission history; the unpacked `data/` folder and unified application are the public-project entry point.
- Do not commit real credentials, personal data, or private assessment feedback.

## Future improvements

- Add automated tests for tokenisation, CSV updates, and score calculations.
- Add configurable tokenisation and scoring rules.
- Add a web or desktop interface.
- Package the application for installation with `pip`.

## License

No license has been selected. Add one before accepting external contributions or allowing reuse.
