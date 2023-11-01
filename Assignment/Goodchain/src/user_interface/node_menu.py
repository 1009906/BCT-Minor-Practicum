import os
import time
from src.system.services.pool_service import check_pool, check_pool_valid_transactions, cancel_transaction_from_pool, transfer_coins
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input
from src.system.context import Context
from src.user_interface.menu import Menu
from src.system.security.validation import is_digit
from src.user_interface.util.colors import convert_to_bold, print_error, print_header, print_success, print_warning
from src.user_interface.util.stopwatch import Stopwatch
from src.system.services.node_menu_service import update_last_login_date
from src.system.services.blockchain_service import explore_chain, mine_new_block

class NodeMenu(Menu):
    _previous_menu = None
    def __init__(self, previous_menu=None):
        super().__init__()
        self._previous_menu = previous_menu
        self.term_size = os.get_terminal_size()
        self.shownotifications = True
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
        if self.shownotifications:
            self.show_notifications()
        self._read_input()

    def show_notifications(self):
        self._clear()
        print_header("Notifications")
        if Context.last_login_date is None:
            print("This is your first login, no notifications to show!")
        else:
            print(f"Last login date: {Context.last_login_date}")

        self.shownotifications = False
        update_last_login_date()
        self._back()

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
        result = explore_chain()
        if result:
            for block in result:
                print(block)
                print('─' * self.term_size.columns)
        else:
            print_error("No blocks in the ledger!")
        self._back()

    def check_pool(self):
        self._clear()
        print_header("Check pool")

        #TODO Code here!
        result = check_pool()
        if result:
            for transaction in result:
                print(transaction)
                print('─' * self.term_size.columns)
        else:
            print_error("No transactions in the pool!")

        self._back()
        
    def cancel_transaction(self):
        self._clear()
        print_header("Cancel transaction")
        #TODO Code here!
        transaction_id = prompt_input(lambda: safe_input("Please enter the transaction id:"))
        result = cancel_transaction_from_pool(transaction_id)

        if result:
            print_success("Transaction is found and removed from the pool!")
        else:
            print_error("Transaction is not found in the pool!")

        self._back()

    def mine_block(self):
        self._clear()
        print_header("Mine block")
        available_transaction_ids = []

        get_transactions_pool = check_pool_valid_transactions()

        if len(get_transactions_pool) < 5: #TODO Maybe comment this out for testing purposes
            print_error("There are not enough transactions in the pool! Please try again later.")
            self._back()
        
        if get_transactions_pool:
            print("Transactions in the pool:")
            for transaction in get_transactions_pool:
                available_transaction_ids.append(str(transaction.id))
                print(f"\t-> Transaction id: {transaction.id} | Owner: {transaction.owner} | Fee: {transaction.transaction_fee}")
        else:
            print_error("No transactions in the pool!")
            self._back()
            
        print("\nEnter the transaction id's you want to add to the block.")
        print("When you are done, type 'done'.\n")

        transaction_ids = []
        while True:
            transaction_id = prompt_input(lambda: safe_input("Please enter the transaction id: "))
            if len(transaction_ids) == 10:
                print_warning("Maximum of 10 transactions reached!")
                break
            if transaction_id == "done":
                if len(transaction_ids) < 5:
                    print_warning("Choose at least 5 transactions!")
                    continue
                break
            if transaction_id not in available_transaction_ids: #Check if transaction id is in the pool
                print_error(f"Id: {transaction_id} is not in the pool! Please enter a valid id.")
                continue
            if transaction_id not in transaction_ids: #Check if transaction id is not already added
                transaction_ids.append(transaction_id)
            else:
                print_error(f"Id: {transaction_id} is already added!")

        print(transaction_ids) #TODO Remove this line

        print(convert_to_bold("Mining block..."))
        stopwatch = Stopwatch()
        stopwatch.start()

        #TODO Implement mining function that mines a block with the given transaction id's
        result = mine_new_block(transaction_ids)

        stopwatch.stop()
        stopwatch.print_elapsed_time()

        #TODO Do someting with the result

        self._back()

    def log_out(self):
        Context.user_id = None
        Context.user_name = None
        Context.private_key = None
        Context.public_key = None
        Context.last_login_date = None

        print_success("You have been logged out.")
        print(convert_to_bold("Redirecting to public menu in 2 seconds..."))
        time.sleep(2)
        self._previous_menu.run()