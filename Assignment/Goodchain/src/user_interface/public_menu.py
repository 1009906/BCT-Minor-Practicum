from src.system.services.public_menu_service import create_user
from src.user_interface.login_menu import LoginMenu
from src.user_interface.menu import Menu

class PublicMenu(Menu):
    def __init__(self):
        super().__init__()
        self._add_label("Menu for sign up in Goodchain")
        self._add_menu_option(self.login, "Login")
        self._add_menu_option(self.explore_blockchain, "Explore blockchain")
        self._add_menu_option(self.sign_up, "Sign up")
        self._add_menu_option(self.exit, "Exit")


    def run(self):
        self._title(f"Public Menu")
        self._display_options()
        self._read_input()
    
    def login(self):
        login = LoginMenu()
        login.run()

    def explore_blockchain(self):
        pass

    def sign_up(self):
        #TODO Input opvragen vanuit de console.

        result = create_user("admin", "123", "private_key", "public_key")
        print(result[1])
        pass

    def exit(self):
        exit("Exiting the application!")