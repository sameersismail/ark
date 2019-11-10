from ark import parser


class TestBasic:
    def test_header_parsing(self) -> None:
        org_input = (
            "* Topic\n"
            "** Sub-topic\n"
            "*** Sub-sub-topic\n"
            "**** Sub-sub-sub-topic; not parsed\n"
        )

        lexer = parser.CardLexer(org_input)
        tokens = lexer.lex()

        token_output = [
            (parser.Token.HEADER_1, 'Topic'),
            (parser.Token.HEADER_2, 'Sub-topic'),
            (parser.Token.HEADER_3, 'Sub-sub-topic'),
        ]

        assert tokens == token_output

    def test_basic_parsing(self) -> None:
        org_input = (
            "* Mathematics\n"
            "\n"
            "- Lorem ipsum\n"
            "- Aenean ac leo maximus\n"
            "\n"
            "Etc.\n"
            "\n"
            "#+begin_src anki\n"
            "f(x) = ~~y~~\n"
            "---\n"
            "Nunc ~~risus~~ metus, consequat ~~vel~~ enim et, viverra faucibus\n"
            "#+end_src\n"
        )

        lexer = parser.CardLexer(org_input)
        tokens = lexer.lex()
        
        token_output = [
            (parser.Token.HEADER_1, 'Mathematics'),
            (parser.Token.CARD, 'f(x) = ~~y~~\n'),
            (parser.Token.CARD, 'Nunc ~~risus~~ metus, consequat ~~vel~~ enim et, viverra faucibus\n'),
        ]

        assert tokens == token_output

    def test_parsing_starting(self) -> None:
        org_input = (
            "* Topic\n"
            "- Discussion on topic\n"
            "    #+begin_src anki\n"
            "    f(x) = ~~y~~\n"
            "    ---\n"
            "    Nunc ~~risus~~ metus, consequat ~~vel~~ enim et, viverra faucibus\n"
            "    #+end_src\n"
        )

        lexer = parser.CardLexer(org_input)
        tokens = lexer.lex()
        
        token_output = [
            (parser.Token.HEADER_1, 'Topic'),
            (parser.Token.CARD, '    f(x) = ~~y~~\n'),
            (parser.Token.CARD, '    Nunc ~~risus~~ metus, consequat ~~vel~~ enim et, viverra faucibus\n'),
        ]

        assert tokens == token_output


class TestMarkdown:
    def test_unordered_list(self) -> None:
        org_input = (
            "#+begin_src anki\n"
            "An unordered list:\n"
            "\n"
            "- X\n"
            "- Y\n"
            "- ~~Z~~\n"
        )

        lexer = parser.CardLexer(org_input)
        tokens = lexer.lex()
        token_output = [(parser.Token.CARD, 'An unordered list:\n\n- X\n- Y\n- ~~Z~~\n')]

        assert tokens == token_output
    
    # TODO: Add further?


def test_multiple_lines() -> None:
    org_input = """
#+begin_src anki
To multiply a **thing** by a **thing**:
~~Multiply thing~~ value by the ~~value~~
#+end_src
    """

    lexer = parser.CardLexer(org_input)
    tokens = lexer.lex()

    token_output = [
        (parser.Token.CARD, 'To multiply a **thing** by a **thing**:\n~~Multiply thing~~ value by the ~~value~~\n'),
    ]

    assert tokens == token_output


def test_empty() -> None:
    org_input = """
**** Sub-sub-sub-topic

#+begin_src anki

#+end_src
    """

    lexer = parser.CardLexer(org_input)
    tokens = lexer.lex()

    token_output = []
    
    assert tokens == token_output


def test_empty_multiple() -> None:
    org_input = """
#+begin_src anki
---
#+end_src

#+begin_src anki

---

#+end_src
    """

    lexer = parser.CardLexer(org_input)
    tokens = lexer.lex()

    assert tokens == []


def test_faulty_cards() -> None:
    org_input = """
#+begin_src anki
Mauris auctor enim vel feugiat dictum.
---
Mauris ~~auctor enim vel feugiat dictum.
---
Mauris ~~auctor~~ ~~enim vel feugiat dictum.
---
---
#+end_src
    """

    lexer = parser.CardLexer(org_input)
    tokens = lexer.lex()

    assert tokens == []


def test_separator_list() -> None:
    org_input = """\
#+begin_src anki
A foo is composed of three things:
- A
- ~~B~~
- C
---
You can do operation ~~bar~~ on foo
#+end_src
    """

    lexer = parser.CardLexer(org_input)
    tokens = lexer.lex()

    token_output = [
        (parser.Token.CARD, 'A foo is composed of three things:\n- A\n- ~~B~~\n- C\n'),
        (parser.Token.CARD, 'You can do operation ~~bar~~ on foo\n'),
    ]

    assert tokens == token_output


def test_invalid_routine() -> None:
    org_input = (
        "* Foo Bar\n"
    )

    lexer = parser.CardLexer(org_input)
    lexer.rules += 'parse_fake'
    tokens = lexer.lex()

    token_output = [
        (parser.Token.HEADER_1, 'Foo Bar'),
    ]

    assert tokens == token_output
