#!C:\Python27\python.exe
# addmessage.py
"""
create table messages (
    id          integer primary key autoincrement, 
    subject     text not null,
    sender      text not null,
    reply_to    int,
    text        text not null);
"""
import sqlite3
conn = sqlite3.connect('db.sqlite')
curs = conn.cursor()

reply_to = raw_input('Reply_to: ')
subject = raw_input('Subject: ')
sender = raw_input('Sender: ')
text = raw_input('Text: ')

if reply_to:
    query = """
    INSERT INTO messages(reply_to, sender, subject, text)
    VALUES('%i', '%s', '%s', '%s')""" % (reply_to, sender, subject, text)
else:
    query = """
    INSERT INTO messages(sender, subject, text)
    VALUES('%s', '%s', '%s')""" % (sender, subject, text)

curs.execute(query)
conn.commit()