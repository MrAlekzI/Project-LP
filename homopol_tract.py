
def polytract_finder(sequence: str) -> dict:
    tract_dict = {}
    tract_count = 0
    repeat_lenght = 0
    for index in range(1, len(sequence)): #не очень понимаю чем enumerate лучше range, почти такая же работа с индексами, к тому же не получается бртать со втрого элемента
        if sequence[index] == sequence[index - 1]:
            repeat_lenght += 1
        else:
            print(repeat_lenght)
            if repeat_lenght >= 4:
                tract_count += 1
                tract_dict[tract_count] = {'hpt_start': index - repeat_lenght,
                                           'hpt_end': index,
                                           'hpt_lenght' : repeat_lenght + 1,
                                           'hpt_type': sequence[index -1]}
            repeat_lenght = 0

#если после цикла ддлина повтора != 0 значит последвоательность кончается на повтор
    if repeat_lenght >=4: 
        tract_dict[tract_count+1] = {'hpt_start': len(sequence)- repeat_lenght,
                                        'hpt_end': len(sequence)+1,
                                        'hpt_lenght' : repeat_lenght + 1,
                                        'hpt_type': sequence[-1]}
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

