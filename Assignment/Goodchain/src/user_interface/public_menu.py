from src.system.context import Context
from src.user_interface.register_menu import RegisterMenu
from src.system.services.public_menu_service import create_user
from src.user_interface.login_menu import LoginMenu
from src.user_interface.menu import Menu
from src.user_interface.util.colors import print_header

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
        login = LoginMenu(self)
        login.run()

    def explore_blockchain(self):
        self._clear()
        print_header("Explore blockchain")
        #TODO Code here!
        self._back()        

    def sign_up(self):
        register_menu = RegisterMenu(self)
        register_menu.run()

    def exit(self):
        Context.db_connection.close()
        exit("Exiting the application!")