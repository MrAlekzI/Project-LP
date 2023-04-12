import random


def random_seq(size):
    dna_symbols = ["a", "t", "g", "c"]
    if size >= 10 and size <= 100000:  # задаём ограничение длины последовательности
        random_seq = "".join([random.choice(dna_symbols) for symbol in range(size)])  # рандомно набираем допустимые символы согласно требуемой длине
        random.shuffle(random_seq)  # перемешиваем ещё раз
        return random_seq
    else:
        raise ValueError("Недопустимая длина последовательности")
    

if __name__ == '__main__':

    size = int(input())
    random_seq(size)