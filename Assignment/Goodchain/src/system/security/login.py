from datetime import datetime
from src.system.security.hashing import hash_password
from src.user_interface.node_menu import NodeMenu
from src.system.context import Context
from src.system.initialize_check import check_blockchain_for_block_to_validate, check_pool_for_invalid_transactions_of_logged_in_user
from src.user_interface.util.colors import print_success

LOGIN_MAX_ATTEMPTS = 3

# kind of like an enum
INCORRECT_LOGIN = 'UNSUCCESSFUL_LOGIN'
SUCCESSFUL_LOGIN = 'SUCCESSFUL_LOGIN'
LOGIN_ATTEMPTS_EXCEEDED = 'LOGIN_ATTEMPTS_EXCEEDED'


def try_login_user(username, password, attempt):
    con = Context.db_connection
    c = con.cursor()
    
    hashed_password = hash_password(password)
    c.execute("SELECT * FROM users WHERE Name=? AND Password=?", (username, hashed_password))

    login_result = c.fetchone()

    if not login_result and attempt > 2:
        # log("Login attempts exceeded", f"Successful login using 'Username: {username}, 'Password: {password}'", True)
        return LOGIN_ATTEMPTS_EXCEEDED, None
    elif login_result:
        # log("Successful Login", f"Successful login using \"Username: '{username}', Password: '{password}'\"")
        return SUCCESSFUL_LOGIN, login_result
    else:
        # log("Unsuccessful Login", f"Unsuccessful login using 'Username: {username}, 'Password: {password}'")
        return INCORRECT_LOGIN, None


def login(user_id, user_name, private_key, public_key, last_login_date, previous_menu):
    last_login_date = datetime.strptime(last_login_date, '%Y-%m-%d %H:%M:%S.%f') if last_login_date != None else None
    Context.user_id = user_id
    Context.user_name = user_name
    Context.private_key = private_key
    Context.public_key = public_key
    Context.last_login_date = last_login_date

    print("Checking pool for invalid transactions...")
    rejected_transactions_list = check_pool_for_invalid_transactions_of_logged_in_user()
    print_success("Done checking pool for invalid transactions...")

    print("Checking blockchain for blocks to validate...")
    automatic_validation_result = check_blockchain_for_block_to_validate()
    print_success("Done checking blockchain for blocks to validate...")

    node_menu = NodeMenu(previous_menu)
    node_menu.run(rejected_transactions_list, automatic_validation_result)