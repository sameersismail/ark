from ark.construct import Template, construct_cards
from ark.parser import Token


def test_header_basics():
    assert Template.assemble_headers(("", "", "")) is None
    assert Template.assemble_headers(("", "", "A")) is None
    assert Template.assemble_headers(("", "A", "")) is None
    assert Template.assemble_headers(("", "B", "A")) is None


def test_header_construct():
    assert Template.assemble_headers(("A", "", "")) == Template.H1_HTML.format("A")
    assert Template.assemble_headers(("A", "B", "")) == Template.H2_HTML.format("A", "B")
    assert Template.assemble_headers(("A", "B", "C")) == Template.H3_HTML.format("A", "B", "C")


def test_construct_simple():
    token_input = [
        (Token.HEADER_1, 'Foo'),
        (Token.CARD, 'A is ~~A~~\n'),
        (Token.HEADER_2, 'Bar'),
        (Token.CARD, 'A is ~~A~~\n'),
        (Token.HEADER_3, 'Baz'),
        (Token.CARD, 'A is ~~A~~\n'),
    ]

    text_output = [
        '''<div class="container"><h1 class="subject">Foo</h1><hr><p>A is {{c1::A}}</p>
</div>''',
    '''<div class="container"><h1 class="subject">Foo: Bar</h1><hr><p>A is {{c1::A}}</p>
</div>''',
    '''<div class="container"><h1 class="subject">Foo, Bar: Baz</h1><hr><p>A is {{c1::A}}</p>
</div>''',
    ]

    assert construct_cards(token_input) == text_output


def test_multiple_words():
    token_input = [
        (Token.HEADER_1, 'Foo'),
        (Token.CARD, 'A is ~~A B~~\n'),
        (Token.CARD, 'A is ~~A B C~~ as well as ~~D E F~~\n'),
    ]

    text_output = [
    '''<div class="container"><h1 class="subject">Foo</h1><hr><p>A is {{c1::A}} {{c1::B}}</p>
</div>''',
        '''<div class="container"><h1 class="subject">Foo</h1><hr><p>A is {{c1::A}} {{c1::B}} {{c1::C}} as well as {{c1::D}} {{c1::E}} {{c1::F}}</p>
</div>''',
    ]

    assert construct_cards(token_input) == text_output


class TestMarkdown:
    def test_unordered_list(self):
        token_input = [
            (Token.CARD, 'An unordered list:\n\n- X\n- Y\n- ~~Z~~\n'),
        ]

        text_output = [
'''<div class="container"><p>An unordered list:</p>
<ul>
<li>X</li>
<li>Y</li>
<li>{{c1::Z}}</li>
</ul>
</div>''',
        ]

        assert construct_cards(token_input) == text_output

    def test_ordered_list(self):
        token_input = [
            (Token.CARD, 'An ordered list:\n\n1. X\n2. Y\n3. ~~Z~~\n'),
        ]

        text_output = [
'''<div class="container"><p>An ordered list:</p>
<ol>
<li>X</li>
<li>Y</li>
<li>{{c1::Z}}</li>
</ol>
</div>''',
        ]

        assert construct_cards(token_input) == text_output

    def test_inline_code(self):
        token_input = [
            (Token.CARD, 'A command: ~~`rustc`~~\n'),
        ]

        text_output = [
'''<div class="container"><p>A command: {{c1::<code>rustc</code>}}</p>
</div>''',
        ]

        assert construct_cards(token_input) == text_output

    def test_code_block(self):
        token_input = [
            (Token.CARD, 'A program:\n\n```\nfn main() -> Result<T, E> {\n    ~~Ok(())~~\n}\n```\n'),
        ]

        text_output = [
'''<div class="container"><p>A program:</p>
<pre><code>fn main() -&gt; Result&lt;T, E&gt; {
    {{c1::Ok(())}}
}
</code></pre>
</div>''',
        ]

        assert construct_cards(token_input) == text_output

    def test_high_code(self):
        token_input = [
            (Token.CARD, 'A highlighted program:\n\n```python\ndef main(argv: List[str]):\n    print("Hello, ~~world.~~")\n```\n'),
        ]

        text_output = [
'''<div class="container"><p>A highlighted program:</p>
<div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">main</span><span class="p">(</span><span class="n">argv</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="nb">str</span><span class="p">]):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Hello, {{c1::world.}}&quot;</span><span class="p">)</span>
</pre></div>
</div>''',
        ]

        assert construct_cards(token_input) == text_output

    def test_inline_tex(self):
        token_input = [
            (Token.CARD, 'Inline TeX: $f(x) = $ ~~$y$~~\n'),
        ]

        text_output = [
r'''<div class="container"><p>Inline TeX: [latex]\scriptsize$f(x) = $[/latex] {{c1::[latex]\scriptsize$y$[/latex]}}</p>
</div>''',
        ]

        assert construct_cards(token_input) == text_output

    def test_table(self):
        token_input = [
            (Token.CARD, 'A table:\n\n|A|B|C|\n|---|---|---|\n|X|Y|~~Z~~|\n'),
        ]

        text_output = [
'''<div class="container"><p>A table:</p>
<table>
<thead><tr>
<th>A</th>
<th>B</th>
<th>C</th>
</tr>
</thead>
<tbody>
<tr>
<td>X</td>
<td>Y</td>
<td>{{c1::Z}}</td>
</tr>
</tbody>
</table>
</div>''',
        ]

        assert construct_cards(token_input) == text_output

    def test_escaped(self):
        token_input = [
            (Token.CARD, 'Escaped:\n\n- \\_\n- \\*\n- ~~\\$~~\n'),
        ]

        text_output = [
'''<div class="container"><p>Escaped:</p>
<ul>
<li>_</li>
<li>*</li>
<li>{{c1::$}}</li>
</ul>
</div>''',
        ]

        assert construct_cards(token_input) == text_output

    def test_block_tex(self):
        token_input = [
            (Token.CARD, 'Block TeX:\n\n$$f(x) = {{c1::y}}$$\n'),
        ]

        text_output = [
'''<div class="container"><p>Block TeX:</p>
[latex]$f(x) = {{c1::y}}$[/latex]</div>''',
        ]

        assert construct_cards(token_input) == text_output
