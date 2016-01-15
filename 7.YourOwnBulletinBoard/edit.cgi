#!C:\\Python27\\python.exe

print 'Content-type: text/html\r\n'
import cgitb; cgitb.enable()

import sqlite3
conn = sqlite3.connect('db.sqlite')
curs = conn.cursor()

import cgi, sys
form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')

print """
<html>
  <head>
    <title>Compose Message</title>
  </head>
  <body>
    <h1>Compose Message</h1>
    <form action="save.cgi" method="POST">
"""

subject = ''
if reply_to is not None:
    print '<input type="hidden" name="reply_to" value="%s"/>' % reply_to
    curs.execute('SELECT subject FROM messages WHERE id = %s' % reply_to)
    subject = curs.fetchone()[0]
    if not subject.startswith('Re:'):
        subject = 'Re: ' + subject

print """
    <b>Subject:</b><br />
    <input type="text" name="subject" size="40" value="%s"/><br />
    <b>Sender:</b><br />
    <input type="text" name="sender" size="40"/><br />
    <b>Message:</b><br />
    <textarea name="text" cols="40" rows="20"></textarea><br />
    <input type="submit" value="Save"/>
    </form>
    <hr />
    <a href="main.cgi">Back to the main page</a>
    </body>
</html>
""" % subject