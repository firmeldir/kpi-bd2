import time
import redis
import random
from threading import Thread

class MessageListWorker(Thread):
    def __init__(self, connect, delay):
        Thread.__init__(self)
        self.connect = connect
        self.delay = delay

    def run(self):
        status = 'status'
        while 1:
            getQueryMessageFromService = self.connect.brpop('queue:')

            if getQueryMessageFromService:
                statusMessage = int(getQueryMessageFromService[1])
                self.connect.hmset(f'message:{statusMessage}', {
                    status: 'check'
                })
                statusMessage = self.connect.hmget(f'message:{statusMessage}',['messageFromId', 'recipientId'])
                idMessage = int(statusMessage[0])
                recipientId = int(statusMessage[1])
                self.getReload(idMessage)
                if random.random() > 0.3:
                    self.toSpam(idMessage, statusMessage)
                else:
                    status = 'status'
                    self.connect.hmset(f'message:{statusMessage}', {
                        status: 'sent'
                    })
                    self.connect.hincrby(f'user:{idMessage}', 'sent', 1)
                    self.connect.sadd(f'sentto:{recipientId}', statusMessage)

    def getReload(self, idMessage):
        self.connect.hincrby(f'user:{idMessage}', 'queue', -1)
        self.connect.hincrby(f'user:{idMessage}', 'check', 1)
        time.sleep(self.delay)
        self.connect.pipeline(True)
        self.connect.hincrby(f'user:{idMessage}', 'check', -1)

    def toSpam(self, idMessage, statusMessage):
        status = 'status'
        fromLogin = self.connect.hmget(f'user:{idMessage}', ['login'])[0]
        self.connect.zincrby('spam:', 1, f'user:{idMessage}')
        self.connect.hmset(f'message:{statusMessage}', {
            status: 'block'
        })
        self.connect.hincrby(f'user:{idMessage}', 'block', 1)
        message = self.connect.hmget(f'message:{statusMessage}', ['text'])[0]
        self.connect.publish('spam', f'User {fromLogin} sent spam message: {message}')


if __name__ == '__main__':
    for x in range(1):
        handlers = random.randint(0, 3)
        connection = redis.Redis(charset='UTF-8', decode_responses=True)
        queryWorkers = MessageListWorker(connection, handlers)
        queryWorkers.daemon = True
        queryWorkers.start()
    while 1:
        pass
