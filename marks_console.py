from typing import Dict

def fix_invalid_value(mark: int | float) -> int | float:
    """
    check val if its valid or not 

    Params:
        mark (int | float): score.

    Returns:
        int | float: -inf
    """
    mark = float("-inf")
    return mark


def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    '''
    revised version
    sonvert a student's mark string into a dict, checking for invalid values.
    use fucniton fix_invalid_value to deal with invaild score
    
    Params:
    mark_str (str): eg: "A1: 90, A2: 85"

    Returns:
        Dict[str, int | float]: Mapping assignment to score 
    '''
    mark_dict = {}
    # split by ", " to get each "key: value"
    for score in mark_str.split(", "):
        # split by ": " to get each sub and socre
        score = score.split(": ")
        key = score[0]
        val = score[1]

        #if theres "." change the tpye to float
        if '.' in val:
            val = float(val)
        else:
            val = int(val)
        #if given aal is out of range[0,100] , flag this as invalid , call "fix_invalid_value"
        if val > 100 or val < 0 :
            val = fix_invalid_value(val)
        mark_dict[key] = val
    return mark_dict



def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, Dict[str, int | float]]:
    """
    deal with multiple students mark into nested dicts.

    Params:
        mark_dict (Dict[str, str]): mapping student_name and raw mark string.

    Returns:
        Dict[str, Dict[str, int | float]]: Mapping student_name and (sub -> score).
    """
    processed_dic = {}
    for name, marks in mark_dict.items():
        processed_dic[name] = mark_str_to_dict_revised(marks)
    return processed_dic

#use split to get the subject avrage mark and numvber of valid and invalid score
#split is the sub_name user choose
def summarize_marks(marks: Dict[str, Dict], split: str) -> dict:
    """
    Compute average, valid count, and invalid count for a given assignment key.

    Params:
        marks (Dict[str, Dict]): eg. {"Jueqing": {"A1": 99, "A2": -inf}}
        split (str): sub to summarize (e.g. "A1").

    Returns:
        dict: {"average_mark": float, "invalid_count": int, "valid_count": int }
    """
    result = {}
    total = 0.0
    average_mark = 0
    invalid_count = 0
    valid_count = 0
    for name, subject in marks.items():
        # if split in subject 
        check = subject[split]

        #valid value are b/t [0,100]
        if check >= 0 and check <= 100:
            total = total + check
            valid_count = valid_count + 1
        else:
            invalid_count = invalid_count + 1
    #using valid marks to compute avarege_mark
    average_mark = total / valid_count if valid_count else 0.0
    
    result["average_mark"] = average_mark
    result["invalid_count"] = invalid_count
    result["valid_count"] = valid_count
    return result



def exit_option(leave : bool)-> int:
    """
    #user choose option Exit , return 0 to let the main knows to leave marking system

    Params:
        leave (bool): whether the user wants to leave.

    Returns:
        int: 0.
    """
    if leave == True:
        print("See u!")
    return 0
    
#check if name match the password
def account_verify(user_info: dict, valid_login: int) -> tuple[bool, str] :
    """
    verify username and password against user_info 
    username are case-insensitive 

    Params:
        user_info (dict): Mapping of username -> password.
        valid_login (int): The menu input indicating a login attempt (not used in logic here).

    Returns:
        tuple[bool, str]: (is_valid, username_lowercased)
                          If valid, True and the matched username (lowercased).
                          If invalid, False and the entered username (lowercased).
    """

    acc_name = str(input("Please key your account name: ")).lower()
    acc_pass = str(input("Please key your password: "))
    for key, value in user_info.items():
        #use function lower for name so case wont cause error
        if acc_name == key.lower() and acc_pass == value:
            return (True, acc_name)
    #return acc_name for later in interface to print out
    return (False,acc_name)


def interface(user_name: str, mark_unprocessed: dict)-> int:
    """
    main user interface, show all the options for user inclugin , Exit, Re-Login, Show records, Summarization.

    Params:
        user_name (str): username(in lowercased) returned by account_verify.
        mark_unprocessed (dict): 

    Returns:
        int: The selected option .
    """
    name = str(user_name)
    #capitalize the first word of the name
    fixed_username = name.capitalize()
    #loop until user exit or relogin 
    while(True):
        print(f"Welcome {fixed_username}")
        print("Please choose one option below:\n"
        "1.Exit\n"
        "2.Re-Login\n"
        "3.Show mark records\n"
        "4.Show summarization\n")
        choice = int(input("Your choice (number only): "))
        #user choose exit
        if choice == 1:
            exit_option(True)
            return choice
        #user choose relogin
        elif choice == 2:
            print("You have logged off successfully!")
            return choice
        #for options 3 and 4, creat their own function marks_records and summarization
        elif choice == 3:
            marks_records(mark_unprocessed) 
        elif choice == 4:
            summarization(mark_unprocessed)  
        else:
            continue

def marks_records(mark_unprocessed: dict):
    """
    print the processed mark records for all students.

    Params:
        mark_unprocessed (dict)

    Returns:
        None
    """
    fixed = process_multiple_students_marks(mark_unprocessed)
    print("Results:")
    for name , sub in fixed.items():
        print(f"{name}:")
        for sub_name, score in sub.items():
            print(f"    {sub_name}: {score}")

def summarization(mark_unprocessed):
    """
    get assignment key, then print average/valid/invalid for that assignment.

    Params:
        mark_unprocessed (dict)

    Returns:
        None
    """
    fixed  = process_multiple_students_marks(mark_unprocessed)
    #creat a set to store the fiexd dict's key of the value, which is the name of subject
    sub_set = set()
    for sub in fixed.values():
        sub_set.update(sub.keys())
    print(f"Available Assignments: {sub_set}")

    choosen_assigment = str(input("The Assignment you want to check (e.g., A1): "))
    result = summarize_marks(fixed, choosen_assigment)
    print(f"Results For {choosen_assigment}:")
    print(f"average_mark: {result.get('average_mark')}")
    print(f"invalid_count: {result.get('invalid_count')}")
    print(f"valid_count: {result.get('valid_count')}")

def main(user_info, mark_unprocessed) -> int:
    """
    initial display and determin user input valid or not

    Params:
        user_info (dict): username -> password (for account_verify).
        mark_unprocessed (dict):

    Returns:
        int: always 0.
    """
    condition = True
    while(condition):
        print("Welcome to the Mark system v0.0!\n"
        "Please Login:\n"
        "1.Exit\n"
        "2.Login\n")
        login_input = int(input("Your choice (number only): "))
        #valid input
        if login_input == 1 or login_input == 2:
            if login_input ==1:
                if exit_option(True) == 0:
                    break
            #vaild and its not exit, check acc_name and acc_pass
            verify_respond, user_name = account_verify(user_info, login_input)
            # password wrong
            if verify_respond == False:
                print("Incorrect username or password!")
            else:
                #leave loop
                condition = False
                interface_choice = interface(user_name ,mark_unprocessed)
                #user choose relogin
                if interface_choice == 2:
                    condition = True
        else:
            continue
    return 0
                    
                
                

    


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    user_info = {
        "Jueqing": "Jueqing123",
        "apple" : "A"
    }
    mark_unprocessed = {
        "Jueqing": "A1: 99, A2: 200, A3: -100",
        "Trang"  : "A1: 300, A2: 100, A3: 100"
    }
    main(user_info, mark_unprocessed)
