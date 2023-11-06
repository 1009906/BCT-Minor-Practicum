import os
from src.user_interface.menu import Menu
from src.system.services.blockchain_service import explore_chain, find_block_to_validate_by_hash, find_last_block_in_chain
from src.user_interface.util.colors import print_error, print_header
from src.user_interface.util.form import prompt_input
from src.user_interface.util.safe_input import safe_input

class LedgerExplorerMenu(Menu):
    _previous_menu = None
    def __init__(self, previous_menu=None):
        super().__init__()
        self._previous_menu = previous_menu
        self.term_size = os.get_terminal_size()
        self._add_label("Menu for exploring the ledger")
        self._add_menu_option(self.view_block_by_hash, "View a specific block by its hash")
        self._add_menu_option(self.view_all_blocks, "View all blocks")
        self._add_menu_option(self.view_all_blocks_paged, "View all blocks (paged)")
        self._add_menu_option(self.view_last_block, "View only the last block")
        self._add_menu_option(self.navigate_back, "Go back to the previous menu")

    def run(self):
        self._title(f"Ledger Explorer Menu")
        self._display_options()
        self._read_input()

    def view_block_by_hash(self):
        self._clear()
        print_header("View block by hash")

        block_hash_to_find = prompt_input(lambda: safe_input("Please enter the block hash: "))
        block = find_block_to_validate_by_hash(block_hash_to_find)

        if block != None:
            print("")
            print(block)
        else:
            print_error(f"Block with hash: {block_hash_to_find} does not exist in the chain.")

        self._back()

    def view_all_blocks(self):
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

    def view_all_blocks_paged(self):
        #TODO TEST PROPERLY
        self._clear()
        print_header("Explore chain (paged)")

        result = explore_chain()

        if len(result) == 0:
            print_error("No blocks in the ledger!")
            self._back()

        current_part = 0
        part_size = 3

        while True:
            self._clear()
            print_header("Explore chain (paged)")
            print(f"Part {current_part + 1} of {len(result) // part_size + 1}")
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
                if current_part < len(result) // part_size:
                    current_part += 1
            elif choice == "2":
                if current_part > 0: 
                    current_part -= 1
            elif choice == "3":
                self.navigate_back()
                break
            else:
                print_error("Invalid choice!")

    def view_last_block(self):
        self._clear()
        print_header("Last block in the chain")

        last_block = find_last_block_in_chain()

        if last_block:
            print("")
            print(last_block)
        else:
            print_error("No blocks in the ledger!")

        self._back()

    def navigate_back(self):
        self._previous_menu.run()