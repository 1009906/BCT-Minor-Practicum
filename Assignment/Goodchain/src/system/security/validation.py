import re
from src.user_interface.util.colors import convert_to_red

class Validator:
    def __init__(self, check, error_message):
        self.error_message = error_message
        self.check = check

# validation objects, contains regexes and error messages
is_digit = Validator(
    lambda string: match_regex("^[0-9]+$", string), convert_to_red("ERROR: Input must be an integer."))

# check is string is under 255 characters
def is_valid_length(string):
    return len(string) < 255

# utility function for checking whether a string matches a pattern
def match_regex(regex, string):
    pattern = re.compile(regex)
    res = re.match(pattern, string)
    return bool(res)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False