"""
Insert an image into the Anki media database.

Grabs an image from the system clipboard, and saves it to the Anki media
database, returning the path of the file in the Anki database, and copying it
to the clipboard.

NOTE: Currently only works on macOS, with `pngpaste` installed and on PATH.
"""

import sys
import argparse
import sqlite3
import subprocess
from typing import List

from ..ankidb import AnkiDB
from ..utils import add_anki_searchpath
from ..config import get_config


EXIT_SUCCESS = 0
EXIT_FAILURE = 1
HTML_IMG = '<img src="{image}" />'


def run_pic(args) -> int:
    """Run the application.
    
    :param args: { filename: str }
    :returns: Process exit code
    """
    
    config = get_config()
    if config is None:
        return EXIT_FAILURE

    try:
        completed = subprocess.run(['pngpaste', args.filename], stdout=subprocess.PIPE)

        if (completed.returncode != 0) or (completed.stdout != b''):
            print("Error: 'pngpaste' command failed.")
            return EXIT_FAILURE
        
        add_anki_searchpath()
        import anki
        ankidb = AnkiDB(anki, config['anki_db'])

        image_name = ankidb.insert_image(args.filename)
        process = subprocess.Popen('pbcopy',
                                   env={'LANG': 'en_US.UTF-8'},
                                   stdin=subprocess.PIPE)
        process.communicate(HTML_IMG.format(image=image_name).encode('utf-8'))
        # TODO: Remove temporary image

        return EXIT_SUCCESS
    except FileNotFoundError as file_error:
        print(f"Error: File '{file_error.filename}' doesn't exist.")
        return EXIT_FAILURE
    except AssertionError:
        print("Error: Path to Anki database must end in 'anki2'.")
        return EXIT_FAILURE
    except sqlite3.OperationalError as sql_error:
        print("Error: Cannot access Anki database. ", end='')

        if sql_error.args[0] == "unable to open database file":
            print("Path to Anki database is incorrect.")
        elif sql_error.args[0] == "database is locked":
            print("Database is locked, close Anki program.")

        return EXIT_FAILURE
    except ModuleNotFoundError as module_error:
        print(f"Error: {module_error.msg}")
        print("Ensure that 'anki' submodule has been cloned.")
        return EXIT_FAILURE
    except ValueError as val_error:
        print("Error: {}.".format(val_error))
        return EXIT_FAILURE


def main() -> None:
    """Entry point for CLI."""
    parser = argparse.ArgumentParser(prog='arkp')
    parser.add_argument('filename',
                        metavar='<filename>', 
                        type=str, 
                        help='Location to store temporary image')

    args = parser.parse_args()
    sys.exit(run_pic(args))
