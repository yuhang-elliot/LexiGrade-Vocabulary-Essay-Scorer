from typing import Tuple, List


def get_vocabs_simple(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    """
    build a vocabulary (unique words + counts).
    split by whitespace, only allows alphabetic.
    record times of occurence.

    Params:
        text (str): raw string.

    Returns:
        Tuple[Tuple[str, ...], Tuple[int, ...]] | Tuple[()]:
            1. (unique_word_list, word_count)
            2. return () if there are no valid alphabetic words.
    """
     # Split on whitespace, only allow alpha input
    text_collection = text.split()
    pure_text_list = [word for word in text_collection if word.isalpha()]
    
    #countfrequencies using a dict
    text_count_dict = {}
    for word in pure_text_list:
        if word in text_count_dict:
            text_count_dict[word] += 1
        else:
            text_count_dict[word] = 1

    #sort unique words to get a list which is in oder
    unique_word_list = tuple(sorted(text_count_dict.keys()))
    #count the counts of the words according to the order of "unique_word_list".
    word_count = tuple(text_count_dict[word] for word in unique_word_list)
    
    if not unique_word_list:
        return ()
    return (unique_word_list, word_count)


def get_vocabs(text: str) -> Tuple[Tuple[str], Tuple[int]] | Tuple[()]:
    """
    hange non-alpha into space, lower the alpha.

    Params:
        text (str):

    Returns:
        Tuple[Tuple[str, ...], Tuple[int, ...]] | Tuple[()]:
            same as "get_vocabs_simple'ㄡ
    """
    
    cleaning_list = []
    for word in text:
        if word.isalpha():
            cleaning_list.append(word.lower())
        else:
            cleaning_list.append(' ')
    clean_str = ''.join(cleaning_list)
    

    return (get_vocabs_simple(clean_str))

    

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    the_example_str = ", ''"
    print(get_vocabs_simple(the_example_str))
    print(get_vocabs(the_example_str))
