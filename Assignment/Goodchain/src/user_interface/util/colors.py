class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_error(message):
    print(f"{bcolors.FAIL}{message}{bcolors.ENDC}")

def print_success(message):
    print(f"{bcolors.OKGREEN}{message}{bcolors.ENDC}")

def print_header(message):
    print(f"{bcolors.HEADER}{message}{bcolors.ENDC}")

def convert_to_bold(message):
    return f"{bcolors.BOLD}{message}{bcolors.ENDC}"