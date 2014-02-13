''' Project test fixtures to be run with nosetests '''
from . import metareg


def test_does_match():
    strings = {"bread", "regale", "fence"}
    good_matches = ["^re", "e.ce", "le$"]
    bad_matches = ["^en", "b.y", "rt$"]
    assert all(metareg.does_match(r, strings) for r in good_matches)
    assert not any(metareg.does_match(r, strings) for r in bad_matches)


def test_matched_strings():
    strings = {"bread", "regale", "fence"}
    matches = {
        "re": {"bread", "regale"},
        "e$": {"regale", "fence"},
        "e.c": {"fence"},
        "^en": set(),
        "b.y": set()
    }
    assert all(metareg.matched_strings(k, strings) == v for k, v in matches.items())


def test_random_substring():
    string = "sixteen sandwiches"
    assert all(metareg.random_substring(string) in string for _ in range(100))
