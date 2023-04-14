import random

class LengthError(ValueError):
    pass

def random_seq(size):
    dna_symbols = ["a", "t", "g", "c"]
    if size >= 10 and size <= 100000:  # задаём ограничение длины последовательности
        random_seq_list = [random.choice(dna_symbols) for symbol in range(size)]  # рандомно набираем допустимые символы согласно требуемой длине
        random.shuffle(random_seq_list)  # перемешиваем ещё раз
        random_seq = ''.join(random_seq_list)
        return random_seq
    else:
        raise LengthError("Недопустимая длина последовательности")
    

if __name__ == '__main__':

    size = int(input())
    print(random_seq(size))