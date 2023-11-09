from src.system.security.validation import *


def safe_input(label: str = "", validator: Validator = None, default_output=False):
    value = input(label)

    if value == "" and default_output:
        return default_output

    # if not is_valid_length(value): #TODO mag deze code eruit blijven? Volgens mij wel, want er is geen lengte check nodig. Anders gaat het fout in transfer coins met public key
    #     print("Input exceeded maximum length")
    #     return False

    if validator:
        if not validator.check(value):
            print(validator.error_message)
            return False

    return value
