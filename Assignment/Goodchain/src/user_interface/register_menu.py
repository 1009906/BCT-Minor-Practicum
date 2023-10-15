import time
from src.system.services.public_menu_service import create_user
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input
from src.user_interface.menu import Menu


class RegisterMenu(Menu):
    _previous_menu = None
    def __init__(self, previous_menu=None):
        self._previous_menu = previous_menu

    def run(self):
        self._title(f"Register")

        while True:
            username = prompt_input(lambda: safe_input("Please input your Username:"))
            password = prompt_input(lambda: safe_input("Please input your Password:"))

            data = create_user(username, password)

            if data[0] == True:
                #Register is succesfull
                print(data[1])
                print("Redirecting to public menu in 2 seconds...")
                time.sleep(2)
                self._previous_menu.run()
                break
            else:
                print(data[1])
                continue