import tkinter as tk
from colorama import Fore, Back, Style


def show_error(title: str, message: str):
    print(Style.RESET_ALL, Fore.RED, title, ":", sep="")
    print(Fore.RED, message, sep="")
    print(Style.RESET_ALL)
