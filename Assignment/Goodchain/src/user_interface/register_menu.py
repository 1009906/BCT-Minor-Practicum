import time
from src.system.services.public_menu_service import create_user, signup_reward
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input
from src.user_interface.menu import Menu
from src.user_interface.util.colors import convert_to_bold, print_error, print_success

class RegisterMenu(Menu):
    _previous_menu = None
    def __init__(self, previous_menu=None):
        self._previous_menu = previous_menu

    def run(self):
        self._title(f"Register")

        while True:
            try:
                username = prompt_input(lambda: safe_input("Please input your Username: "))
                password = prompt_input(lambda: safe_input("Please input your Password: "))

                data = create_user(username, password)
                if data[0] == True:
                    #Register is succesfull
                    print_success(data[1])
                    print("Creating signup reward transaction...")

                    result = signup_reward(username)
                    if result[0] == True:
                        print_success(result[1])
                    else:
                        print_error(result[1])

                    print(convert_to_bold("\nRedirecting to public menu in 2 seconds..."))
                    time.sleep(2)
                    break
                else:
                    print_error(data[1])
                    continue
            except:
                print_error("Something went wrong. Please try again.")
                continue
        return self._previous_menu.run()