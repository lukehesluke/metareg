import re

ESCAPE_CHARACTERS = {
	'.', '*', '+', '?',
	'^', '$',
	'{', '}',
	'(', ')',
	'|', '[', ']',
	'\\'
}

DOTIFY_CHANCE = 0.05

REPEAT_CHARACTERS = ['', '*', '+', '?']
REPEAT_CHANCES = [94, 2, 2, 2]


def does_match(regex, strings):
	''' Does regex match any from a collection of strings? '''
	compiled = re.compile(regex)
	return any(re.search(compiled, s) for s in strings)


def matched_strings(regex, strings):
	''' Set of strings matched by regex '''
	compiled = re.compile(regex)
	return {s for s in strings if re.search(compiled, s)}


def escape(char):
	'''
	Escape special regex character
	re.escape escapes all characters that are neither ASCII letters,
	numbers or '_'. This results in too many backslashes, unnecessarily
	increasing the size of the resulting regex
	'''
	return "\\{0}".format(char) if char in ESCAPE_CHARACTERS else char


def dotify(glyph):
    ''' Randomly return character or a dot '''
    return "." if random.random() < DOTIFY_CHANCE else glyph


def repeat(glyph):
    '''
    Possibly repeat a regex character
    Appends a +, * or a ? to the character with a low probability
    '''
    index = util.one_of(REPEAT_CHANCES)
    return glyph + REPEAT_CHARACTERS


def create_pattern(string):
	''' Create random pattern matching string '''
	glyphs = '^' + [repeat(dotify(escape(c))) for c in string] + '$'
	start_index = random.randrange(len(glyphs) - 1)
	# TODO
	#length = max(start_index - 1, 1
