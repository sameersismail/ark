"""
Ark.
"""

import sys
import argparse
import sqlite3
from typing import List

from ..parser import CardLexer
from ..construct import construct_cards
from ..ankidb import AnkiDB
from ..utils import add_anki_searchpath
from ..config import get_config, CONFIG_FILE, CONFIG_DIR


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def run(args) -> int:
    """Run the application.
    
    :param args: { deck: str, file: List[str], dry: boolean }
    :returns: Process exit code
    """

    try:
        config = get_config()
    except FileNotFoundError as e:
        print("Error: Configuration file not found.")
        print(f"Initialise configuration file '{CONFIG_FILE}' at '{CONFIG_DIR}'.")
        print("See [documentation].")
        return EXIT_FAILURE
    except json.JSONDecodeError as e:
        print(f"Error: Configuration file not formatted correctly: {e}.")
        print("See [documentation].")
        return EXIT_FAILURE
    except KeyError as e:
        print("Error: Configuration file missing field 'anki_db'")
        print("See [documentation].")
        return EXIT_FAILURE

    try:
        for org_file in args.file:
            with open(org_file) as fd:
                contents: str = fd.read()

            tokens = CardLexer(contents).lex()
            cards = construct_cards(tokens)

            if args.dry:
                for card in cards:
                    print(card)
            else:
                add_anki_searchpath()
                import anki
                anki = AnkiDB(anki, config['anki_db'])
                anki.insert_cards(cards, args.deck)

        return EXIT_SUCCESS
    except FileNotFoundError as file_error:
        print(f"Error: File '{file_error.filename}' doesn't exist.")
        return EXIT_FAILURE
    except AssertionError:
        print("Error: Path to Anki database must end in 'anki2'.")
        return EXIT_FAILURE
    except sqlite3.OperationalError as sql_error:
        # TODO: Improve disambiguation between error conditions
        print("Error: Cannot access Anki database. ", end='')

        if sql_error.args[0] == "unable to open database file":
            print("Path to Anki database is incorrect.")
        elif sql_error.args[0] == "database is locked":
            print("Database is locked, close Anki program.")

        return EXIT_FAILURE
    except ModuleNotFoundError as module_error:
        print(f"Error: {module_error.msg}.")
        print("Ensure that 'anki' submodule has been cloned.")
        return EXIT_FAILURE
    except ValueError as val_error:
        print(f"Error: {val_error}.")
        return EXIT_FAILURE


def main() -> None:
    """Entry point for CLI."""
    parser = argparse.ArgumentParser(prog='ark')
    parser.add_argument('deck',
                        metavar='<deck>', 
                        type=str, 
                        help='Deck of choice')

    parser.add_argument('file',
                        metavar='<file>',
                        nargs='+',
                        type=str, 
                        help='Files to parse')

    parser.add_argument('-d',
                        '--dry', 
                        action='store_true',
                        help="Don't touch the database; just print parsed results")

    args = parser.parse_args()

    sys.exit(run(args))
