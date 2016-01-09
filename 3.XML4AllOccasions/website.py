# coding=utf-8
from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

class Dispatcher(object):
    """将不同类型的元素分发给不同的ContentHandler方法处理"""

    def dispatch(self, prefix, name, attrs=None):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        method = getattr(self, mname, None)
        if callable(method): 
            args = ()
        else:
            method = getattr(self, dname, None)
            args = name,  # 赋值表达式的后面加了逗号后，会自动得到一个tuple的对象。
        if prefix == 'start':
            args += attrs,  # 与上个注释相同, 省略“,”会出错。
        if callable(method): method(*args)

    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)

    def endElement(self, name):
        self.dispatch('end', name)


class WebsiteConstructor(Dispatcher, ContentHandler):
    
    passthrough = False
    
    def __init__(self, directory):
        self.directory = [directory]
        self.ensureDirectory()

    def ensureDirectory(self):
        path = os.path.join(*self.directory)
        if not os.path.isdir(path): os.makedirs(path)

    def characters(self, chars):
        if self.passthrough: self.out.write(chars)

    def defaultStart(self, name, attrs):
        if self.passthrough:
            self.out.write('<' + name)
            for key, val in attrs.items():
                self.out.write(' %s="%s"' % (key, val))
            self.out.write('>')

    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write('</%s>' % name)

    def startDirectory(self, attrs):
        self.directory.append(attrs['name'])
        self.ensureDirectory()

    def endDirectory(self):
        self.directory.pop()

    def startPage(self, attrs):
        filename = os.path.join(*self.directory + [attrs['name'] + '.html'])
        self.out = open(filename, 'w')
        self.writeHeader(attrs['title'])
        self.passthrough = True

    def endPage(self):
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeHeader(self, title):
        self.out.write('<html>\n<head>\n    <title>')
        self.out.write(title)
        self.out.write('</title>\n </head>\n    <body>\n')

    def writeFooter(self):
        self.out.write('\n </body>\n </html>\n')

parse('website.xml', WebsiteConstructor('public_html'))