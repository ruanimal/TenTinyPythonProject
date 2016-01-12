#coding=utf-8
"""
NewsAgent有两种类型的新闻来源， SimpleWebSource 和 NNTPSourse。
NewsAgent通过addSourse添加来源，通过addDestination添加Destination。
这两个来源通过getItems将新闻包装成'NewsItem'生成器对象，每个'NewsItem'有title,body两个属性。
NewsAgent.distribute方法将所有来源的NewsItem分发到各个Destination处理。
各个Destination，通过receiveItems方法处理NewItes，生产不同类型的新闻聚合。
"""

from nntplib import NNTP
from time import strftime, time, localtime
from email import message_from_string
from urllib import urlopen
import textwrap
import re

day = 24 * 60 * 60   # seconds of a day
def wrap(string, max=70):
    return '\n'.join(textwrap.wrap(string)) + '\n'


class NewsAgent(object):
    def __init__(self):
        self.sourses = []
        self.destinations = []

    def addSourse(self, sourse):
        self.sourses.append(sourse)

    def addDestination(self, dest):
        self.destinations.append(dest)

    def distribute(self):
        items = []
        for sourse in self.sourses:
            items.extend(sourse.getItems())
        for dest in self.destinations:
            dest.receiveItems(items)

class NewsItem(object):
    def __init__(self, title, body):
        self.title = title
        self.body = body

class NNTPSourse(object):
    def __init__(self, servername, group, window):
        self.servername = servername
        self.group = group
        self.window = window

    def getItems(self):
        start = localtime(time() - self.window*day)
        date = strftime('%y%m%d', start)
        hour = strftime('%H%M%S', start)

        server = NNTP(self.servername)

        ids = server.newnews(self.group, date, hour)[1]
        for id in ids:
            lines = server.article(id)[3]
            message = message_from_string('\n'.join(lines))

            title = message['subject']
            body = message.get_payload()
            if message.is_multipart():
                body = body[0]

            yield NewsItem(title, body)

        server.quit()

class SimpleWebSource(object):
    def __init__(self, url, titlePattern, bodyPattern):
        self.url = url
        self.titlePattern = re.compile(titlePattern)
        self.bodyPattern = re.compile(bodyPattern)

    def getItems(self):
        text = urlopen(self.url).read()
        titles = self.titlePattern.findall(text)
        bodies = self.bodyPattern.findall(text)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, wrap(body))

class PlainDestination(object):
    def receiveItems(self, items):
        for item in items:
            print item.title
            print '-'*len(item.title)
            print item.body

class HTMLDestination(object):
    def __init__(self, filename):
        self.filename = filename

    def receiveItems(self, items):
        out = open(self.filename, 'w')
        print >> out, '''
        <html>
            <head>
            <title>Today' News</title>
            </head>
            <body>
            <h1>Today's News</h1>
        '''

        print >> out, '<ul>'
        id = 0
        for item in items:
            id += 1
            print >> out, '<li><a href="#%i">%s</a></li>' % (id, item.title)
        print >> out, '</ul>'
        
        id = 0
        for item in items:
            id += 1
            print >> out, '<h2><a name="%i">%s</a></h2>' % (id, item.title)
            print >> out, '<pre>%s</pre>' % item.body

        print >> out, """
            </body>
        </html>
        """

def runDefaultSetup():
    agent = NewsAgent()

    bbc_url = 'http://news.bbc.co.uk/text_only.stm'    # 该来源已失效
    bbc_title = r'(?s)a href="[^"]*">\s*<b>\s*(.*?)\s*</b>'
    bbc_body = r'(?s)</a>\s*<br />\s*(.*?)\s*<'
    bbc = SimpleWebSource(bbc_url, bbc_title, bbc_body)

    agent.addSourse(bbc)

    clpa_server = 'news.mixmin.net'  #可访问http://www.freeusenetnews.com/获取nntp服务器
    clpa_group = 'talk.euthanasia'
    clap_window = 10
    clpa = NNTPSourse(clpa_server, clpa_group, clap_window)

    agent.addSourse(clpa)

    agent.addDestination(PlainDestination())
    agent.addDestination(HTMLDestination('news.html'))

    agent.distribute()

if __name__ == "__main__": runDefaultSetup()
