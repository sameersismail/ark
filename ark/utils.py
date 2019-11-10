"""
Various utilities.
"""

import os
import sys
import copy


ANKI_START = '{{c1::'
ANKI_END = '}}'
CUST_DELIM = '~~'


def add_anki_searchpath() -> None:
    """Import the Anki package. Relies upon the `anki` sourcetree being present
    in the `ark` directory alongside this file.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    module_path = os.path.join(dir_path, 'anki')
    sys.path.append(module_path)


def add_cloze(text: str) -> str:
    """Replace custom enclosing characters with Anki delimiters."""
    flip = True
    chars = list(text)

    for i in range(len(chars) - 1):
        if (chars[i] == '~') and (chars[i + 1] == '~'):
            chars[i] = ANKI_START if flip else ANKI_END
            chars[i + 1] = ""
            flip ^= True

    return "".join(chars) if (flip == True) else text


def segment_section(text: str) -> str:
    """Split each cloze section on whitespace, make each individual word (and
    compound word) into its own section.""" 
    words = [CUST_DELIM + word + CUST_DELIM for word in text.split()]
    new = []

    for word in words:
        new.append(word.replace("-", f"{CUST_DELIM}-{CUST_DELIM}"))

    return " ".join(new)
