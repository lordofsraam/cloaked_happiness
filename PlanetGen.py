import random

class WordGen:
	#alphabet = "abcdefghijklmnopqrstuvwxyz"
	alphabet = "bcdfghjklmnpqrstvwxyz"
	common = "bcdfgh"
	rare = "qvwxyzkj"
	vowls = "aeiou"
	pairs = ["th", "he", "an", "re", "er", "in", "on", "at", "nd", "st", "es", "en", "of", "te", "ed", "or", "ti", "hi", "as", "to"]
	doubles = ["ll", "ee", "ss", "oo", "tt", "ff", "rr", "nn", "pp", "cc"]
	endings = ["cy", "ion", "en", "es", "se", "ty"]

	def __init__(self, length):
		self.length = length
		pass

	def GenWord(self):
		i = 0
		ending = None
		word = ""

		try:
			num_of_vowls = (self.length % 7) + 2
		except ZeroDivisionError:
			num_of_vowls = 1

		if num_of_vowls > 1:
			num_of_vowls = 1

		if random.randint(0, 1):
			ending = random.choice(self.endings)
			leng = self.length - len(ending)
		else:
			leng = self.length

		print "Length: ", self.length
		print "Ending: ", ending if ending != None else "(None)"
		print "Vowls: ", num_of_vowls

		while i < leng:
			i += 1
			if i != num_of_vowls:
				if i % num_of_vowls:
					word += random.choice(self.vowls)
					continue

			if random.randrange(1, 100, 2) == 50:
				word += random.choice(self.doubles)
				i += 1
				continue

			if random.randrange(1, 10, 2) == 5:
				word += random.choice(self.pairs)
				i += 1
				continue

			if random.randrange(1, 5, 2) == 3:
				word += random.choice(self.common)
			elif random.randrange(1, 50, 2) == 23:
				word += random.choice(self.rare)
			else:
				word += random.choice(self.alphabet)

		if ending:
			word += ending

		return word




class Planet:
	def __init__(self):
		self.distance = 0


class PlanetEarth(Planet):
	def __init__(self):
		pass
