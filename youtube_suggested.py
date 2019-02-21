import urllib2
from bs4 import BeautifulSoup
import operator
import matplotlib.pyplot as plt
import numpy as np


RECUR_DEPTH = 6
TREE_WIDTH = 2


class Link(object):
    def __init__(self, title, href):
        self.title = title.strip()
        self.url = 'https://www.youtube.com' + href

    def __str__(self):
        return self.title


class Page(object):
    def __init__(self, link):
        if type(link) == Link:
            vid_page_src = urllib2.urlopen(link.url)
            self.url = link.url
        else:
            vid_page_src = urllib2.urlopen(link)
            self.url = link

        if vid_page_src is None:
            raise ValueError('Failed to load ' + self.url)

        self.page = BeautifulSoup(vid_page_src, 'html.parser')

        res = self.page.find_all('a',
                                 attrs={'class': ' content-link spf-link yt-uix-sessionlink spf-link '})
        if len(res) == 0:
            # Sometimes the html class doesnt have spaces and bs4 doesn't strip
            #    so we gotta look again
            res = self.page.find_all('a',
                                     attrs={'class': 'content-link spf-link yt-uix-sessionlink spf-link'})

        if len(res) == 0:
            open('/tmp/dump.html', 'w').write(str(self.page))
            raise ValueError('No suggested links found for ' + self.url)

        self.title = self.page.title.text
        self.suggested = []
        for s in res[:TREE_WIDTH]:
            self.suggested.append(Link(s.attrs['title'], s.attrs['href']))

    def __str__(self):
        return self.title

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.url == other.url
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def recur(self):
        if Page in map(type, self.suggested):
            return

        for i in range(len(self.suggested)):
            print '\tPaging', i + 1, 'out of', len(self.suggested), '...',
            self.suggested[i] = Page(self.suggested[i])
            print 'Done'

    def contains(self, link):
        if type(link) == Link:
            link = link.url

        for s in self.suggested:
            if s.url == link:
                return True

        return False



db = {}
vid_page_url = 'https://www.youtube.com/watch?v=dCGS067s0zo'

print 'Getting page from', vid_page_url, '...',
p = Page(vid_page_url)
print 'Done'

current_level = [p]
rings = [current_level]
weights = []

for i in range(RECUR_DEPTH):
    # Call recur to convert all leaf nodes into Pages instead of Links
    for page in current_level:
        page.recur()
    
    print 'Recur lvl', i + 1, 'complete'

    # Put all leaf nodes into a single list
    current_level = [item for sublist in map(lambda x: x.suggested, current_level) for item in sublist]

    # How often each previous page appears in the current level
    level_weight = [current_level.count(page) for page in rings[-1]]

    print 'Weights:', level_weight
    weights.append(level_weight)

    rings.append(current_level)

    # Update the db for stat distribution
    for l in current_level:
        db[l.title] = db.setdefault(l.title, 0) + 1

most_common = max(db.iteritems(), key=operator.itemgetter(1))[0]

print 'Most common video:'
print most_common

counts = db.values()
counts.sort(reverse=True)

plt.bar(range(len(counts)),counts)
plt.show()

img = []
max_len = len(weights[-1])
for w in weights:
    n = max_len-len(w)
    l = n/2
    r = n-l
    a = np.pad(w, (l,r), 'constant',constant_values=0)
    img.append(a)

plt.imshow(img, interpolation='gaussian')
plt.show()
