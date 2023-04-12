
# расклаываем исходную последовательность на фрагметы размером с длину повтора для каждого из фреймшифта
def fold (sequence:str, n_fold:int) ->list: 
    seq_split = []  #список для списков разбивки последовательностей с разынми фреймшифтами
    if n_fold >= 2 and n_fold <= (len(sequence) // 2):  # задаём ограничение длины повтора
        for item in range(n_fold): #цикл для создания фреймшифта, +1 чтобы проверять является ли элемент последним
            fold_seq = "" #последвоательность раная длине повтора 
            seq_frameshift = [] #cписок элементов последовательности равных длине повтора
            for nucleotide in sequence[item:]: # дробим последовательность для каждого из фреймшифтов
                fold_seq += nucleotide
                if len(fold_seq) == n_fold:
                    seq_frameshift.append(fold_seq)
                    fold_seq = '' #обнуляем для следующего фрагмента
            seq_split.append(seq_frameshift)
    else:
        raise ValueError("Недопустимая длина повтора")
    return seq_split 

def format_seq(raw_repeat, count):
    return f'Repeat #{count}:Number of repated elements: {raw_repeat["number_elements"]}, type: {raw_repeat["repeat_type"]}, start at {raw_repeat["first_nucleotide"]} nt, end at {raw_repeat["last_nucleotide"]}, frameshift: {raw_repeat["frameshift"]}'



def tandem_repeat(folded_seq: list) -> list: #находит тип повтора, начало и конец каждого повтора
    repeat_list = []
    for (frameshift_index, frameshift_list) in enumerate(folded_seq):
        repeat_lenght = 0
        print(frameshift_list, frameshift_list[-1])
        for index in range(1, len(frameshift_list)): 
            n_fold = len(frameshift_list[index])
            if frameshift_list[index] == frameshift_list[index - 1]:
                repeat_lenght += 1
            else:
                if repeat_lenght >= 1:
                    start_nucleotide = ((index - repeat_lenght - 1)*(n_fold)) + (frameshift_index + 1)                   
                    repeat_list.append({'repeat_start_element': index - repeat_lenght,
                                        'repeat_end_element': index,
                                        'number_elements' : repeat_lenght + 1,
                                        'element_length': n_fold,
                                        'repeat_type': frameshift_list[index -1],
                                        'frameshift': frameshift_index  + 1,
                                        'first_nucleotide': start_nucleotide, #абсолютная начальная позиция в исходной последовательности
                                        'last_nucleotide': start_nucleotide + (repeat_lenght+1)*n_fold - 1 #абсолютная конечная позиция в исходной последовательности
                                        })
                repeat_lenght = 0
        if repeat_lenght >=1: #если после цикла длина повтора != 0 значит последвоательность кончается на повтор
            repeat_list.append({'repeat_start_element': len(frameshift_list)- repeat_lenght,
                                            'repeat_end_element': len(frameshift_list),
                                            'number_elements' : repeat_lenght + 1,
                                            'element_length': n_fold,
                                            'repeat_type': frameshift_list[-1],
                                            'frameshift': frameshift_index + 1,
                                            'first_nucleotide': (start_nucleotide := (len(frameshift_list)- repeat_lenght - 1)*n_fold + (frameshift_index + 1)),
                                            'last_nucleotide': start_nucleotide + (repeat_lenght+1)*n_fold - 1,
                                            })

    repeat_list.sort(key=lambda item: item['first_nucleotide'])

#формируем список из не-вложеных повторов
    final_list = []
    if len(repeat_list) != 0:
        final_list.append(repeat_list[0])
        for index in range(1, len(repeat_list)):
            if repeat_list[index]['first_nucleotide'] > repeat_list[index - 1]['last_nucleotide']:
                final_list.append(repeat_list[index])


    return final_list
       

if __name__ == '__main__':
    seq = input('enter sequence') #принимаем последовательность от пользователя
    n_fold = int(input()) #принимаем длину повтора от пользователя которая будет использоваться для формирования фремшифтов
    
    fold_seq = fold(seq, n_fold)
    print(fold_seq)
    rep_lst = tandem_repeat(fold_seq)
    print(rep_lst)