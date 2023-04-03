# <!-- Imports -->
from typing import Union
from os import getenv
from sys import exit, stdout, stderr
import colorama

# <!-- Code -->
# Enable debug function(s)
DEBUG: bool = True if getenv("UNLS_DEBUG") == "1" else False


# Support for disabling colors according to 'https://no-color.org/'
if getenv("NO_COLOR") is None:
    C: dict = {
        "black": colorama.Fore.BLACK,
        "red": colorama.Fore.RED,
        "green": colorama.Fore.GREEN,
        "yellow": colorama.Fore.YELLOW,
        "blue": colorama.Fore.BLUE,
        "magenta": colorama.Fore.MAGENTA,
        "cyan": colorama.Fore.CYAN,
        "white": colorama.Fore.WHITE,
        "reset": colorama.Fore.RESET,
    } 
else:
    C: dict = {
        "black": "",
        "red": "",
        "green": "",
        "yellow": "",
        "blue": "",
        "magenta": "",
        "cyan": "",
        "white": "",
        "reset": "",
    } 


# Generic function to print messages
def message(label: str, text: str, accent: str = "reset", use_stderr: bool = False) -> None:
    target = stderr if use_stderr else stdout
    print(f"{C[accent]}[{label}]{C['reset']} {text}", file=target)


# Send an info message
def info(text: str) -> None:
    message("INFO", text, accent="blue", use_stderr=False)


# Send a debug message visible only with environment variable
def debug(text: str) -> None:
    if DEBUG:
        message("DEBUG", text, accent="cyan", use_stderr=False)


# Send a warning message
def warn(text: str) -> None:
    message("WARNING", text, accent="yellow", use_stderr=True)


# End the program execution with a success message or an error.
def error(text: str, code: Union[int, None] = None) -> None:
    message("ERROR", text, accent="red", use_stderr=True)
    if code is not None:
        exit(code)

