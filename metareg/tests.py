''' Project test fixtures to be run with nosetests '''
import itertools
import re

from . import metareg


# Constants used by tests
MATCH_THESE = {"bread", "regale", "fence"}
DONT_MATCH_THESE = {"hamburger", "tense", "murphy"}


def test_does_match():
    match_these = ["^br", "e.ce", "le$"]
    dont_match_these = ["^en", "b.y", "rt$"]
    assert all(metareg.does_match(r, MATCH_THESE) for r in match_these)
    assert not any(metareg.does_match(r, MATCH_THESE) for r in dont_match_these)


def test_matched_strings():
    matches = {
        "re": {"bread", "regale"},
        "e$": {"regale", "fence"},
        "e.c": {"fence"},
        "^en": set(),
        "b.y": set()
    }
    assert all(metareg.matched_strings(k, MATCH_THESE) == v for k, v in matches.items())


def test_escape():
    string = "abcdef.+*(ghi)?"
    expected = r"abcdef\.\+\*\(ghi\)\?"
    assert "".join(metareg.escape(c) for c in string) == expected


def test_random_substring():
    string = "sixteen sandwiches"
    assert all(re.search(metareg.random_substring(string), string) for _ in range(200))


def test_random_regex_component_generator():
    components = itertools.islice(metareg.random_regex_component_generator(MATCH_THESE), 200)
    assert all(metareg.does_match(c, MATCH_THESE) for c in components)


def test_verify():
    assert metareg.verify("^br|e.ce|le$", MATCH_THESE, DONT_MATCH_THESE)
    assert not metareg.verify("^br|en.e|le$", MATCH_THESE, DONT_MATCH_THESE)
