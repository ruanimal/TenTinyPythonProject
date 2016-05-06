#coding=utf-8
# output
class Handler:
    """HTMLRenderer的基类"""

    def callback(self, prefix, name, *args):
        """通过添加prefix调用特定的方法"""
        method = getattr(self, prefix+name, None)
        if callable(method): return method(*args)
    def start(self, name):
        """开始一个元素"""
        self.callback('start_', name)
    def end(self, name):
        """结束一个元素"""
        self.callback('end_', name)
    def sub(self, name):
        """返回相应的替换器"""
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: match.group(0)
            return result
        return substitution


class HTMLRenderer(Handler):
    """一些渲染规则"""

    def start_document(self):
        print '<html><head><title>...</title></head><body>'
    def end_document(self):
        print '</body></html>'
    def start_paragraph(self):
        print '<p>'
    def end_paragraph(self):
        print '</p>'
    def start_heading(self):
        print '<h2>'
    def end_heading(self):
        print '</h2>'
    def start_list(self):
        print '<ul>'
    def end_list(self):
        print '</ul>'
    def start_listitem(self):
        print '<li>'
    def end_listitem(self):
        print '</li>'
    def start_title(self):
        print '<h1>'
    def end_title(self):
        print '</h1>'
    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self, data):
        print data

