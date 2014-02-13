from metareg.metareg import find_regex, verify


def lines_from_file(filename):
    with open(filename, "r") as f:
        return {l.strip() for l in f}


def main():
    good_strings = lines_from_file("good_strings.txt")
    bad_strings = lines_from_file("bad_strings.txt") - good_strings
    regex = find_regex(good_strings, bad_strings)
    if verify(regex, good_strings, bad_strings):
        print("Solution found (%s chars): %s" % (len(regex), regex))
    else:
        print("Solution could not be found. Closest: %s" % (regex,))

if __name__ == "__main__":
    main()
