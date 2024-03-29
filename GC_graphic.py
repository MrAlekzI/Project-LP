import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from random import choice
from configs import fig_path, gc_fig_clearance


def gc_content(seq: str) ->float: #подсчет контента
    g = seq.count('g')
    c = seq.count('c')
    return ((g + c) / len(seq)) * 100


def nucl_slicing(seq: str, frame: int) ->dict:
    plot_data = {}
    frame_count = 0
    for i in range(0, len(seq), frame):
        frame_count += 1 #чтобы реализовать поиск максимумов и минимумов делаем словарь
        seq_frame = seq[i:i+frame] #срез по последовательности
        if len(seq_frame) == frame:
            current_frame = (i+1, i+frame, gc_content(seq_frame)) #формируем кортеж где первый элемент - начало, второй - конец фрейма, третйи - GC состав
            plot_data[frame_count] = current_frame #список кортежей, где содержатся все фреймы
    return plot_data 


def gc_search(plot_data: dict, func) ->dict: #поиск фреймов с с применением выбраной функции (например max, min) gc%, тут по факту два поиска - до первого найденого, а потом вообще по всем, не заню насколько это плохо для алгоритма поиска
    result = {'gc_content': None, 'frame': []}
    func_frame = func(plot_data, key=lambda item: plot_data[item][2])
    func_value = plot_data[func_frame][2]
    result['gc_content'] = func_value #выставляем процент
    for frame in plot_data: #на случай если енсколько фреймов
        if plot_data[frame][2] == func_value:
            formated_frame = f'{plot_data[frame][0]} - {plot_data[frame][1]}'
            result['frame'].append(formated_frame)
    return result


def plot_axis(plot_data): #разбиваем по данные по осям
    data_x = []
    data_y = []
    for frame in plot_data.values():
        data_x.append(frame[0])
        data_x.append(frame[1])
        data_y.append(frame[2])
        data_y.append(frame[2])
    return data_x, data_y


def draw_gc_content(sequence, frame):
    current_plot = plot_axis(nucl_slicing(sequence, frame)) #формируем массив для осей
    fig, ax = plt.subplots() #подстомтрел в интернете, не понимаю зачем fig, но без него не работает
    plt.ylim(0, 100)
    ax.plot(current_plot[0], current_plot[1])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.set_xlabel('GC content, %', fontsize = 15)
    ax.set_ylabel('DNA positnion, bp', fontsize = 15)
    gc_fig_clearance()
    fig.savefig(os.path.join(fig_path, 'gc_fig.jpg'), dpi=150)
    

if __name__ == '__main__':
    length = int(input('Input randome DNA lenght'))
    chose_frame = int(input('Input frame of content calculation'))
    rand_seq = ''.join([choice('atgc') for _ in range(0, length)])
    draw_gc_content(rand_seq, chose_frame)






