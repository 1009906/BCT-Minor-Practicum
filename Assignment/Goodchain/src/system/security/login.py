from src.system.context import Context
# from src.system.roles.roles import Roles
# from src.user_interface.advisor_menu import AdvisorMenu
# from src.user_interface.super_admin_menu import SuperAdminMenu
# from src.user_interface.system_admin_menu import SystemAdminMenu
# from src.system.logging.logger import log

LOGIN_MAX_ATTEMPTS = 3

# kind of like an enum
INCORRECT_LOGIN = 'UNSUCCESSFUL_LOGIN'
SUCCESSFUL_LOGIN = 'SUCCESSFUL_LOGIN'
LOGIN_ATTEMPTS_EXCEEDED = 'LOGIN_ATTEMPTS_EXCEEDED'


def try_login_user(username, password, attempt):
    con = Context.db_connection
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

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


def login(user_id, name, role_id):
    print(f"{user_id}, {name}, {role_id}")
    pass
#     """ Opens a menu based on the role id of the logged in employee """
#     Context.user_id = user_id
#     Context.user_name = name

#     log('Login', f'User: {name}#{user_id} has logged into the system')

#     if role_id is Roles.SUPER_ADMIN.value:
#         log("SuperAdminMenu Run", f"Super Admin Menu Run")
#         SuperAdminMenu().run()
#     elif role_id is Roles.SYSTEM_ADMIN.value:
#         log("SystemAdminMenu Run", f"System Admin Menu Run")
#         SystemAdminMenu().run()
#     elif role_id is Roles.ADVISOR.value:
#         log("Advisor Run", f"Advisor Run")
#         AdvisorMenu().run()
#     else:
#         log("Login Error", f"Login Error")
#         raise LoginError("Error from 'def _open_menu'. Something possibly went wrong with the role_id.")
