from typing import Dict, Tuple

def save_word_freq(words: Tuple[str, ...], freqs: Tuple[int, ...], file_path: str = "word_freq.txt") -> None:
    """
    save words and their frequencies to a file, sorted by descending frequency

    Args:
        words (Tuple[str]):Tuple of words
        freqs (Tuple[int]): Corresponding frequencies for each word
        file_path (str): Output file path

    """

    if len(words) != len(freqs):
        raise ValueError("words and freqs must have the same length")
    pairs = sorted(zip(words, freqs), key=lambda pair: (-pair[1], pair[0]))
    with open(file_path, "w", encoding="utf-8") as f:
        for word, frequency in pairs:
            f.write(f"{word} {frequency}\n")



def save_word2idx(words: Tuple[str, ...], file_path: str = "word2idx.txt") -> None:
    """
    save a word to index mapping, sorted by word alphabetically

    Args:
        words(Tuple[str]):Tuple of words
        file_path(str): Output file path

    """

    sorted_unique = sorted(set(words))

    #create a mapping from word to index
    mapping = {}
    for idx in range(len(sorted_unique)):
        word = sorted_unique[idx]
        mapping[word] = idx

    #write the mapping to a file
    with open(file_path, "w", encoding="utf-8") as f:
        for word in mapping:
            index = mapping[word]
            line = f"{word} {index}\n"
            f.write(line)


def save_idx2word(words: Tuple[str, ...], file_path: str = "idx2word.txt") -> None:
    """
    save an index-to-word mapping, sorted by word alphabetically 

    Args:
        words(Tuple[str]):Tuple of words
        file_path (str): Output file path

    """

    sorted_unique = sorted(set(words))

    #create a mapping from index to word
    mapping = {}

    for idx in range(len(sorted_unique)):
        word = sorted_unique[idx]
        mapping[idx] = word

    #write the mapping to a file
    with open(file_path, "w", encoding="utf-8") as f:
        for idx in sorted(mapping):
            line = f"{idx} {mapping[idx]}\n"
            f.write(line)


def load_word_freq(file_path: str) -> Dict[str, int]:
    """
    load a word to frequency mapping from a file

    Args:
        file_path(str):path to the word frequency file

    Returns:
        Dict[str, int]:dictionary of word-frequency pairs


    """

    word_freq ={}
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            parts=line.strip().split(maxsplit=1)

            #check if the line has exactly two parts
            if len(parts)!= 2:
                print("Invalid format at line", line_num)
                continue

            word=parts[0]
            freq_str = parts[1]

            #check if frequency is a valid number
            if not freq_str.isdigit():
                print("Invalid frequency at line", line_num)
                continue

            freq = int(freq_str)

            #add to dictionary
            word_freq[word]=freq

    return word_freq


def load_word2idx(file_path: str) -> Dict[str, int]:
    """
    load a word to index mapping from a file

    Args:
        file_path(str):path to the word2idx.txt file

    Returns:
        Dict[str,int]:dictionary mapping words to indices

    """
    mapping = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            parts=line.strip().split(maxsplit=1)

            #check if the line has exactly two parts
            if len(parts)!= 2:
                print("Invalid format at line", line_num)
                continue
            word = parts[0]
            idx_str = parts[1]
            #try converting index to integer
            if not idx_str.isdigit():
                print("Invalid index at line", line_num)
                continue
            idx = int(idx_str)
            #check for duplicates
            if word in mapping:
                print("Duplicate word at line", line_num)
                continue
            if idx in mapping.values():
                print("Duplicate index at line", line_num)
                continue
            #add to mapping
            mapping[word] = idx

    return mapping



def load_idx2word(file_path: str) -> Dict[int, str]:
    """
    load an index to word mapping from a file

    Args:
        file_path(str):Path to the idx2word file

    Returns:
        Dict[int, str]: dictionary mapping indices to words

    """

    mapping = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            parts = line.strip().split(maxsplit=1)
        #check if the line has exactly two parts
            if len(parts)!= 2:
                print("Invalid format at line", line_num)
                continue
            idx_str,wrd=parts
        #convert index to integer
            try:
                idx = int(idx_str)
            except ValueError:
                print("Invalid index at line", line_num)
                continue
        #check for duplicate index or word
            if idx in mapping:
                print("Duplicate index at line", line_num)
                continue
            if wrd in mapping.values():
                print("Duplicate word at line", line_num)
                continue
        #add to mapping
            mapping[idx]=wrd
    return mapping


