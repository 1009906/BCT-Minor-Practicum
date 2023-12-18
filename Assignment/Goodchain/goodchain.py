from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

from src.user_interface.public_menu import PublicMenu
from src.system.connection import get_connection
from src.system.context import Context
from src.system.security.hashing import calculate_file_hash, load_hashes_from_file
from src.user_interface.util.colors import convert_to_bold, print_error

def check_file_integrity():
    file_is_changed = False
    error_message = ""
    old_database_hash, old_ledger_hash, old_pool_hash = load_hashes_from_file()
    
    new_database_hash = calculate_file_hash(Context.database_path)
    if new_database_hash != old_database_hash:
        file_is_changed = True
        error_message += "Database file has changed.\n"

    new_ledger_hash = calculate_file_hash(Context.ledger_path)
    if new_ledger_hash != old_ledger_hash:
        file_is_changed = True
        error_message += "Ledger file has changed.\n"

    new_pool_hash = calculate_file_hash(Context.pool_path)
    if new_pool_hash != old_pool_hash:
        file_is_changed = True
        error_message += "Pool file has changed.\n"
    
    if file_is_changed:
        print_error(error_message)
        exit(convert_to_bold("Exiting the application!"))

def start_servers():
    #TODO Start all servers, maybe pass processes to public menu and stop them when exiting the application.

    wallet_server_subprocess = Popen([executable, 'src/system/networking/wallet_server.py'], creationflags=CREATE_NEW_CONSOLE)
    # wallet_server_args = []
    # wallet_server_command = [executable, 'src/system/networking/wallet_server.py'] + wallet_server_args
    # wallet_server_subprocess = Popen(wallet_server_command, creationflags=CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    check_file_integrity()
    Context.db_connection = get_connection()
    start_servers()
    public_menu = PublicMenu()
    public_menu.run()