
def polytract_finder(sequence: str) -> dict:
    tract_dict = {}
    tract_count = 0
    tract_start = None
    tract_end = None
    for i in range(1, len(sequence)):
        current_nucleotide = sequence[i - 1]
        if sequence[i] == current_nucleotide and tract_start is None:
            tract_start = i - 1
        elif sequence[i] == current_nucleotide and tract_start is not None:
            if i == len(sequence) - 1: # проверяем не является ли посдедним нуклеотидом
                tract_end = i #записываем последный элемент как конец повтора
            else:
                continue
        elif sequence[i] != current_nucleotide and tract_start is None:        
            continue
        elif sequence[i] != current_nucleotide and tract_start is not None: #поиск конечного элемента
            tract_end = i - 1
        if tract_start is not None and tract_end is not None: #определяем длину повтроа и если он больше 4 записываем в словарь где ключи - нмоер повтрора
            if (tract_end - tract_start +1) > 4: 
                tract_count += 1 
                #каждый повтрор - слоарь hpt это сокращение homopolymer tract
                tract_dict[tract_count] = {'hpt_start': tract_start+1,
                                           'hpt_end': tract_end +1,
                                           'hpt_lenght' : tract_end - tract_start + 1,
                                           'hpt_type': current_nucleotide}
            tract_start = None
            tract_end = None
    return tract_dict


if __name__ == '__main__':
    test_1 = 'aaaagct' #длина повтора <5, повтро в начале
    test_2 = 'aaaaagct' #длина повтора >=5, повтор в начале
    test_3 = 'agctttt' #длина повтора <5, повтро в конце
    test_4 = 'agcttttt' #длина повтора >=5, повтор в конце
    test_5 = 'aggggct' #повтор в середине, <5
    test_6 = 'agggggct'  #повтор в середине, >=5
    test_7 = 'aaaaattttt' #два примыкающих повтра >=5
    test_8 = 'aaaattttt' #два примыкающих повтра <5, =>5
    test_9 = 'aaaaatttt' #два примыкающих повтра >=5, <5
    
    #проверка сколько найдется
    assert(len(polytract_finder(test_1)) == 0)
    assert(len(polytract_finder(test_2)) == 1)
    assert(len(polytract_finder(test_3)) == 0)
    assert(len(polytract_finder(test_4)) == 1)
    assert(len(polytract_finder(test_5)) == 0)
    assert(len(polytract_finder(test_6)) == 1)
    assert(len(polytract_finder(test_7)) == 2)
    assert(len(polytract_finder(test_8)) == 1)
    assert(len(polytract_finder(test_9)) == 1)
    print('Succesfull assert tests')
    seq = input('Enter your sequence: ')
    print(polytract_finder(seq))

