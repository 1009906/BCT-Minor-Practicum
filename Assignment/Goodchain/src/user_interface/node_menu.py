import os
import time
from src.system.services.pool_service import check_pool_valid_transactions, cancel_transaction_from_pool, transfer_coins
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input
from src.system.context import Context
from src.user_interface.menu import Menu
from src.system.security.validation import is_float
from src.user_interface.util.colors import convert_to_bold, convert_to_green, convert_to_purple, convert_to_red, print_error, print_header, print_success, print_warning
from src.user_interface.util.stopwatch import Stopwatch
from src.system.services.node_menu_service import check_balance, check_mined_blocks_status_since_last_login, get_current_password_hashed, update_last_login_date, update_password
from src.system.services.blockchain_service import check_possibility_to_mine, explore_chain_since_date, get_information_of_chain, mine_new_block, succesfull_transactions_since_date, tamper_proof_check
from src.system.security.hashing import hash_password
from src.system.initialize_check import check_blockchain_for_block_to_validate
from src.user_interface.ledger_explorer_menu import LedgerExplorerMenu
from src.system.security.validation import is_digit
from src.user_interface.pool_explorer_menu import PoolExplorerMenu

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
        self._add_menu_option(self.validate_chain, "Validate the chain")
        self._add_menu_option(self.show_profile, "Show profile")
        self._add_menu_option(self.edit_password, "Edit password")
        self._add_menu_option(self.log_out, "Log out")

    def run(self, rejected_transactions_list = [], automatic_validation_result = "", tamper_proof_result = (None, None)):
        self._title(f"Node Menu, Username: {Context.user_name}")
        self._display_options()
        if self.shownotifications:
            self.show_notifications(rejected_transactions_list, automatic_validation_result, tamper_proof_result)
        self._read_input()

    def show_notifications(self, rejected_transactions_list, automatic_validation_result, tamper_proof_result):
        self._clear()
        print_header("Notifications")

        chain_info = get_information_of_chain()
        if Context.last_login_date is not None:
            blocks_added_since_last_login = explore_chain_since_date(Context.last_login_date)
            succesfull_transactions_since_last_login = succesfull_transactions_since_date(Context.last_login_date, Context.user_name)
            mined_blocks_status_since_last_login = check_mined_blocks_status_since_last_login(blocks_added_since_last_login, Context.user_name)

        print(f"Size of blockchain | Blocks: {chain_info[0]} | Transactions: {chain_info[1]}\n")
        print("Automatic validation result: " + automatic_validation_result + "\n")

        if Context.last_login_date is None:
            print("This is your first login, no other notifications to show!")
        else:
            print(f"Last login date: {Context.last_login_date}\n")

            if len(rejected_transactions_list) > 0:
                print_error("Rejected transactions:")
                for transaction in rejected_transactions_list:
                    print(transaction)
                    print('─' * self.term_size.columns)
            else:
                print_success("No rejected transactions to show.\n")

            if len(blocks_added_since_last_login) > 0:
                print_success("Blocks added since last login:")
                for block in blocks_added_since_last_login:
                    print(block)
                    print('─' * self.term_size.columns)
            else:
                print_warning("No blocks added since last login to show.\n")

            if len(succesfull_transactions_since_last_login) > 0:
                print_success("Succesfull transactions since last login:")
                for transaction in succesfull_transactions_since_last_login:
                    print(transaction)
                    print('─' * self.term_size.columns)
            else:
                print_warning("No succesfull transactions since last login to show.\n")

            print(mined_blocks_status_since_last_login)
            is_possible_to_mine = check_possibility_to_mine()
            print(f"\nIs it possible to mine a block: {is_possible_to_mine[0]} | Reason: {is_possible_to_mine[1]}")

            if tamper_proof_result[0] != None:
                result = "\nIs blockchain tamperd: "
                if tamper_proof_result[0] == True:
                    result += convert_to_red(f"{tamper_proof_result[0]} | Reason: {tamper_proof_result[1]}")
                else:
                    result += convert_to_green(f"{tamper_proof_result[0]} | Reason: {tamper_proof_result[1]}")

                print(result)

        self.shownotifications = False
        update_last_login_date()
        self._back()

    def transfer_coins(self):
        self._clear()
        print_header("Transfer coins")
        print("Enter receivers username. ")

        receiver = prompt_input(lambda: safe_input("Please enter the receivers username: "))
            
        amountCoins = prompt_input(lambda: safe_input("Please enter the amount of coins: "))
        transactionFee = prompt_input(lambda: safe_input("Please enter the transaction fee: "))

        if is_float(amountCoins) == False or is_float(transactionFee) == False:
            print_error("You can only enter numbers!")
            self._back()

        if float(amountCoins) <= 0 or float(transactionFee) < 0:
            print_error("You can't enter a negative number or enter a amount of coins of 0!")
            self._back()

        result = transfer_coins(receiver, float(amountCoins), float(transactionFee))

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
        pool_menu = PoolExplorerMenu(self)
        pool_menu.run()
        
    def cancel_transaction(self):
        self._clear()
        print_header("Cancel transaction")

        transaction_id = prompt_input(lambda: safe_input("Please enter the transaction id:"))
        result = cancel_transaction_from_pool(transaction_id)

        if result:
            print_success("Transaction is found and removed from the pool!")
        else:
            print_error("Transaction is not found in the pool or you are not the owner of the transaction!")

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

        result = mine_new_block(transaction_ids, amount_of_transactions_user_want_to_add)

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

    def validate_chain(self):
        self._clear()
        print_header("Validate chain")

        tamper_proof_result = tamper_proof_check()
        result = "\nIs blockchain tamperd: "
        if tamper_proof_result[0] == True:
            result += convert_to_red(f"{tamper_proof_result[0]} | Reason: {tamper_proof_result[1]}")
        else:
            result += convert_to_green(f"{tamper_proof_result[0]} | Reason: {tamper_proof_result[1]}")

        print(result)
        self._back()

    def show_profile(self):
        self._clear()
        print_header("Profile")
        print(Context.__repr__(Context))
        print("Public key: ")
        print(fr"{str(Context.public_key, encoding='utf-8')}")
        print("Private key: ")
        print(fr"{str(Context.private_key, encoding='utf-8')}")
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