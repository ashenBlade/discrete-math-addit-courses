import logging


from diffie_hellman import connect_to_server


def main():
    logging.info('Подключаюсь к серверу')
    with connect_to_server() as client:
        while True:
            question = input('> ')
            client.send(question)
            answer = client.receive()
            print(f'> {answer}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.fatal('Ошибка во время работы программы', exc_info=e)
