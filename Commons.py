import colorama
import os
import sys


REPOSITORY_DIRECTORY: str = os.path.join(os.path.dirname(__file__), 'gRPC_Repository')
"""The location of the repository got using git."""
OUTPUT_DIRECTORY: str = os.path.join(os.path.dirname(__file__), 'gRPC_Library')
"""The location of the output with all includes and libraries."""


def get_file_name(path: str) -> str:
    """
    Gets the file name without any extension from a path.
    """
    file_name: str = os.path.basename(path.strip())
    if '.' in file_name:
        index: int = file_name.index('.')
        file_name = file_name[0 : index]
    return file_name


def print_message(file_name: str, message: str) -> None:
    """
    Prints a normal message with the associated file name.
    """
    print(f'[{ get_file_name(file_name) }] { message }')


def print_success(file_name: str, message: str) -> None:
    """
    Prints a success message in green, with the associated file name
    """
    print(f'[{ get_file_name(file_name) }]{ colorama.Fore.GREEN } { message }')


def print_failure(file_name: str, message: str) -> None:
    """
    Prints a failure message in red, with the associated file name
    """
    print(f'[{ get_file_name(file_name) }]{ colorama.Fore.RED } { message }', file = sys.stderr)

