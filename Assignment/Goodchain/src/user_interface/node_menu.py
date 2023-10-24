import time
from src.system.services.node_menu_service import check_pool, transfer_coins
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input
from src.system.context import Context
from src.user_interface.menu import Menu
from src.system.security.validation import is_digit
from src.user_interface.util.colors import convert_to_bold, print_error, print_header, print_success

class NodeMenu(Menu):
    _previous_menu = None
    def __init__(self, previous_menu=None):
        super().__init__()
        self._previous_menu = previous_menu
        self._add_label("Welcome to goodChain node")
        self._add_menu_option(self.transfer_coins, "Transfer Coins")
        self._add_menu_option(self.check_balance, "Check the Balance")
        self._add_menu_option(self.explore_chain, "Explore the chain")
        self._add_menu_option(self.check_pool, "Check the pool")
        self._add_menu_option(self.cancel_transaction, "Cancel a transaction")
        self._add_menu_option(self.mine_block, "Mine a block")
        self._add_menu_option(self.log_out, "Log out")


    def run(self):
        self._title(f"Node Menu, Username: {Context.user_name}")
        self._display_options()
        self._read_input()

    def transfer_coins(self):
        self._clear()
        print_header("Transfer coins")
        receiver = prompt_input(lambda: safe_input("Please enter the receiver:"))
        amountCoins = prompt_input(lambda: safe_input("Please enter the amount of coins:", is_digit))
        transactionFee = prompt_input(lambda: safe_input("Please enter the transaction fee:", is_digit))

        result = transfer_coins(receiver, int(amountCoins), int(transactionFee)) #TODO Mogen hier ook komma getallen gegeven worden? Anders float gebruiken? Ook in de validator aanpassen

        if result[0]:
            print_success(result[1])
        else:
            print_error(result[1])

        self._back()

    def check_balance(self):
        self._clear()
        print_header("Check balance")
        #TODO Code here!
        self._back()

    def explore_chain(self):
        self._clear()
        print_header("Explore chain")
        #TODO Code here!
        self._back()

    def check_pool(self):
        self._clear()
        print_header("Check pool")

        #TODO Code here!
        result = check_pool()
        if result:
            for transaction in result:
                print(transaction)
        else:
            print_error("No transactions in the pool!")

        self._back()
        
    def cancel_transaction(self):
        self._clear()
        print_header("Cancel transaction")
        #TODO Code here!
        self._back()

    def mine_block(self):
        self._clear()
        print_header("Mine block")
        #TODO Code here!
        self._back()

    def log_out(self):
        Context.user_id = None
        Context.user_name = None
        Context.private_key = None
        Context.public_key = None

        print_success("You have been logged out.")
        print(convert_to_bold("Redirecting to public menu in 2 seconds..."))
        time.sleep(2)
        self._previous_menu.run()