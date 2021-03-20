import random
import redis
import atexit
from faker import Faker
from threading import Thread
from service import Service


class Thread(Thread):
    def __init__(self, connect, log, initList):
        Thread.__init__(self)
        self.c = connect
        self.d = Service(self.c)
        self.d.registration(login)
        self.id = self.d.log(log)
        self.l = initList

    def run(self):
        choice = random.choice(self.l)
        messages = Faker().sentence(nb_words=7)
        self.d.sendMessage(messages, self.id, choice)

def startThread(threads):
    for thread in threads:
        thread.start()

def end():
    online = 'online'
    connection = redis.Redis(charset='utf-8', decode_responses=True)
    online = connection.smembers(online)
    connection.srem(online, list(online))


if __name__ == '__main__':
    atexit.register(end)
    logs = 'username'
    loginUsers = [Faker().profile(fields=[logs])[logs] for exist in range(3)]
    threads = []
    print(loginUsers)
    for login in loginUsers:
        threads.append(Thread(redis.Redis(charset='utf-8', decode_responses=True), login, loginUsers))
    startThread(threads)
