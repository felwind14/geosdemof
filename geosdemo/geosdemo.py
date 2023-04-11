"""Main module."""

import string 
import random
import ipyleaflet

class Map (ipyleaflet.Map):   #we are going to build based on this
     
    def __init__(self, center, zoom, **kwargs) -> None:  #needs to be passed back to the ipyleafclass this is why we put center and zoom in __init__
        
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True   
            
        print(f"this is what the user is providing:{kwargs}") #prints what the user provides       
        super().__init__(center=center, zoom=zoom, **kwargs)      #super means upper label, the class you inherit from. This passes the parameters to geosdemo.py 
    
    def add_search_control(self, position="topleft", **kwargs):  #based on control  example
        """_summary_

        Returns:
            _type_: _description_
        """  
        if "url" not in kwargs:
            kwargs["url"] = "https://nominatim.openstreetmap.org/search?format=json&q={s}"

        
        search_control = ipyleaflet.SearchControl(position= position, **kwargs) #based on example in https://ipyleaflet.readthedocs.io/en/latest/controls/search_control.html
        
        print(f"this is what the user is providing:{kwargs}") 
        self.add_control(search_control)   

    


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


