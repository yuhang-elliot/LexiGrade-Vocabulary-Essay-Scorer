from typing import Dict


def mark_str_to_dict(mark_str: str) -> Dict [str, int | float]:
    '''
    recive a str which has mark,convering into new dict
    Paramaters: mmark_str: str - eg. "subjectA: scoreA , subjectB: scoreB"
    Return: Dict [str, int | float] -  subject, score 
    '''
    mark_dict = {}
    #separte subject
    for score in mark_str.split(", "):
        #separte score and subject
        score = score.split(": ")
        key = score[0]
        val = score[1]
        #conver score to int or float
        if '.' in val:
            val = float(val)
        else:
            val = int(val)
        mark_dict[key] = val
    return mark_dict


def fix_invalid_value(mark: int | float) -> int | float:
    '''
    turn invalid score into "-inf"
    Paramaters : mark: int | float - score
    Returns : int | float - fixed score
    '''
    mark = float("-inf")
    return mark
  


def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    '''
    recive a str which has mark,convering into new dict
    split value and key ,then check value exceed the limit or not 
    Paramaters: mmark_str: str - eg. "subjectA: scoreA , subjectB: scoreB"
    Return: Dict [str, int | float] -  subject, score 
    '''
    mark_dict = {}
    #separte subject
    for score in mark_str.split(", "):
        #conver score to int or float
        score = score.split(": ")
        key = score[0]
        val = score[1]
        if '.' in val:
            val = float(val)
        else:
            val = int(val)
        #fix exceed value
        if val > 100 or val < 0 :
            val = fix_invalid_value(val)
        mark_dict[key] = val
    return mark_dict

def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, Dict[str, int | float]]:
    '''
    process multiple student marks into dict
    Paramaters : mark_dict: Dict[str, str] - eg. "name" , "subject : score" 
    Returns : Dict[str, Dict[str, int | float]
    '''
    processed_dic = {}
    for name, marks in mark_dict.items():
        processed_dic[name] = mark_str_to_dict_revised(marks)
    return processed_dic

#use split to get the subject avrage mark and numvber of valid and invalid score
#split is the sub_name user choose
def summarize_marks(marks: Dict[str, Dict], split: str) -> dict:
    '''
    summarize marks into "average_mark" , "invalid_count" , "valid_count"
    Paramaters: Dict[str, Dict], split: str
    Returns: dict
    '''
    result = {}
    total = 0.0
    average_mark = 0
    invalid_count = 0
    valid_count = 0
    for name, subject in marks.items():
        check = subject[split]
        #check if score valid
        if check >= 0 and check <= 100:
            total = total + check
            valid_count = valid_count + 1
        else:
            invalid_count = invalid_count + 1
    average_mark = total / valid_count if valid_count else 0.0
    
    result["average_mark"] = average_mark
    result["invalid_count"] = invalid_count
    result["valid_count"] = valid_count
    return result

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # Your testing code goes here
    m = { 
        "Jueqing": "A1: 99, A2: 200, A3: -100",
        "Trang"  : "A1: 300, A2: 100, A3: 100"
    }

    res = process_multiple_students_marks(m)
    print(res)
