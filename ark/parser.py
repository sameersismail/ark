"""
Parse an Emacs Org Mode file, and extract the embedded Anki sections.

See `test/test_parsing.py` for an example of the syntax.
"""

import re
from enum import Enum, auto
from typing import List, Tuple


class Token(Enum):
    """Token classes."""
    CARD = auto()
    HEADER_1 = auto()
    HEADER_2 = auto()
    HEADER_3 = auto()


class CardGrammar:
    """Grammar for the primary constructs."""
    heading = re.compile(
        r'^'                            # Beginning of line
            r'(?P<leading>\*{1,3})'     # 1-3 stars
            r'\ '                       # Separating space
            r' *'                       # Any number of leading spaces
            r'(?P<header>[^\n]+)'       # Header text, anything but a newline
            r' *'                       # Any number of trailing spaces
        r'$'                            # End of line
    )
    
    block_start = re.compile(
        r'^'                        # Beginning of line
            r' *'                   # Any number of leading spaces
            r'#\+begin_src anki'    # Block start
            r' *'                   # Any number of trailing spaces
        r'$'                        # End of line
    )

    block_end = re.compile(
        r'^'                        # Beginning of line
            r' *'                   # Any number of leading spaces
            r'#\+end_src'           # Block end
            r' *'                   # Any number of trailing spaces
        r'$'                        # End of line
    )


class CardLexer:
    """Tokenise the input into the appropriate classes."""
    def __init__(self, org_input: str):
        self.grammar = CardGrammar()
        self.rules = ['heading', 'block_start', 'block_end']
        self.CARD_SEPARATOR = (r' *' r'---')

        self.org_input = org_input
        self.tokens: List[Tuple[Token, str]] = []

        self.lines = self.org_input.splitlines(keepends=True)
        self.lines.reverse()

    def lex(self) -> List[Tuple[Token, str]]:
        """Iterate over each line of input, and parse the section."""
        while len(self.lines) > 0:
            line = self.lines.pop()

            for key in self.rules:
                rule = getattr(self.grammar, key, None)
                if rule is None:
                    continue

                pattern = rule.match(line)
                if not pattern:
                    continue

                parse_method = getattr(self, 'parse_{}'.format(key), None)
                if parse_method is None:
                    continue
                parse_method(pattern)

        return self.tokens

    def parse_heading(self, pattern):
        """Append the appropriate header to the token stream."""
        header_prefix = pattern.groupdict()['leading']
        header = pattern.groupdict()['header']

        if len(header_prefix) == 1:
            self.tokens.append((Token.HEADER_1, header))
        elif len(header_prefix) == 2:
            self.tokens.append((Token.HEADER_2, header))
        elif len(header_prefix) == 3:
            self.tokens.append((Token.HEADER_3, header))

    def parse_block_start(self, pattern):
        """Extract the Anki block.""" 
        card_buffer: List[str] = []
        block_end_pattern = self.grammar.block_end

        while len(self.lines) > 0:
            line = self.lines.pop()
            block_end = block_end_pattern.match(line)
            if not block_end:
                card_buffer.append(line)
            else:
                break

        self.parse_block(card_buffer)
        
    def parse_block(self, card_buffer: List[str]):
        """Parse the individual card."""
        cards: List[str] = []
        interim_card: List[str] = []
        
        for line in card_buffer:
            if re.match(self.CARD_SEPARATOR, line) is not None:
                cards.append("".join(interim_card))
                interim_card.clear()
            else:
                interim_card.append(line)
        
        if len(interim_card) > 0:
            cards.append("".join(interim_card))
        
        # TODO: Add more preprocessing: spellcheck, valid parentheses, etc.
        for card in cards:
            if (len(card) == 0) or (card.isspace()):
                # TODO: Add warning message
                continue
            elif card.count('~~') == 0:
                # TODO: Add warning message
                continue
            elif card.count('~~') % 2 != 0:
                # TODO: Add warning message
                continue
            else:
                self.tokens.append((Token.CARD, card))
