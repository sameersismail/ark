"""
Renderers to translate from custom Markdown format into HTML, with Anki syntax
interspersed.
"""

import re
from .mistune import Markdown, Renderer, escape
from .utils import add_cloze


CODE_BLOCK = (
    r'(`{3})'   # Start of Markdown code block ('```')
    r' *'       # Any number of spaces
    r'(\S+)'    # One or more characters, except a newline
    r' *'       # Any number of spaces
    r'\n'       # End of line
)


class HighLightRenderer(Renderer):
    """Override the code block parsing to add syntax highlighting."""
    def __init__(self, highlight, get_lexer_by_name, html):
        super().__init__()
        self.highlight = highlight
        self.get_lexer_by_name = get_lexer_by_name
        self.html = html

    def block_code(self, code, lang):
        """Add syntax highlighting to code block using Pygments."""
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(escape(code))
        else:
            lexer = self.get_lexer_by_name(lang, stripall=True)
            formatter = self.html.HtmlFormatter()
            return self.highlight(code, lexer, formatter)


class Render:
    def __init__(self):
        self.renderer = None
        self.md = Markdown()
        self.code_block = re.compile(CODE_BLOCK)

    def render(self, card: str) -> str:
        # Dynamically load pygments lexing; only if needed
        if self.code_block.search(card) is not None:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import html

            self.renderer = HighLightRenderer(highlight, get_lexer_by_name, html)
            self.md = Markdown(renderer=self.renderer)

        return self.md.render(card)
