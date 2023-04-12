class InputDNA:

    dna_symbols = ["a", "t", "g", "c", "u", "n"] #допустимые символы

    def __init__(self, sequence:str) -> str:
        self.initial_seq = sequence.lower().strip() #приводим к нижнему регистру и стрипим
        self.counter = 0 # счетчик недопустимых символов
        self.is_uracil = 0
        self.is_non_identified = 0
        self.__seq_format = [] # список для отформатированной строки, где удаляем недопустимые символы
        for symbol in self.initial_seq:
            if symbol in InputDNA.dna_symbols:  # посимвольное сравнение элемента исходной строки и добавление в новую, если символ допустимый
                if symbol == 'u': #заменяем u на t, записываем что нашли РНК символы
                    self.__seq_format.append('t')
                    self.is_uracil += 1
                else:
                    self.__seq_format.append(symbol)
                    if symbol == 'n': #такие тоже бывают при ошибках в секвенаторе - их лучше не удалять, но логировать
                        self.is_non_identified += 1
            else:
                self.counter += 1  # если находим недопустимый символ
            
        self.formated_sequence = "".join(self.__seq_format)  # отформатированный список преобразовываем в строку
        self.input_lenth = len(self.formated_sequence)
    
