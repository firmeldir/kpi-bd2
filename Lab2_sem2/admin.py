import logging
import redis
from threading import Thread
from service import Service
from lab2.allMenus import adminMenu

logging.basicConfig(filename='history.log', level=logging.INFO)

class InitListener(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

def connection():
    connect = redis.Redis(charset='utf-8', decode_responses=True)
    sub = InitListener(connect)
    sub.setDaemon(True)
    sub.start()
    return Service(connect)

if __name__ == '__main__':
    def mainMenu():
        adminMenu()
        return int(input('Enter a number: '))
    service = connection()
    while 1:
        switch = mainMenu()
        if switch != 1 and switch != 2 and switch != 3:
            print('exit')
            break
        elif switch == 1:
            service.initOnlineUsers()
        elif switch == 2:
            service.serviceSenders()
        elif switch == 3:
            service.serviceSpamers()
