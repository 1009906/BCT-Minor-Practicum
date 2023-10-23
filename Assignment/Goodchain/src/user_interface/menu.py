import os
from abc import abstractmethod

from src.user_interface.util.colors import bcolors
from .util.safe_input import safe_input
from src.system.security.validation import is_digit


class Menu:  # abstract class
    _previous_step = None

    def __init__(self):
        self._options = []
        self._label = []

    @abstractmethod
    def run(self):
        """ Override method, every Menu class must implement this method """
        pass

    def _title(self, title):
        """ Usually executed at the top of a `run` method. Clears the console and the prints a message """
        self._clear()
        print(title)

    def _back(self):
        """ Usually ran after a certain task is completed, takes the user back a step"""
        safe_input(f"\n{bcolors.BOLD}Press Enter to go back to the Menu.{bcolors.ENDC}")
        self.run()

    def _add_label(self, display):
        if self._options:
            highest_listing = max([number[1] for number in self._options]) + 1
            self._label.append((highest_listing, display))
        else:
            self._label.append((1, display))

    def _add_menu_option(self, action, display):
        self._options.append((action, len(self._options) + 1, display))

    def _read_input(self):
        """ Reads input and executes a function that corresponds to that specified input """
        try:
            value = safe_input("", is_digit)

            for option in self._options:
                if int(value) == option[1]:
                    option[0]()

            if value:
                print("Please enter a valid option.")
            self._read_input()

        except ValueError:
            self._read_input()

    def _display_options(self):
        """ Displays menu options that the user can choose """
        for option in self._options:

            for label in self._label:
                if label[0] == option[1]:
                    print("\n==== " + label[1] + " ====")

            print(f"[{option[1]}] {option[2]}")

    @staticmethod
    def _clear():
        """ Clears the console """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _request_input(input_prompt):
        while True:
            user_input = input(input_prompt)

            if user_input != "":
                return user_input

    @staticmethod
    def _multiple_fields_input(fields):
        print(f"You may search by the following fields: {', '.join(fields)}")
        print("First, enter each field you want to search by separated by a comma and a space ', '.")

        while True:
            fields_input = safe_input()
            search_fields = set(fields_input.split(', '))

            # Checks whether the user entered any fields that do not exist
            if not search_fields.issubset(fields):
                incorrect_fields = search_fields.difference(fields)
                print(f"The following field(s) are not valid: '{', '.join(incorrect_fields)}'. Please try again.")
                continue
            else:
                break

        parameters = []
        for parameter in search_fields:
            parameter = safe_input(f"Enter search parameter for '{parameter}': ")
            parameters.append(parameter)

        return dict(zip(search_fields, parameters))
