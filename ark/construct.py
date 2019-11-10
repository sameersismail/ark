"""
Construct the HTML-formatted cards.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional

from .parser import Token
from .renderer import Render
from .utils import add_cloze


@dataclass
class Template:
    """DOM elements which relate to Anki card's CSS."""
    H1_HTML = '<h1 class="subject">{}</h1>'
    H2_HTML = '<h1 class="subject">{}: {}</h1>'
    H3_HTML = '<h1 class="subject">{}, {}: {}</h1>'
    OPEN_CARD = '<div class="container">'
    CLOSE_CARD = '</div>'

    @staticmethod
    def assemble_headers(headers: Tuple[str, str, str]) -> Optional[str]:
        if not (headers[0] == "" or headers[1] == "" or headers[2] == ""):
            return Template.H3_HTML.format(headers[0], headers[1], headers[2])
        elif not (headers[0] == "" or headers[1] == ""):
            return Template.H2_HTML.format(headers[0], headers[1])
        elif not headers[0] == "":
            return Template.H1_HTML.format(headers[0])
        else:
            return None


def construct_cards(tokens: List[Tuple[Token, str]]) -> List[str]:
    """Construct list of HTML-formatted cards.
    
    :param tokens: List containing a token class and lexeme pair.
    :returns: List of HTML-formatted cards.
    """
    md = Render()
    headers: Tuple[str, str, str] = ("", "", "")
    cards: List[str] = []

    for token in tokens:
        if token[0] == Token.HEADER_1:
            headers = (token[1], "", "")
        elif token[0] == Token.HEADER_2:
            headers = (headers[0], token[1], "")
        elif token[0] == Token.HEADER_3:
            headers = (headers[0], headers[1], token[1])
        elif token[0] == Token.CARD:
            constructed_headers = Template.assemble_headers(headers)
            body = add_cloze(md.render(token[1]))

            if constructed_headers is None:
                cards.append(
                    f'{Template.OPEN_CARD}' 
                        f'{body}'
                    f'{Template.CLOSE_CARD}'
                )
            else:
                cards.append(
                    f'{Template.OPEN_CARD}' 
                        f'{constructed_headers}'
                        f'<hr>'
                        f'{body}'
                    f'{Template.CLOSE_CARD}'
                )

    return cards
