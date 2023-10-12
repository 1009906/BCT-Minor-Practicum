def prompt_input(prompter, allow_empty=False):
    """ Keeps prompting until value is not null """
    while True:
        value = prompter()

        if value or allow_empty:
            return value


def single_choice(prompter, choices):
    """ Keeps prompting until user types in one of the options """
    options = list([option[1] for option in choices])

    while True:
        print(f"Please pick one of the following options: {', '.join(options)}")  # only displays the names, not the ids
        value = prompter()

        for index, choice in enumerate(options):
            if choice == value:
                return choices[index]  # returns entire object, including id and name
