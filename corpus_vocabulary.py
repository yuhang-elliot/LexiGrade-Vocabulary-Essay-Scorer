from pathlib import Path
from typing import List, Optional, Tuple

def get_stopwords(stopwords_file: str) -> List[str]:
    """
    load and clean stop_words in files 

    Args:
        stopwords_file(str):path to the stopwords file

    Returns:
        List[str]: list of cleaned lowercase stopwords

    """

    path = Path(stopwords_file)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path

    stopwords: List[str] = []
    with path.open('r', encoding='utf-8-sig') as f:
        for line in f:
            w=line.strip().lower()

            clean_word = "".join(ch for ch in w if ch.isalnum())
            if clean_word:
                stopwords.append(clean_word)

    return stopwords

def _normalize_text(text: str) -> str:
    """
    normalize text by lowercasing and removing punctuation

    Args:
        text(str):Raw input text

    Returns:
        str:cleaned and normalized text
    """
    text_lower=text.lower()
    ascii_punct=set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~") #String of ascii punctuation characters
    extra_punct={'—', '–', '−', '“', '”', '‘', '’', '…'}# impelement of punctuation characters
    all_punct=ascii_punct.union(extra_punct)
    translation_map = {}
    for ch in all_punct:
        # get the Unicode number for the character and map it to a space
        translation_map[ord(ch)] = ' '
    text_lower=text_lower.translate(translation_map)

    return ' '.join(text_lower.split()) 



def get_vocabs(text: str, stopwords: List[str]) -> Tuple[Tuple[str], Tuple[int]] | Tuple[()]:
    """
    extracting  vocabulary and frequency from text, excluding stopwords and short digit containing tokens


    Args:
        text(str):input text to process
        stopwords(List[str]):list of stopwords to exclude


    Returns:
        Tuple[Tuple[str],Tuple[int]]:sorted vocabulary and corresponding frequencies
        if no valid tokens found, return empty
    """
    clean_text=_normalize_text(text)
    if not clean_text:
        return ()

    sw=set(stopwords)

    # check if the token is >=2 and containing any number or including stopwords
    tokens=[ tok for tok in clean_text.split() 
    if len(tok)>=2
    and not any(charactor.isdigit() for charactor in tok)
    and tok not in sw]

    if not tokens:
        return ()

    freq_dict: dict[str, int]={}
    for tok in tokens:
        freq_dict[tok]=freq_dict.get(tok, 0)+1

    sorted_words=tuple(sorted(freq_dict.keys()))
    sorted_freqs= tuple(freq_dict[w] for w in sorted_words)
    return (sorted_words, sorted_freqs)



def process_mini_dataset(
    stop_words: List[str],
    data_path: str = 'data',
    category: Optional[str] = None,
) -> Tuple[Tuple[str], Tuple[int]] | Tuple[()]:
    """
    process a directory of all .txt files to extract vocabulary,excluding stopwords

    Args:
        stop_words(List[str]):list of stopwords to exclude
        data_path (str):Root directory containing text files
        category(Optional[str]):Subdirectory/category to process

    Returns:
        Tuple[Tuple[str],Tuple[int]]:vocabulary and frequency tuples
        or empty tuple if no valid files or tokens found
    """

    root_dir = Path(category) if category else Path(data_path)
    if not root_dir.is_absolute():
        root_dir = Path(__file__).resolve().parent / root_dir


    txt_file_paths: List[Path] = []

    #go through any folders in root_dir
    for file_path in root_dir.rglob("*.txt"):
        if file_path.name != "stop_words_english.txt":
            txt_file_paths.append(file_path)


    parts: List[str] = []
    for file_path in txt_file_paths:
        with file_path.open('r', encoding='utf-8-sig') as f:
            parts.append(f.read())


    aggregated_text = " ".join(parts).strip()
    return get_vocabs(aggregated_text, stop_words)

# WARNING!!! *DO NOT* REMOVE THIS LINE 
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    stopwords = get_stopwords("data/stop_words_english.txt")

