# coding=utf-8
# python simple_guiclient.py urlfile.txt files http://localhost:8080
from xmlrpclib import ServerProxy, Fault
from server import Node, UNHANDLED
from client import randomString
from threading import Thread
from time import sleep
from os import listdir
import sys
import wx

HEAD_START = 0.1   #  Second
SECRET_LENGTH = 100


class ListtableNode(Node):
    def list(self):
        return listdir(self.dirname)

class Client(wx.App):
    def __init__(self, url, dirname, urlfile):
        self.secret = randomString(SECRET_LENGTH)
        n = ListtableNode(url, dirname, self.secret)
        t = Thread(target=n._start)
        t.setDaemon(1)
        t.start()
        sleep(HEAD_START)
        self.server = ServerProxy(url)
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)
        super(Client, self).__init__()

    def updateList(self):
        self.files.Set(self.server.list())

    def OnInit(self):
        win = wx.Frame(None, title="File Sharing Client", size=(400, 300))
        bkg = wx.Panel(win)
        self.input = input = wx.TextCtrl(bkg)

        submit = wx.Button(bkg, label="Fetch", size=(80, 25))
        submit.Bind(wx.EVT_BUTTON, self.fetchHandler)

        hbox = wx.BoxSizer()
        hbox.Add(input, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        hbox.Add(submit, flag=wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)

        self.files = files = wx.ListBox(bkg)
        self.updateList()

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND)
        vbox.Add(files, proportion=1,
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        bkg.SetSizer(vbox)

        win.Show()
        return True

    def fetchHandler(self, event):
        query = self.input.GetValue()
        try:
            self.server.fetch(query, self.secret)
            self.updateList()

        except Fault as f:
            if f.faultCode != UNHANDLED: raise
            print "Couldn't find the file", query


def main():
    urlfile, directory, url = sys.argv[1:]
    client = Client(url, directory, urlfile)
    client.MainLoop()

if __name__ == "__main__": main()