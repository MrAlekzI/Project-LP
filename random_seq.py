import random

dna_symbols = ["a", "t", "g", "c"]

def random_seq(size):
    if size >= 100 and size <= 100000:  # задаём ограничение длины последовательности
        random_seq = "".join([random.choice(dna_symbols) for symbol in range(size)])  # рандомно набираем допустимые символы согласно требуемой длине
        random.shuffle(random_seq)  # перемешиваем ещё раз
        return random_seq
    else:
        raise ValueError("Недопустимая длина последовательности")