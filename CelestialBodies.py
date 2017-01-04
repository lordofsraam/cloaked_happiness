import random, re, string, math

import markov

class Planet(object):

    def __init__(self, name = markov.genWord(random.choice(string.letters), random.randint(0,9)).capitalize()):
        super(Planet, self).__init__()
        self.Name = name
        self.Radius = (((random.random() * 100.0) + 1.5 ) % 60 ) #in thousands of km
        self.Inhabited = bool(random.getrandbits(1))
        self.Atmosphere = bool(random.getrandbits(1))

    def Mass(self):
        vol = math.pow(self.Radius, 3) * math.pi * (4.0/3.0) #yeah I know its just the volume equation but what do you want from me
        return vol

class StarSystem(object):
    
    planets = []

    def __init__(self):
        super(StarSystem, self).__init__()
        
        for i in xrange(1, random.randint(1,15)):
            planets.append(Planet())
