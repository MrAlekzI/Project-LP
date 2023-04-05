
from flask import Flask, render_template, request, redirect, url_for, flash
from random import randint, choice
from homopol_tract import polytract_finder # поиск однобуквенных повторов
import gc_graphic as gc


app = Flask(__name__)

test_querry = { 'input_seq': None,
                'remove_count': -1,
                'random_seq':None,
                'is_random': 0,
                'tandem_test':0,
                'redirect_test':None,
                'homopol_tract': None,
                'homopol_tract_number': 0,
                'gc_frame_length': 0, 
                'gc_content': None
                } #словарь для тестирования функций 

@app.route("/")
def index(): #обрабатываем главную страницу
    title = "DNA feature finder"
    return render_template('index.html', page_title=title, querry_length = '', remove_count = test_querry['remove_count'], is_random=test_querry['is_random'] )
        

@app.route("/", methods=['POST'])
def input_seq(): #запрос последовательности из окна
    try:
        dna_query = request.form.get('dna_querry')
        test_querry['input_seq'] = dna_query #здесь будет применена функция форматирования, запись в словарь
        dna_query_lengh = len(test_querry['input_seq'])
        return render_template('index.html', querry_length = dna_query_lengh, remove_count = test_querry['remove_count'])
    except (TypeError, IndexError):
        return render_template('index.html', remove_count = test_querry['remove_count'],  querry_length = '')

@app.route("/input_report", methods=['POST'])
def input_report(): #обрабатываем кнопку показа введенной последоваьельности после ввода и форматирования
    title = 'Input sequence after formating' 
    if (test_querry['input_seq'] is not None) or (test_querry['input_seq'] != ' ') or (test_querry['input_seq'] != '') or (ord(test_querry['input_seq']) != 32): #условие как-то не арботает почему-то
    #все арвно почему то не хочет считвать пустой символ, надеюсь привязка функции форматирования поможет
        return f"{test_querry['input_seq']}"     
    else:
        return 'No DNA sequence input' #почему то не работает, хотя когда ничего не вводится там сотит пробел (ord=32) 

@app.route("/random_gen", methods=['POST'])
def input_random(): #симуляция рандомной генерации, далее нужно подключать модуль
    try:
        random_length = int(request.form.get('random_length'))
        if random_length > 0:
            test_output = ''.join([choice('atgc') for nucleotide in range(random_length)])
            test_querry['random_seq'] = test_output #запись в словарь
            test_querry['is_random']  = 1 #для вывода сообщения что прошла генерация
            return redirect(url_for('index'))
        else: 
            test_querry['is_random']  = 0 #убираем сообщение о генерации когда 0
            return redirect(url_for('index'))
    except (TypeError, IndexError, ValueError):
        test_querry['is_random']  = 0 #убираем сообщение о генерации если кликнули с пустым полем
        return redirect(url_for('index'))

@app.route("/random_report", methods=['POST'])
def random_report(): #обработки кнопки что за последоватльность сгенерировалася
    if test_querry['random_seq'] is not None:           
            return f"{test_querry['random_seq']}"       
    else:
        return 'No DNA generated'    


@app.route("/repeats")
def repeat_page(): #страница работы с повторами
    return render_template('repeats.html', tandem_found = test_querry['tandem_test'], tract_number = test_querry['homopol_tract_number'])

@app.route("/repeats", methods=['POST'])
def input_tandem(): #ввод длины повтора, его обработка и вывод
    try:
        tandem_length = request.form.get('tandem_length')
        test_querry['tandem_test'] = int(tandem_length)*10 #переменная для тестирвоания кнопки
        return render_template('repeats.html', tandem_found = test_querry['tandem_test'])
    except (TypeError, IndexError, ValueError):
        return render_template('repeats.html', tandem_found = '')

'''   
@app. route("/tandem_report")
def tandem_report_page(): #заготовка странциы с описание найдленых повторов в упододавимой форме
    return redirect(url_for('repeats')) 
'''

@app.route("/tandem_report", methods=['POST'])
def tandem_report(): #обработка кнопки для показа найденых повторов (отчет уже готов когда произведен поиск
    if test_querry['tandem_test'] > 0:
            test_querry['redirect_test'] = test_querry['tandem_test']*10 #тестовый вывод обработки
            return f"{test_querry['redirect_test']}" #пока примитивный вывод       
    else:
        return 'No repeats found'
    
@app. route("/poly_tract", methods=['POST'])
def poly_tract_finder(): #кнопка поиска поиск гомопимерных трактов
    #пока последовательнотсь будет браться из input как разнести последовательности из дургих источнико я пока не знаю
    test_querry['homopol_tract'] = polytract_finder(test_querry['input_seq'])
    test_querry['homopol_tract_number'] = len(test_querry['homopol_tract'])
    return redirect(url_for('repeat_page'))


'''
@app. route("/poly_tract_report")
def poly_tract_report_page(): #заготовка странциы с описание найдленых гомополимероных участков в упододавимой форме
    return render_template('homopolymer_report.html', page_title=title)
'''

@app. route("/poly_tract_report", methods=['POST'])
def poly_tract_report(): #кнопка показа найденых повторов
    if test_querry['homopol_tract'] is not None and test_querry['homopol_tract'] != {}:
        #вызопв тип тракта
            return f'{test_querry["homopol_tract"]}'
    else:
        return f'No homopolymer tracts'
    
@app.route('/gc_content')
def gc_content(): 
    return render_template('gc_content.html',  total_GC_content = '')

@app.route('/gc_content', methods=['POST'])
def input_frame_gc():  #ввод длины окна поиска
    try:
        frame_length = int(request.form.get('frame_length'))
        test_querry['gc_frame_length'] = frame_length
        test_querry['gc_content'] = gc.nucl_slicing(test_querry['input_seq'], frame_length) #записываем конетнт в словарь чтобы потом работаьь в min и max
        total_gc = gc.gc_content(test_querry['input_seq'])
        figure = gc.draw_gc_content(test_querry['input_seq'], frame_length)
        return render_template('gc_content.html', total_GC_content=total_gc)
    except (TypeError, IndexError, ValueError):
        return render_template('gc_content.html', total_GC_content = '')
       
@app.route('/gc_content_min', methods=['POST'])
def gc_min_report():  #ввод участков с минимальными GC
    if test_querry['gc_content'] is not None:
        min_content = gc.min_gc_search(test_querry['gc_content']) #словарь с минимальным контентом
        return f'Minimal GC is {min_content["gc_content"]:.2f} within region(s): {" ".join(min_content["frame"])} bp'
    else:
        return 'Please calculate content before'
   
@app.route('/gc_content_max', methods=['POST'])
def gc_max_report():  #ввод участков с минимальными GC
    if test_querry['gc_content'] is not None:
        max_content = gc.max_gc_search(test_querry['gc_content']) #словарь с максимальным контентом
        return f'Minimal GC is {max_content["gc_content"]:.2f} within region(s): {" ".join(max_content["frame"])} bp'
    else:
        return 'Please calculate content before'






if __name__ == '__main__':
    app.run(debug=True)
