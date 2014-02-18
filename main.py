from metareg.metareg import find_regex, verify


def lines_from_file(filename):
    with open(filename, "r") as f:
        return {l.strip() for l in f}


def get_strings():
    good_strings = lines_from_file("good_strings.txt")
    bad_strings = lines_from_file("bad_strings.txt") - good_strings
    return good_strings, bad_strings


def main():
    good_strings, bad_strings = get_strings()
    regex = find_regex(good_strings, bad_strings)
    if verify(regex, good_strings, bad_strings):
        print("Solution found ({0} chars): {1}".format(len(regex), regex))
    else:
        print("Solution could not be found. Closest: {0}".format(regex))

if __name__ == "__main__":
    main()
