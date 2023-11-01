from src.user_interface.util.colors import *
from .menu import Menu
from src.system.security.login import login, try_login_user, SUCCESSFUL_LOGIN, LOGIN_ATTEMPTS_EXCEEDED
from .util.form import prompt_input
from .util.safe_input import safe_input

class LoginMenu(Menu):
    _previous_menu = None
    def __init__(self, previous_menu):
        self._previous_menu = previous_menu

    def run(self):
        self._title(f"Login")
        login_attempt = 1

        while True:
            username = prompt_input(lambda: safe_input("Please input your Username:"))
            password = prompt_input(lambda: safe_input("Please input your Password:"))

            data = try_login_user(username, password, login_attempt)

            if data[0] == SUCCESSFUL_LOGIN:
                break
            elif data[0] == LOGIN_ATTEMPTS_EXCEEDED:
                return exit("Too many login attempts.")
            else:
                print_error("Incorrect username or password, please try again.")
                login_attempt += 1
                continue

        login(data[1][0], data[1][1], data[1][3], data[1][4], data[1][5],self._previous_menu)