import urllib2
from bs4 import BeautifulSoup
import operator


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
            raise ValueError('No suggested links found for ' + self.url)

        self.title = self.page.title.text
        self.suggested = []
        for s in res[:3]:
            self.suggested.append(Link(s.attrs['title'], s.attrs['href']))

    def __str__(self):
        return self.title

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
vid_page_url = 'https://www.youtube.com/watch?v=dBbKtOvfTiE'

print 'Getting page from', vid_page_url, '...',

p = Page(vid_page_url)

print 'Done'
print 'Creating pages from suggestions...'
p.recur()
print 'Done'

c = map(lambda x: x.contains(vid_page_url), p.suggested).count(True)

print c, 'pages from the original suggestions contain the original video'

level = [p]
for i in range(3):
    for page in level:
        page.recur()
    print 'Recur lvl', i + 1, 'complete'
    level = [item for sublist in map(lambda x: x.suggested, level) for item in sublist]
    # map(lambda x: db[x.title] = db.setdefault(x.title, 0) + 1, level)
    for l in level:
        db[l.title] = db.setdefault(l.title, 0) + 1

most_common = max(db.iteritems(), key=operator.itemgetter(1))[0]

print 'Most common video:'
print most_common

counts = db.values()
