import re

class Validator:
    def __init__(self, check, error_message):
        self.error_message = error_message
        self.check = check


# validation objects, contains regexes and error messages
is_digit = Validator(
    lambda string: match_regex("^[0-9]+$", string), "ERROR: Input must be an integer.")

is_username = Validator(
    lambda string: match_regex("^[a-zA-Z][a-zA-Z0-9_'.]{5,10}$", string),
    "Error: Incorrect username format. Username must be between 6 and 10 characters and "
    "can contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.).")

is_password = Validator(
    lambda string: match_regex("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$", string),
    "Error: Incorrect password format. Password must be between 8 and 30 characters and "
    "must have a combination of at least one lowercase letter, one uppercase letter, "
    "one digit, and one special character such as ~!@#$%&_-+=`|\(){}[]:;'<>,.?/")

not_empty = Validator(
    lambda string: string,
    "Error: Input is empty. Please enter a valid input")


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
