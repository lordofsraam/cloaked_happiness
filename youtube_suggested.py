import urllib2
from bs4 import BeautifulSoup

class Link(object):
    def __init__(self, title, href):
        self.title = title.strip()
        self.url = 'https://www.youtube.com'+href

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

        self.page = BeautifulSoup(vid_page_src, 'html.parser')
        res = self.page.find_all('a', 
                        attrs={'class': ' content-link spf-link yt-uix-sessionlink spf-link '})
        
        self.title = self.page.title.text
        self.suggested = []
        for s in res:
            self.suggested.append(Link(s.attrs['title'], s.attrs['href']))

    def __str__(self):
        return self.title

    def recur(self, exclude=None):
        if Page in map(type, self.suggested):
            return
        
        for i in range(len(self.suggested)):
            print '\tPaging', i+1, 'out of', len(self.suggested), '...',
            self.suggested[i] = Page(self.suggested[i])
            print 'Done'

    def contains(self, link):
        if type(link) == Link:
            link = link.url
        
        for s in self.suggested:
            if s.url == link:
                return True
        
        return False


vid_page_url = 'https://www.youtube.com/watch?v=0sqhSybK0P0'

print 'Getting page from', vid_page_url, '...',

p = Page(vid_page_url)

print 'Done'
print 'Creating pages from suggestions...'
p.recur()
print 'Done'

c = map(lambda x: x.contains(vid_page_url), p.suggested).count(True)

print c, 'pages from the original suggestions contain the original video'
