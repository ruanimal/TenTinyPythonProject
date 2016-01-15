#!C:\\Python27\\python.exe

print 'Content-type: text/html\r\n'
import cgitb; cgitb.enable()

import sqlite3
conn = sqlite3.connect('db.sqlite')
curs = conn.cursor()

import cgi, sys
form = cgi.FieldStorage()
id = form.getvalue('id')

print """
<html>
  <head>
    <title>View Message</title>
  </head>
  <body>
    <h1>View Message</h1>
"""

try:
    id = int(id)
except Exception as e:
    print 'Invalid message ID'
    print e
    sys.exit()

curs.execute('SELECT * FROM messages WHERE id = %i' % id)
names = [d[0] for d in curs.description]
rows = [dict(zip(names, row)) for row in curs.fetchall()]

if not rows:
    print 'Unknown message ID'
    sys.exit()

row = rows[0]

print """
    <p><b>Subject:</b> %(subject)s <br />
    <b>Sender:</b> %(sender)s <br />
    <pre>%(text)s</pre>
    </p>
    <hr />
    <a href="main.cgi">Back to the main page</a>
    | <a href="edit.cgi?reply_to=%(id)s">Reply</a>
  </body>
</html>
""" % row