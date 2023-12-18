import os
import uuid #TODO REMOVE
from src.system.context import Context
from src.user_interface.register_menu import RegisterMenu
from src.user_interface.login_menu import LoginMenu
from src.user_interface.menu import Menu
from src.user_interface.util.colors import convert_to_bold
from src.system.security.hashing import save_hashes_to_file
from src.user_interface.ledger_explorer_menu import LedgerExplorerMenu
from src.system.blockchain.Signature import generate_keys #TODO REMOVE
from src.system.networking.wallet_client import WalletClient #TODO REMOVE
from src.system.blockchain.Transaction import Tx #TODO REMOVE
from cryptography.hazmat.primitives import serialization #TODO REMOVE

class PublicMenu(Menu):
    def __init__(self):
        super().__init__()
        self.term_size = os.get_terminal_size()
        self._add_label("Menu for sign up in Goodchain")
        self._add_menu_option(self.login, "Login")
        self._add_menu_option(self.explore_blockchain, "Explore blockchain")
        self._add_menu_option(self.sign_up, "Sign up")
        self._add_menu_option(self.exit, "Exit")
        self._add_menu_option(self.send_message_to_server_test, "Send message to server test") #TODO REMOVE


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

    #TODO REMOVE to bottom after testing
    def create_test_transaction(self):
        alex_prv, alex_pbc = generate_keys()
        mike_prv, mike_pbc = generate_keys()

        alex_prv_ser = alex_prv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )
    
        alex_pbc_ser = alex_pbc.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
    
        mike_pbc_ser = mike_pbc.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

        Tx1 = Tx(uuid.uuid1(), "Alex", "Mike", 0.1)
        Tx1.add_input(alex_pbc_ser, 2.3)
        Tx1.add_output(mike_pbc_ser, 1.0)
        Tx1.sign(alex_prv_ser)

        return Tx1

    def send_message_to_server_test(self):
        Context.user_name = Context.current_node
        new_transaction = self.create_test_transaction()
        wallet_client = WalletClient()
        wallet_client.handle_server(new_transaction)