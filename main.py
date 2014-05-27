import argparse

from metareg.metareg import find_regex, verify


def lines_from_file(filename):
    with open(filename, "r") as f:
        return {l.strip() for l in f}


def get_strings(match_these_filename, dont_match_these_filename):
    match_these = lines_from_file(match_these_filename)
    dont_match_these = lines_from_file(dont_match_these_filename) - match_these
    return match_these, dont_match_these


def main():
    parser = argparse.ArgumentParser(description="Find shortest regex matching all strings from one list and none from another")
    parser.add_argument("match_these_filename", metavar="MATCH_THESE", type=str, help="Match strings in this file")
    parser.add_argument("dont_match_these_filename", metavar="DONT_MATCH_THESE", type=str, help="Don't match strings in this file")
    args = parser.parse_args()
    match_these, dont_match_these = get_strings(args.match_these_filename, args.dont_match_these_filename)
    regex = find_regex(match_these, dont_match_these)
    if verify(regex, match_these, dont_match_these):
        print("Solution found ({0} chars): {1}".format(len(regex), regex))
    else:
        print("Solution could not be found. Closest: {0}".format(regex))

if __name__ == "__main__":
    main()
