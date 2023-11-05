import os
import time
from src.system.services.pool_service import check_pool, check_pool_valid_transactions, cancel_transaction_from_pool, transfer_coins
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input
from src.system.context import Context
from src.user_interface.menu import Menu
from src.system.security.validation import is_digit
from src.user_interface.util.colors import convert_to_bold, convert_to_purple, print_error, print_header, print_success, print_warning
from src.user_interface.util.stopwatch import Stopwatch
from src.system.services.node_menu_service import check_balance, check_mined_blocks_status_since_last_login, update_last_login_date
from src.system.services.blockchain_service import explore_chain, explore_chain_since_date, find_block_to_validate, get_information_of_chain, mine_new_block, succesfull_transactions_since_date

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
        self._add_menu_option(self.show_profile, "Show profile")
        self._add_menu_option(self.log_out, "Log out")

    def run(self, rejected_transactions_list = [], automatic_validation_result = ""):
        self._title(f"Node Menu, Username: {Context.user_name}")
        self._display_options()
        if self.shownotifications:
            self.show_notifications(rejected_transactions_list, automatic_validation_result)
        self._read_input()

    def show_notifications(self, rejected_transactions_list, automatic_validation_result):
        """
        ● General information of the blockchain (the size of blockchain, number of transactions, etc.) -> Done
        ● Users mined block status (if a user already mined a block and the block was on pending for verification by other nodes -> Done
        ● Any block which was on pending and is confirmed or rejected by this user after login -> Done
        ● Reward notification if there was any reward pending for confirmation from other nodes
        ● New added block(s) since the last login (already confirmed by other nodes or waiting for a confirmation) -> Done
        ● Rejected transactions of the user -> Done
        ● Successful transactions of the user -> Done
        """	
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

        self.shownotifications = False
        update_last_login_date()
        self._back()

    def transfer_coins(self):
        self._clear()
        print_header("Transfer coins")
        receiver = prompt_input(lambda: safe_input("Please enter the receiver: "))
        amountCoins = prompt_input(lambda: safe_input("Please enter the amount of coins: ", is_digit))
        transactionFee = prompt_input(lambda: safe_input("Please enter the transaction fee: ", is_digit))

        result = transfer_coins(receiver, int(amountCoins), int(transactionFee)) #TODO Mogen hier ook komma getallen gegeven worden? Anders float gebruiken? Ook in de validator aanpassen

        if result[0]:
            print_success(result[1])
        else:
            print_error(result[1])

        self._back()

    def check_balance(self):
        self._clear()
        print_header("Check balance")
        # chain = explore_chain()
        # total_in = 0
        # total_out = 0
        # for block in chain:
        #     for tx in block.data:
        #         for addr, amt in tx.inputs:
        #             if addr == Context.public_key:
        #                 total_in = total_in + amt
        #         for addr, amt in tx.outputs:
        #             if addr == Context.public_key:    
        #                 total_out = total_out + amt

        # print_success(f"Your balance is: {total_out - total_in}")
        
        balance = check_balance()
        print(f"Your balance is: {balance}")

        self._back()

    def explore_chain(self):
        self._clear()
        print_header("Explore chain")
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

        #Add check if there is no block in pending state
        find_pending_block = find_block_to_validate()
        if find_pending_block is not None:
            print_error("There is still a block in pending state! Please wait until it is validated.")
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

        print(convert_to_bold("Mining block..."))
        stopwatch = Stopwatch()
        stopwatch.start()

        result = mine_new_block(transaction_ids)

        stopwatch.stop()
        stopwatch.print_elapsed_time()

        if result[0]:
            print_success(result[1])
        else:
            print_error(result[1])

        self._back()

    def show_profile(self):
        self._clear()
        print_header("Profile")
        print(Context.__repr__(Context))
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