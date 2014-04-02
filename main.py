import argparse

from metareg.metareg import find_regex, verify


def lines_from_file(filename):
    with open(filename, "r") as f:
        return {l.strip() for l in f}


def get_strings(good_strings_filename, bad_strings_filename):
    good_strings = lines_from_file(good_strings_filename)
    bad_strings = lines_from_file(bad_strings_filename) - good_strings
    return good_strings, bad_strings


def main():
    parser = argparse.ArgumentParser(description="Find shortest regex matching all strings from one list and none from another")
    parser.add_argument("good_strings_filename", metavar="GOOD_STRINGS", type=str, help="File with strings to match")
    parser.add_argument("bad_strings_filename", metavar="BAD_STRINGS", type=str, help="File with strings to not match")
    args = parser.parse_args()
    good_strings, bad_strings = get_strings(args.good_strings_filename, args.bad_strings_filename)
    regex = find_regex(good_strings, bad_strings)
    if verify(regex, good_strings, bad_strings):
        print("Solution found ({0} chars): {1}".format(len(regex), regex))
    else:
        print("Solution could not be found. Closest: {0}".format(regex))

if __name__ == "__main__":
    main()
