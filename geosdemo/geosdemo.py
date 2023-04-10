"""Main module."""

import string 
import random

#Created on youtube lesson week 10
def generate_random_string(length, upper= False, digits = False, punctuation= False):
    
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