import functools
import operator
import os
import random

import tabulate


def get_m_k() -> tuple[int, int]:
    """
    Получить пару кол-во куч, максимум спичек за ход
    """
    while True:
        try:
            m = int(input('Введите кол-во куч (m): '))
            break
        except ValueError:
            print('Ошибка ввода, попробуйте еще раз')

    while True:
        try:
            k = int(input('Введите макс число спичек за ход (k): '))
            break
        except ValueError:
            print('Ошибка ввода, попробуйте еще раз')

    return m, k


def create_heaps(heaps_count: int, max_step: int) -> list[int]:
    def determine_should_fill_random():
        while True:
            i = input('Сгенерировать кучи случайно? (д/н)')
            if 'д' in i or 'y' in i:
                return True
            if 'н' in i or 'n' in i:
                return False
            print('Не понял')
    fill_random = determine_should_fill_random()
    if fill_random:
        max_items = max_step * 2 + 1
        print(f"Генерирую {heaps_count} куч. Максимальное количество спичек: {max_items}")
        return [
            random.randint(1, max_items)
            for _ in range(heaps_count)
        ]

    result = [0] * heaps_count
    for i in range(heaps_count):
        while True:
            try:
                items_count = int(input(f'Введите кол-во спичек для {i} кучи: '))
                if items_count < 1:
                    print('Кол-во элементов не может быть отрицательным')
                    continue
                result[i] = items_count
                break
            except ValueError:
                print("Не удалось спарсить число. Повторите заново")
    return result


class NimState:
    heaps: list[int]
    max_to_take: int

    def __init__(self, heaps, max_step):
        self.heaps = heaps
        self.max_to_take = max_step

    @property
    def end(self):
        """
        Достигнут ли конец игры
        :return:
        """
        return not any(self.heaps)

    def make_step(self, heap_index: int, to_take: int):
        """
        Сделать один ход

        :param heap_index: Номер кучи
        :param to_take: Кол-во спичек
        :raises ValueError: Ошибка хода, повторить ход
        """
        if to_take == 0:
            raise ValueError('Нельзя ничего не брать. Хотя бы одну')
        if self.max_to_take < to_take:
            raise ValueError(f'Нельзя брать больше {self.max_to_take} спичек')
        if not (0 <= heap_index < len(self.heaps)):
            raise ValueError(f'Кучи {heap_index} не существует. Есть с 0 до {len(self.heaps) - 1} включительно')
        items = self.heaps[heap_index]
        if items < to_take:
            raise ValueError(f'В куче {heap_index} осталось только {items} спичек. Выбери другое число')
        items -= to_take
        self.heaps[heap_index] = items

    def calculate_xor(self):
        return functools.reduce(operator.xor, map(lambda x: x % (self.max_to_take + 1), self.heaps))

    def is_win_step(self):
        """
        Является ли текущий ход выигрышным, если бы я сейчас сходил?
        """
        return self.calculate_xor() != 0

    def determine_best_step(self) -> tuple[int, int]:
        """
        Определить лучший ход в текущей позиции
        :return: Пару индекс кучи и кол-во спичек, чтобы взять
        """
        # Находим общий XOR
        total_xor = self.calculate_xor()

        # Находим позицию бита, который надо инвертировать
        index_to_change = int.bit_length(total_xor)
        if index_to_change == 0:
            raise ValueError('Позиция идеальна. Ходов делать не надо')

        mask = 1 << (index_to_change - 1)

        for index, items_count in enumerate(self.heaps):
            if items_count == 0:
                # Пропускаем пустые кучи
                continue

            # Находим число, у числа гранди которого, это бит выставлен
            if mask & (items_count % (self.max_to_take + 1)) == 0:
                continue

            for number in range(1, self.max_to_take + 1):
                temp_heaps = list(self.heaps)
                temp_heaps[index] = items_count - number
                if ((items_count - number) % (self.max_to_take + 1)) == 0:
                    return index, number

                # Этот код чтобы наверняка, но пока не буду использовать

                # success = functools.reduce(operator.xor, map(lambda x: x % (self.max_to_take + 1), temp_heaps)) == 0
                # if success:
                #     return index, number

        # Сюда можем попасть только, если не нашли решение

        raise ValueError(f'Не удалось найти подходящее число. {total_xor = }')


def print_state(nim: NimState):
    table = tabulate.tabulate({
        "Куча": list(range(len(nim.heaps))),
        "Размер": nim.heaps
    }, tablefmt='outline')
    print(table)


def get_user_input(max_step: int):
    heap, to_remove = 0, 0
    while True:
        try:
            heap = int(input('Введите номер кучи: '))
            if heap < 0:
                print("Меньше 0 куч нет")
                continue
            break
        except ValueError:
            continue

    while True:
        try:
            to_remove = int(input(f'Введите сколько взять (не больше {max_step}): '))
            if to_remove < 1:
                print('Меньше 1 удалить нельзя')
                continue
            break
        except ValueError:
            continue

    return heap, to_remove


def main():
    heaps_count, max_step = get_m_k()
    heaps = create_heaps(heaps_count, max_step)
    nim = NimState(heaps, max_step)
    user_step = not nim.is_win_step()

    while not nim.end:
        print_state(nim)
        if user_step:
            # Пользователь ходит
            while True:
                heap, to_remove = get_user_input(max_step)

                try:
                    nim.make_step(heap, to_remove)
                    break
                except ValueError as ve:
                    print(ve.args)
                    continue

            if nim.end:
                print('Пользователь победил. Невозможно!!')
                break
        else:
            index, to_subtract = nim.determine_best_step()
            print(f'Компьютер берет {to_subtract} спичек из {index} кучи')
            nim.make_step(index, to_subtract)
            if nim.end:
                print('Компьютер победил. УРААА')
                break

        user_step = not user_step


if __name__ == '__main__':
    main()

