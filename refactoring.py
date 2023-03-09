"""
Функция для случайной генерации ДНК последовательности выбраной длины

На ввод получает целое число  - требуемая длина, на вывод - строка из случайно сгенерированных символов agtc

"""

import random
from tkinter.messagebox import showwarning

dna_symbols = ["a", "t", "g", "c"]
# преобразовали введённую пользователем длину последовательность в целое число
size = int(input())


def random_seq():
    try:
        if size >= 100 and size <= 100000:  # задаём ограничение длины последовательности
            random_seq = "".join([random.choice(dna_symbols) for symbol in range(size)])  # рандомно набираем допустимые символы согласно требуемой длине
            random.shuffle(random_seq)  # перемешиваем ещё раз
            return random_seq
        else:
            raise ValueError()
    except ValueError:
        return "Недопустимая длина последовательности"


"""
Функция форматирования введенной последовательности: 
1. найти не atgc символы, сообщить что они найдены
2. если есть - вывести какой символ и его позицию в лог
3. если нет - вернуть в лог последовательность

в прошлой версии не atcg удалялись из последовательности
"""

seq = list(input().lower())  # преобразовали введённую пользователем последовательность в строку
counter = 0  # счетчик недопустимых символов
seq_format = []  # список для отформатированной строки с удаленными недопустимыми символами


def format_seq():
    for symbol in seq:
        if symbol in dna_symbols:  # посимвольное сравнение элемента исходной строки (переведённой в список) и добавление в новый список, если символ допустимый
            seq_format.append(symbol)
        else:
            counter += 1  # если находим недопустимый символ

    seq_format = "".join(seq_format)  # отформатированный список преобразовываем в строку

    if counter >= 1:
        showwarning(title="Warning!", message="Unavailable symbols were deleted")  # предупреждаем, что нашли и удалили недопустимые символы
        return seq_format
    else:
        return seq_format
