import re, operator, random

f = open("/usr/share/dict/american-english")

words = re.sub(r'[.!\',]', '', f.read()).lower().split()

lang_signature = {'a': {}, 'b': {}, 'c': {},
					'd': {}, 'e': {}, 'f': {}, 'g': {},
					'h': {}, 'i': {}, 'j': {}, 'k': {},
					'l': {}, 'm': {}, 'n': {}, 'o': {},
					'p': {}, 'q': {}, 'r': {}, 's': {},
					't': {}, 'u': {}, 'v': {}, 'w': {},
					'x': {}, 'y': {}, 'z': {},
					'th': {}, 'ch': {}, 'ph': {}, 'sh': {}}

for letter in lang_signature:
	for w in filter(lambda x: letter in x, words):
		for i in xrange(len(w) - 1):
			if w[i] == letter:
				if w[i + 1] in lang_signature[letter]:
					lang_signature[letter][w[i + 1]] += 1
				else:
					lang_signature[letter][w[i + 1]] = 1
			elif w[i] + w[i + 1] == letter and i < len(w) - 2:
				if w[i + 2] in lang_signature[letter]:
					lang_signature[letter][w[i + 2]] += 1
				else:
					lang_signature[letter][w[i + 2]] = 1


def genWord(c='a', l=5):
	c = c.lower()
	org = c
	ii = 0
	while ii < len(c):
		if c[ii::] in lang_signature:
			c = c[ii::]
			r_str = c
			break
		else:
			ii += 1

	for i in xrange(l - len(c)):
		sorted_signature = sorted(lang_signature[c].iteritems(), key=operator.itemgetter(1), reverse=True)
		weighted_list = []
		total = 0
		for j in xrange(len(lang_signature[c]) / 2):
			total += sorted_signature[j][1]
		for j in xrange(len(lang_signature[c]) / 2):
			weighted_list += [sorted_signature[j][0]] * int((float(sorted_signature[j][1]) / total) * 100)
		_c = random.choice(weighted_list)
		r_str += _c
		c = _c
	return org[:ii:] + r_str
