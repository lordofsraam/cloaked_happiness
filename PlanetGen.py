__author__ = 'Justin Crawford'
import random, markov, sys, time

class Planet:
	def __init__(self, galaxy, distance):
		# distance (in lightyears, based on center of galaxy)
		self._distance = distance
		self._galaxy = galaxy
		self._name = markov.genWord(random.choice("abcdefghijklmnopqrstuvwxyz"), random.randint(5, 8))
		self.supportsLife = bool(random.getrandbits(1))
		self.discoveryDate = time.time()
		self._mass = 0
		self._gravity = 0

		if self.supportsLife:
			self._population = random.randint(1, sys.maxint)
			self._populationName = markov.genWord(random.choice("abcdefghijklmnopqrstuvwxyz"), random.randint(5, 8))
			# temperature (in kelvin)
			self._temperature = random.randint(184, 330)
		else:
			self._reason = random.choice([
				'ATMOSPHERE',
				'WEATHER',
				'TERRAIN',
				'TEMPERATURE',
				'RADIOACTIVE',
			])
			# temperature (in kelvin)
			self._temperature = random.randint(1, 48000)

		#if self._temperature > 330:

	def getDistance(self):
		return self._distance

	def getName(self):
		return self._name

	def population(self):
		if self.supportsLife:
			return [self._population, self._populationName]
		else:
			return None

	def getTemperature(self, celsius=False, fahrenheit=False):
		if celsius:
			return self._temperature - 273.15
		if fahrenheit:
			return ((self._temperature - 273.15) * 1.8) + 32
		return self._temperature

	def supportsLife(self, life=None):
		if life is None:
			return self.supportsLife
		else:
			self.supportsLife = life



class Galaxy:
	def __init__(self, id, name):
		self.id = id
		self._name = markov.genWord(random.choice("abcdefghijklmnopqrstuvwxyz"), random.randint(5, 8))
		self.discoveryDate = time.time()
		self._planets = []

	def getName(self):
		return self._name

	def getPlanets(self):
		return self._planets

	def findPlanet(self, name):
		for p in self._planets:
			if name in p.name.lower():
				return p
		return None

	def addPlanet(self, planet):
		if not isinstance(planet, PlanetEarth) and not isinstance(planet PlanetEarth):
			return False
		else:
			self._planets.append(planet)


class MilkyWayGalaxy(Galaxy):
	def __init__(self):
		self.id = 0
		self._name = "MilkyWay"
		# Because timestamps cant go negative and still be valid,
		# the milkygalaxy was discovered in 1970.
		self.discoveryDate = 0
		self._planets = [PlanetEarth()]


class PlanetEarth(Planet):
	def __init__(self):
		milkyway = MilkyWayGalaxy()
		Planet.__init__(self, milkyway, 0)
		self._name = "Earth"
		self.supportsLife = True
		self._populationName = "Human"
		self._population = 7046553287