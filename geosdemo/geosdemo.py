"""Main module."""

import string 
import random

#Created on youtube lesson week 10
def generate_random_string(length= 10, upper= False, digits = False, punctuation= False):
    """Generates a random string of a given length

    Args:
        length (int, optional): Length of the string. Defaults to 10.
        upper (bool, optional): Wheater to include uppercase. Defaults to False.
        digits (bool, optional): _description_. Defaults to False.
        punctuation (bool, optional): _description_. Defaults to False.

    Returns:
        str: The generated string
    """    
    letters = string.ascii_lowercase
    if upper:
         letters += string.ascii_uppercase
    if digits:
         letters += string.digits
    if punctuation:
         letters += string.pun
        
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_lucky_number(length= 1):
    """_summary_

    Args:
        length (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """    
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)


