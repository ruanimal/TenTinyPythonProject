#!C:\\Python27\\python.exe
# coding=utf-8

print 'Content-type: text/html\r\n'

from os.path import join, abspath
import cgi, sys, sha

BASE_DIR = abspath('data')

form = cgi.FieldStorage()
text = form.getvalue('text')
filename = form.getvalue('filename')
password = form.getvalue('password')

if not (filename and password):
    print 'Invalid parameters'
    sys.exit()

if sha.sha(password).hexdigest() != '8843d7f92416211de9ebb963ff4ce28125932878':
    print 'Invalid password'  ## password is "foobar"
    sys.exit()

f = open(join(BASE_DIR, filename), 'w')
f.write(text)
f.close()

print 'The file has been saved'
