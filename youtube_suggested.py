import urllib2
import urllib
from bs4 import BeautifulSoup
import operator
from random import sample
import matplotlib.pyplot as plt
import numpy as np
from cookielib import CookieJar


RECUR_DEPTH = 35  # How deep into YT to go
TREE_WIDTH = 2  # How many suggested videos to click on
LIMIT_WIDTH = 10  # How many samples from all suggested videos to take
SPREAD = 2  # How many suggested videos to click on After reaching LIMIT_WIDTH
EXP_DECIMATION = 1.5  # How bias against videos farther from center to weigh against

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

class Link(object):
    def __init__(self, title, href):
        self.title = title.strip()
        self.url = 'https://www.youtube.com' + href

    def __str__(self):
        return self.title


class SearchPage(object):
    def __init__(self, keyword):
        self.url = 'https://www.youtube.com/results?search_query='+keyword

        # vid_page_src = urllib2.urlopen(self.url)
        vid_page_src = opener.open(self.url)

        if vid_page_src is None:
            raise ValueError('Failed to load ' + self.url)

        self.page = BeautifulSoup(vid_page_src, 'html.parser')

        res = self.page.find_all('a',
                                 attrs={'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})
        if len(res) == 0:
            # Sometimes the html class doesnt have spaces and bs4 doesn't strip
            #    so we gotta look again
            res = self.page.find_all('a',
                                     attrs={'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link '})

        if len(res) == 0:
            open('/tmp/search_dump.html', 'w').write(str(self.page))
            raise ValueError('No search results found for ' + self.url)

        self.results = []
        for s in res:
            self.results.append(Link(s.attrs['title'], s.attrs['href']))


class Page(object):
    def __init__(self, link):
        if type(link) == Link:
            vid_page_src = opener.open(link.url)
            self.url = link.url
        else:
            vid_page_src = opener.open(link)
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

kw = ''

s = SearchPage(urllib.quote_plus(kw))

vid_page_url = s.results[0]

print 'Getting page from', vid_page_url, '...',
p = Page(vid_page_url)
print 'Done'

current_level = [p]
rings = []
weights = []

for i in range(RECUR_DEPTH):
    # Call recur to convert all leaf nodes into Pages instead of Links
    for page in current_level:
        page.recur()
    
    print 'Recur lvl', i + 1, 'complete'

    # Put all leaf nodes into a single list
    current_level = [item for sublist in map(lambda x: x.suggested, current_level) for item in sublist]
    # Pick out random samples to prevent exponential growth
    current_level = sample(current_level, min(LIMIT_WIDTH, len(current_level)))
    
    if len(current_level) == LIMIT_WIDTH:
        TREE_WIDTH = SPREAD
        level_weight = [float(0)] * LIMIT_WIDTH
        for i, ring in enumerate(rings):
            print '\tRaw vals for ring', i, [current_level.count(page) for page in ring]
            new_vals = [float(current_level.count(page))/((i+1)**EXP_DECIMATION) for page in ring]
            level_weight = map(operator.add, new_vals, level_weight)

        print 'Weights:', level_weight
        weights.append(level_weight)

        rings.append(current_level)

    # Update the db for stat distribution
    for l in current_level:
        db[l.title] = db.setdefault(l.title, 0) + 1

most_common = max(db.iteritems(), key=operator.itemgetter(1))[0]

try:
    print map(str, rings[0])
except UnicodeEncodeError:
    print 'Unicode mess detected'

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
