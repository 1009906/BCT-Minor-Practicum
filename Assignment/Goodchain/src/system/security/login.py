from src.system.security.hashing import hash_password
from src.user_interface.node_menu import NodeMenu
from src.system.context import Context

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


def login(user_id, user_name, private_key, public_key):
    Context.user_id = user_id
    Context.user_name = user_name
    Context.private_key = private_key
    Context.public_key = public_key

    node_menu = NodeMenu()
    node_menu.run()