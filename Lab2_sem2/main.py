import redis
import atexit
from service import Service
from lab2.allMenus import startMenu
from lab2.allMenus import userMenu

def main():
    connect = redis.Redis(charset='UTF-8', decode_responses=True)
    serv = Service(connect)
    crntId = -1

    def endH():
        serv.logout(crntId)

    atexit.register(endH)
    menu = startMenu
    while 1:
        state = menu()
        if state == 1:
            login = input('Please enter login: ')
            serv.registration(login)
        elif state == 2:
            login = input('Please enter login: ')
            crntId = serv.login(login)
            if crntId != -1:
                connect.publish('users', f'User {login} connected')
                while 1:
                    state = userMenu()
                    if state == 1:
                        message = input('message: ')
                        recipient = input('recipient login: ')
                        serv.sendMessage(message, crntId, recipient)

                    elif state == 2:
                        mssList = serv.connection.smembers(f'sentto:{crntId}')
                        for mssId in mssList:
                            message = serv.connection.hmget(f'message:{mssId}',
                                                               ['messageFromId', 'text', 'status'])
                            mssId = message[0]
                            getValueFrom = serv.connection.hmget(f'user:{mssId}', ['login'])[0]
                            print(f'Message by: {getValueFrom} - {message[1]} ')
                            if message[2] != 'deliver':
                                connectPipeline = serv.connection.pipeline(True)
                                connectPipeline.hset(f'message:{mssId}', 'status', 'deliver')
                                connectPipeline.hincrby(f'user:{mssId}', 'sent', -1)
                                connectPipeline.hincrby(f'user:{mssId}', 'deliver', 1)
                                connectPipeline.execute()
                    elif state == 3:
                        loggedUser = connect.hmget(f'user:{crntId}',['create', 'check', 'block', 'sent', 'total'])
                        print('CREATE message: {} || CHECK message: {} ||BLOCK message: {} ||SENT message: {} '
                              '||TOTAL message: {} '
                                .format(*tuple(loggedUser)))
                    elif state == 0:
                        serv.logout(crntId)
                        connect.publish('users', f'User signed out')
                        return
        elif state == 0:
            return


if __name__ == '__main__':
    main()
