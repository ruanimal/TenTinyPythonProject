#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""虚拟茶话会和qq群类似。
LoginRoom、ChatRoom、LogoutRoom 管理自己内部的多个session，响应session的命令
session有进入房间、关闭、发送消息的响应的方法
"""

import asyncore, socket
from asyncore import dispatcher
from asynchat import async_chat


PORT = 5005
NAME = 'TestChat'

class EndSession(Exception):
    pass


class CommandHandler(object):
    """
    处理用户输入命令，并尝试调用对应的方法，Room的父类
    """
    def unknown(self, session, cmd):
        session.push('Unknown command: %s\r\n' % cmd)

    def handle(self, session, line):
        if not line.strip(): return
        parts = line.strip().split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError, e:
            line = ''
        meth = getattr(self, 'do_'+cmd, None)
        try:
            meth(session, line)
        except TypeError:
            self.unknown(session, cmd)


class Room(CommandHandler):
    """
    管理当前room的session，通过add、remove、do_logout操作
    """
    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def remove(self, session):
        self.sessions.remove(session)

    def broadcast(self, line):
        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        raise EndSession


class LoginRoom(Room):
    """
    处理login， 覆写unknown方法
    """
    def add(self, session):
        Room.add(self,session)
        self.broadcast('Welcome to %s\r\n' % self.server.name)

    def unknown(self, session, cmd):
        session.push('Please log in\nUse "login <nick>"\r\n')

    def do_login(self, session, line):
        name = line.strip()
        if not name:
            session.push('Please enter a name\r\n')
        elif name in self.server.users:
            session.push('The name "%s" is taken.\r\n' % name)
            session.push('Please try again.\r\n')
        else:
            session.name = name
            session.enter(self.server.main_room)


class ChatRoom(Room):
    def add(self, session):
        self.broadcast(session.name + 'has entered the room.\r\n')
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        Room.remove(self, session)
        self.broadcast(session.name+' has left the romm.\r\n')

    def do_say(self, session, line):
        self.broadcast(session.name+': '+line+'\r\n' )

    def do_look(self, session, line):
        session.push('The following are in this room: \r\n')
        for other in self.sessions:
            session.push(other.name + '\r\n')

    def do_who(self, session, line):
        for name in self.server.users:
            session.push(name + '\r\n')


class LogoutRoom(Room):
    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError as e:
            pass

class ChatSession(async_chat):
    '''
    接收socket，调用LoginRoom处理用户的登录。
    '''
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator('\r\n')
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    def enter(self, room):
        try:
            cur = self.room
        except AttributeError as e:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))


class ChatServer(dispatcher):
    '''
    服务器类，初始化socket并监听端口，初始化users字典用于记录用户session，
    处理socket连接，并且新建相应的session
    '''

    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)


if __name__ == "__main__":
    s = ChatServer(PORT, NAME)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print




