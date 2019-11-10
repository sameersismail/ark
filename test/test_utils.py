from ark import utils


def test_add_cloze():
    assert utils.add_cloze("") == ""
    assert utils.add_cloze("A") == "A"

    assert utils.add_cloze("~~A~~") == "{{c1::A}}"
    assert utils.add_cloze("~~A~~BA") == "{{c1::A}}BA"
    assert utils.add_cloze("A~~B~~A") == "A{{c1::B}}A"
    assert utils.add_cloze("AB~~A~~") == "AB{{c1::A}}"

    assert utils.add_cloze("AB~~A") == "AB~~A"
    assert utils.add_cloze("AB~~A") == "AB~~A"
    assert utils.add_cloze("A~~B~~A~~") == "A~~B~~A~~"


def test_segment_section():
    assert utils.segment_section("") == ""

    assert utils.segment_section("a b") == "~~a~~ ~~b~~"
    assert utils.segment_section("a b c d") == "~~a~~ ~~b~~ ~~c~~ ~~d~~"

    assert utils.segment_section("a, b-d") == "~~a,~~ ~~b~~-~~d~~"
    assert utils.segment_section("b-d-e") == "~~b~~-~~d~~-~~e~~"


def test_add_anki():
    utils.add_anki_searchpath()
    import anki
