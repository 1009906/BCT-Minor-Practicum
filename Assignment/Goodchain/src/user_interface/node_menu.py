import os
import time
from src.system.services.pool_service import check_pool, check_pool_valid_transactions, cancel_transaction_from_pool, transfer_coins
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input
from src.system.context import Context
from src.user_interface.menu import Menu
from src.system.security.validation import is_float
from src.user_interface.util.colors import convert_to_bold, convert_to_purple, print_error, print_header, print_success, print_warning
from src.user_interface.util.stopwatch import Stopwatch
from src.system.services.node_menu_service import check_balance, check_mined_blocks_status_since_last_login, get_current_password_hashed, update_last_login_date, update_password
from src.system.services.blockchain_service import check_possibility_to_mine, explore_chain, explore_chain_since_date, get_information_of_chain, mine_new_block, succesfull_transactions_since_date
from src.system.security.hashing import hash_password
from src.system.initialize_check import check_blockchain_for_block_to_validate
from src.user_interface.ledger_explorer_menu import LedgerExplorerMenu
from src.system.security.validation import is_digit

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
        self._add_menu_option(self.validate_block, "Validate a block")
        self._add_menu_option(self.show_profile, "Show profile")
        self._add_menu_option(self.edit_password, "Edit password")
        self._add_menu_option(self.log_out, "Log out")

    def run(self, rejected_transactions_list = [], automatic_validation_result = ""):
        self._title(f"Node Menu, Username: {Context.user_name}")
        self._display_options()
        if self.shownotifications:
            self.show_notifications(rejected_transactions_list, automatic_validation_result)
        self._read_input()

    def show_notifications(self, rejected_transactions_list, automatic_validation_result):
        self._clear()
        print_header("Notifications")

        chain_info = get_information_of_chain()
        blocks_added_since_last_login = explore_chain_since_date(Context.last_login_date)
        succesfull_transactions_since_last_login = succesfull_transactions_since_date(Context.last_login_date, Context.user_name)
        mined_blocks_status_since_last_login = check_mined_blocks_status_since_last_login(blocks_added_since_last_login, Context.user_name)

        print(f"Size of blockchain | Blocks: {chain_info[0]} | Transactions: {chain_info[1]}")
        print("Automatic validation result: " + automatic_validation_result)

        if Context.last_login_date is None:
            print("This is your first login, no other notifications to show!")
        else:
            print(f"Last login date: {Context.last_login_date}\n")

            if len(rejected_transactions_list) > 0:
                print_warning("Rejected transactions:")
                for transaction in rejected_transactions_list:
                    print(transaction)
                    print('─' * self.term_size.columns)
            else:
                print_success("No rejected transactions to show.")

            if len(blocks_added_since_last_login) > 0:
                print("Blocks added since last login:")
                for block in blocks_added_since_last_login:
                    print(block)
                    print('─' * self.term_size.columns)
            else:
                print("No blocks added since last login to show.")

            if len(succesfull_transactions_since_last_login) > 0:
                print("Succesfull transactions since last login:")
                for transaction in succesfull_transactions_since_last_login:
                    print(transaction)
                    print('─' * self.term_size.columns)
            else:
                print("No succesfull transactions since last login to show.")

            print(mined_blocks_status_since_last_login)
            is_possible_to_mine = check_possibility_to_mine()
            print(f"\nIs it possible to mine a block: {is_possible_to_mine[0]} | Reason: {is_possible_to_mine[1]}")

        self.shownotifications = False
        update_last_login_date()
        self._back()

    def transfer_coins(self):
        self._clear()
        print_header("Transfer coins")
        print("Enter receivers username or public key.")
        print("[1] Username")
        print("[2] Public key")

        while True:
            transfer_method = prompt_input(lambda: safe_input("Please enter the desired option: "))
            if transfer_method == "1":
                receiver = prompt_input(lambda: safe_input("Please enter the receivers username: "))
                break
            if transfer_method == "2":
                receiver = prompt_input(lambda: safe_input("Please enter the receivers public key: "))
                break
            if transfer_method != "1" or transfer_method != "2":
                print_error("You can only enter 1 or 2!")
                continue
            
        amountCoins = prompt_input(lambda: safe_input("Please enter the amount of coins: "))
        transactionFee = prompt_input(lambda: safe_input("Please enter the transaction fee: "))

        if is_float(amountCoins) == False or is_float(transactionFee) == False:
            print_error("You can only enter numbers!")
            self._back()

        if float(amountCoins) < 0 or float(transactionFee) < 0:
            print_error("You can't enter a negative number!")
            self._back()

        result = transfer_coins(receiver, float(amountCoins), float(transactionFee), transfer_method)

        if result[0]:
            print_success(result[1])
        else:
            print_error(result[1])

        self._back()

    def check_balance(self):
        self._clear()
        print_header("Check balance")
        
        balance = check_balance()
        print(f"Your balance is: {balance}")

        self._back()

    def explore_chain(self):
        ledger_menu = LedgerExplorerMenu(self)
        ledger_menu.run()

    def check_pool(self):
        self._clear()
        print_header("Check pool")

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

        is_possible_to_mine = check_possibility_to_mine()
        if is_possible_to_mine[0] == False:
            print_error(is_possible_to_mine[1])
            self._back()

        available_transaction_ids = []
        get_transactions_pool = check_pool_valid_transactions()

        if len(get_transactions_pool) < 5:
            print_error("There are not enough transactions in the pool! Please try again later.")
            self._back()
        
        if get_transactions_pool:
            print("Transactions in the pool:")
            for i, transaction in enumerate(get_transactions_pool):
                available_transaction_ids.append(str(transaction.id))
                if i % 2 == 0:
                    print(f"\t-> Transaction id: {transaction.id} | Owner: {transaction.owner} | Fee: {transaction.transaction_fee}")
                else:
                    print(convert_to_purple(f"\t-> Transaction id: {transaction.id} | Owner: {transaction.owner} | Fee: {transaction.transaction_fee}"))
        else:
            print_error("No transactions in the pool!")
            self._back()

        while True:
            amount_of_transactions_user_want_to_add = int(prompt_input(lambda: safe_input("\nPlease enter the amount of transactions you want to add to the block: ", is_digit)))
            if amount_of_transactions_user_want_to_add > 10 or amount_of_transactions_user_want_to_add < 5:
                print_error("You can only add a minimum of 5 and a maximum of 10 transactions!")
            else:
                break
        
        print("\nEnter the transaction id's you want to add to the block.")
        print("When you are done, type 'done'.\n")

        transaction_ids = []
        while True:
            transaction_id = prompt_input(lambda: safe_input("Please enter the transaction id: "))
            if len(transaction_ids) == 10:
                print_warning("Maximum of 10 transactions reached!")
                break
            if len(transaction_ids) >= amount_of_transactions_user_want_to_add // 2: #Half of the amount of transactions the user want to add, the rest goes automaticly
                print_warning("Maximum of transactions reached!")
                break
            if transaction_id == "done":
                break
            if transaction_id not in available_transaction_ids: #Check if transaction id is in the pool
                print_error(f"Id: {transaction_id} is not in the pool! Please enter a valid id.")
                continue
            if transaction_id not in transaction_ids: #Check if transaction id is not already added
                transaction_ids.append(transaction_id)
                if len(transaction_ids) >= amount_of_transactions_user_want_to_add // 2:
                    print_warning("Maximum of transactions reached!")
                    break
            else:
                print_error(f"Id: {transaction_id} is already added!")

        print(convert_to_bold("Mining block..."))
        stopwatch = Stopwatch()
        stopwatch.start()

        result = mine_new_block(transaction_ids, amount_of_transactions_user_want_to_add)

        stopwatch.stop()
        stopwatch.print_elapsed_time()

        if result[0]:
            print_success(result[1])
        else:
            print_error(result[1])

        self._back()
    
    def validate_block(self):
        self._clear()
        print_header("Validate block")

        block_hash = prompt_input(lambda: safe_input("Please enter the block hash: "))
        result = check_blockchain_for_block_to_validate(block_hash, False)
        print(result)

        self._back()

    def show_profile(self):
        self._clear()
        print_header("Profile")
        print(Context.__repr__(Context))
        self._back()
    
    def edit_password(self):
        self._clear()
        print_header("Edit password")

        current_password_hashed = get_current_password_hashed()
        if current_password_hashed[0] == False:
            print_error(current_password_hashed[1])
            self._back()

        while True:
            old_password = prompt_input(lambda: safe_input("Please enter your current password: "))
            old_password_hashed = hash_password(old_password)
            if old_password_hashed != current_password_hashed[1]:
                print_error("The password you entered is incorrect! Please try again.")
            else:
                break

        new_password = prompt_input(lambda: safe_input("Please enter your new password: "))
        new_password_hashed = hash_password(new_password)

        if old_password_hashed == new_password_hashed:
            print_error("The new password can't be the same as the old password!")
            self._back()

        result = update_password(new_password_hashed)

        if result[0]:
            print_success(result[1])
        else:
            print_error(result[1])

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