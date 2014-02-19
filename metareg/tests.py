''' Project test fixtures to be run with nosetests '''
import itertools
import re

from . import metareg


# Constants used by tests
GOOD_STRINGS = {"bread", "regale", "fence"}
BAD_STRINGS = {"hamburger", "tense", "murphy"}


def test_does_match():
    good_matches = ["^br", "e.ce", "le$"]
    bad_matches = ["^en", "b.y", "rt$"]
    assert all(metareg.does_match(r, GOOD_STRINGS) for r in good_matches)
    assert not any(metareg.does_match(r, GOOD_STRINGS) for r in bad_matches)


def test_matched_strings():
    matches = {
        "re": {"bread", "regale"},
        "e$": {"regale", "fence"},
        "e.c": {"fence"},
        "^en": set(),
        "b.y": set()
    }
    assert all(metareg.matched_strings(k, GOOD_STRINGS) == v for k, v in matches.items())


def test_escape():
    string = "abcdef.+*(ghi)?"
    expected = r"abcdef\.\+\*\(ghi\)\?"
    assert "".join(metareg.escape(c) for c in string) == expected


def test_random_substring():
    string = "sixteen sandwiches"
    assert all(re.search(metareg.random_substring(string), string) for _ in range(200))


def test_random_regex_component_generator():
    components = itertools.islice(metareg.random_regex_component_generator(GOOD_STRINGS), 200)
    assert all(metareg.does_match(c, GOOD_STRINGS) for c in components)


def test_verify():
    assert metareg.verify("^br|e.ce|le$", GOOD_STRINGS, BAD_STRINGS)
    assert not metareg.verify("^br|en.e|le$", GOOD_STRINGS, BAD_STRINGS)
