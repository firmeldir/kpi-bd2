def startMenu():
    print('-' * 30)
    print('|1| User registration')
    print('-' * 30)
    print('|2| User authorization')
    print('-' * 30)
    print('|0| Exit')
    print('-' * 30)
    return int(input('Enter a number: '))


def userMenu():
    print('-' * 30)
    print('|1| Send a message')
    print('-' * 30)
    print('|2| Messages')
    print('-' * 30)
    print('|3| Types of messages')
    print('-' * 30)
    print('|0| Exit')
    print('-' * 30)
    return int(input('Enter a number: '))

def adminMenu():
    print('-' * 30)
    print('|1| Users')
    print('-' * 30)
    print('|2| The most active senders')
    print('-' * 30)
    print('|3| The most active spammers')
    print('-' * 30)
    print('|0| Exit')
    print('-' * 30)