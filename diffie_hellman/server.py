import logging
import socket

from diffie_hellman import accept_client


logging.basicConfig(level=logging.DEBUG)


def main():
    logging.info('Начинаю принимать клиентов')
    with accept_client(host=socket.gethostname()) as client:
        while True:
            answer = client.receive()
            print(f'> {answer}')
            question = input('> ')
            client.send(question)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.fatal('Ошибка во время работы программы', exc_info=e)
