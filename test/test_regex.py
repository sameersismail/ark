import re
from ark import renderer
from ark.parser import CardGrammar


def test_code_block_regex():
    cb = re.compile(renderer.CODE_BLOCK)
    
    # Failed
    assert cb.search("qwerty") is None
    assert cb.search("```\n") is None
    
    # Successful
    assert cb.search("```a\n") is not None
    assert cb.search("```a \n") is not None
    assert cb.search("\n\n```a \n") is not None
    assert cb.search("Header:\n"
        "Some text, and some ~~code~~:\n"
        "\n"
        "```python\n"
        "def main(argv: List[str]):\n"
        "    pass\n"
    ) is not None


def test_parser_regex():
    # CardGrammar.{heading, block_start, block_end}
    assert 1 == 1
