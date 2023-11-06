import os
from src.system.context import Context
from src.user_interface.register_menu import RegisterMenu
from src.user_interface.login_menu import LoginMenu
from src.user_interface.menu import Menu
from src.user_interface.util.colors import convert_to_bold, print_error, print_header
from src.system.security.hashing import save_hashes_to_file
from src.system.services.blockchain_service import explore_chain
from src.user_interface.ledger_explorer_menu import LedgerExplorerMenu

class PublicMenu(Menu):
    def __init__(self):
        super().__init__()
        self.term_size = os.get_terminal_size()
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
        ledger_menu = LedgerExplorerMenu(self)
        ledger_menu.run()       

    def sign_up(self):
        register_menu = RegisterMenu(self)
        register_menu.run()

    def exit(self):
        Context.db_connection.close()
        save_hashes_to_file()
        exit(convert_to_bold("Exiting the application!"))