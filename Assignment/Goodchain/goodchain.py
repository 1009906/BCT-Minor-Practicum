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

    # wallet_server_subprocess = Popen([executable, 'src/system/networking/wallet_server.py'], creationflags=CREATE_NEW_CONSOLE)
    wallet_server_args = []
    wallet_server_command = [executable, 'wallet_server.py'] + wallet_server_args
    wallet_server_subprocess = Popen(wallet_server_command, creationflags=CREATE_NEW_CONSOLE)

    Context.subprocesses.append(wallet_server_subprocess)

    miner_server_args = []
    miner_server_command = [executable, 'miner_server.py'] + miner_server_args
    miner_server_subprocess = Popen(miner_server_command, creationflags=CREATE_NEW_CONSOLE)

    Context.subprocesses.append(miner_server_subprocess)

"""
How to run the application:
-> Navigate to the Goodchain folder.
-> Make sure that in the Context class (context.py) the current_node is set to "node1".
-> Run the following command: python goodchain.py
-> The application is now running on node1. And all the servers are running.

-> Do the same for node2, but change the current_node in the Context class to "node2".
"""

if __name__ == "__main__":
    # check_file_integrity() #TODO Uncomment this line when the application is ready for production.
    Context.db_connection = get_connection()
    start_servers()
    public_menu = PublicMenu()
    public_menu.run()

"""
-> DatabaseClient en DatabaseServer implementeren. Port 5004 en 5005.
-> Context omschrijven met de ports dat het addressen zijn. [('localhost', port), ('localhost', port)]
-> Opt: Niks wijzigen aan de code en toch de node1 naar node2 zetten. Via tekstfile oid?
-> Alles wat nu via het netwerk gaat, heel goed en grondig testen.

Public Menu:
-> 1 Login functie over netwerk updaten van laatste login date in database.
-> 3 Signup functie over netwerk user toevoegen aan database.

Node Menu:
-> 5 Cancel transaction functie over netwerk.
-> 10 Edit password functie over netwerk.
"""