import time
from src.system.context import Context
from src.user_interface.menu import Menu

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
        pass

    def check_balance(self):
        pass

    def explore_chain(self):
        pass

    def check_pool(self):
        pass
        
    def cancel_transaction(self):
        pass

    def mine_block(self):
        pass

    def log_out(self):
        Context.user_id = None
        Context.user_name = None
        Context.private_key = None
        Context.public_key = None

        print("You have been logged out.")
        print("Redirecting to public menu in 2 seconds...")
        time.sleep(2)
        self._previous_menu.run()