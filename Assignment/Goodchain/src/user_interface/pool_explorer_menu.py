import os
from src.user_interface.menu import Menu
from src.system.services.pool_service import check_pool, find_last_transaction_in_pool, load_transaction_by_id
from src.user_interface.util.colors import print_error, print_header
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input

class PoolExplorerMenu(Menu):
    _previous_menu = None
    def __init__(self, previous_menu=None):
        super().__init__()
        self._previous_menu = previous_menu
        self.term_size = os.get_terminal_size()
        self._add_label("Menu for exploring the pool")
        self._add_menu_option(self.view_transaction_by_id, "View a specific transaction by id")
        self._add_menu_option(self.view_all_transactions, "View all transactions")
        self._add_menu_option(self.view_all_transactions_paged, "View all transactions (paged)")
        self._add_menu_option(self.view_last_transaction, "View only the last transaction")
        self._add_menu_option(self.navigate_back, "Go back to the previous menu")

    def run(self):
        self._title(f"Pool Explorer Menu")
        self._display_options()
        self._read_input()

    def view_transaction_by_id(self):
        self._clear()
        print_header("View transaction by id")

        transaction_id_to_find = prompt_input(lambda: safe_input("Please enter the transaction id: "))
        transaction = load_transaction_by_id(transaction_id_to_find)

        if transaction != None:
            print("")
            print(transaction)
        else:
            print_error(f"Transaction with id: {transaction_id_to_find} does not exist in the pool.")

        self._back()

    def view_all_transactions(self):
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

    def view_all_transactions_paged(self):
        self._clear()
        print_header("Check pool (paged)")

        result = check_pool()

        if len(result) == 0:
            print_error("No transaction in the pool!")
            self._back()

        current_part = 0
        part_size = 3

        while True:
            self._clear()
            pages_length = len(result) // part_size + 1 if len(result) % part_size != 0 else len(result) // part_size

            print_header("Check pool (paged)")
            print(f"Part {current_part + 1} of {pages_length}")
            print("")

            for i in range(current_part * part_size, current_part * part_size + part_size):
                if i < len(result):
                    print(result[i])
                    print('─' * self.term_size.columns)
                else:
                    break

            print("")
            print("[1] Next page")
            print("[2] Previous page")
            print("[3] Go back")
            print("")

            choice = prompt_input(lambda: safe_input("Please enter your choice: "))

            if choice == "1":
                if current_part < pages_length - 1:
                    current_part += 1
            elif choice == "2":
                if current_part > 0: 
                    current_part -= 1
            elif choice == "3":
                self.navigate_back()
                break
            else:
                print_error("Invalid choice!")

    def view_last_transaction(self):
        self._clear()
        print_header("Last transaction in the pool")

        last_transaction = find_last_transaction_in_pool()

        if last_transaction:
            print("")
            print(last_transaction)
        else:
            print_error("No transactions in the pool!")

        self._back()

    def navigate_back(self):
        self._previous_menu.run()