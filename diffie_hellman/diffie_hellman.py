import logging
import sys
from contextlib import contextmanager
from itertools import cycle
from random import randint
import socket
from typing import ContextManager

from generator_finder import get_generator
from utils import power_mod


# Число Мерсена (4 байтное, для удобства)
# https://ru.wikipedia.org/wiki/Список_простых_чисел
POWER_PRIME = 162259276829213363391578010288127  # 107 бит

# Общее число, в которое возводится степень - генератор
BASE = get_generator(POWER_PRIME)

MSG_SIZE = 16


class DiffieHellmanClient:
    socket: socket.socket
    private_key: list[int]

    def __init__(self, private_key: int, sock: socket):
        self.private_key = list(private_key.to_bytes(MSG_SIZE, byteorder=sys.byteorder))  # 128 байт
        self.socket = sock

    def __aenter__(self):
        return self

    def send(self, message: str):
        encoded = encode(message, self.private_key)
        self.socket.send(encoded, )

    def receive(self) -> str:
        received = self.socket.recv(512)
        return decode(received, self.private_key)

    def close(self):
        self.socket.close()
        self.private_key = None


@contextmanager
def accept_client(host: str = '0.0.0.0', port: int = 8080) -> ContextManager[DiffieHellmanClient]:
    """
        Принять нового клиента
        и установить защищенное соединение
    """
    # Генерируем свой ключ
    my_power = randint(1, 10000000000)

    # Отправляем его на сервер и получаем его ключ
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP) as server_socket:
        logging.debug('Бинжу адрес %s:%i', host, port)
        server_socket.bind((host, port))
        server_socket.listen(1)
        logging.debug('Слушаю подключения')
        sock, addr = server_socket.accept()
        with sock as sock:
            server_socket.close()

            logging.debug('Подключился клиент с адреса %s. Читаю его число', addr)
            client_number = int.from_bytes(sock.recv(MSG_SIZE))
            logging.debug('Число клиента получено. Отправляю свое')
            powered = power_mod(BASE, my_power, POWER_PRIME)
            sock.send(powered.to_bytes(MSG_SIZE))

            private_key = power_mod(client_number, my_power, POWER_PRIME)
            yield DiffieHellmanClient(private_key, sock)


@contextmanager
def connect_to_server(host: str = '0.0.0.0', port: int = 8080) -> ContextManager[DiffieHellmanClient]:
    """
    Подключиться к серверу и
    установить новое защищенное соединение
    """
    # Генерируем свой ключ
    my_power = randint(1, 10000000000)

    # Отправляем его на сервер и получаем его ключ
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logging.debug('Подключаюсь по адресу %s:%i', host, port)
        sock.connect((host, port))
        logging.debug("Отправляю свой ключ на сервер. Ключ: %i", my_power)
        powered = power_mod(BASE, my_power, POWER_PRIME)
        sock.send(powered.to_bytes(MSG_SIZE))
        logging.debug('Получаю ключ сервера')
        data = sock.recv(MSG_SIZE)
        server_number = int.from_bytes(data)
        private_key = power_mod(server_number, my_power, POWER_PRIME)
        logging.debug('Рассчитанный ключ %i', private_key)
        yield DiffieHellmanClient(private_key, sock)


def encode(data: str, key: list[int]) -> bytes:
    encoded = data.encode()
    result = [
        d ^ k
        for d, k in zip(encoded, cycle(key))
    ]
    return bytes(result)


def decode(data: bytes, key: list[int]) -> str:
    result = [
        d ^ k
        for d, k in zip(data, cycle(key))
    ]
    return bytes(result).decode()

