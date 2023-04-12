from flask import Flask, render_template, request, redirect, url_for, flash
from random import randint, choice
from homopol_tract import polytract_finder, format_homopol # поиск однобуквенных повторов
import gc_graphic as gc
from random_seq import random_seq
from verification_seq import InputDNA
import tandem_search as ts



app = Flask(__name__)

test_querry = { 'input_seq': None,
                'remove_count': -1,
                'random_seq':None,
                'is_random': 0,
                'tandem_list':None,
                'homopol_tract': None,
                'homopol_tract_number': 0,
                'gc_frame_length': 0, 
                'gc_content': None
                } #словарь для тестирования функций 

@app.route("/")
def index(): #обрабатываем главную страницу
    title = "DNA feature finder"
    return render_template('index.html', page_title=title, querry_length = '', remove_count = 0,
                            is_random=test_querry['is_random'], is_rna = 0, non_identified = 0 )
        

@app.route("/", methods=['POST'])
def input_seq(): #запрос последовательности из окна
    try:
        dna_query = InputDNA(request.form.get('dna_querry'))
        test_querry['input_seq'] = dna_query.formated_sequence #сохраняем в словарь
        return render_template('index.html', querry_length = dna_query.input_lenth, remove_count = dna_query.counter,
                                is_rna = dna_query.is_uracil, non_identified = dna_query.is_non_identified)
    except (TypeError, IndexError):
        return render_template('index.html', remove_count = dna_query.counter,  querry_length = '')


@app.route("/input_report", methods=['POST'])
def input_report(): #обрабатываем кнопку показа введенной последоваьельности после ввода и форматирования
    title = 'Input sequence after formating' 
    if test_querry['input_seq']:
        return f"{test_querry['input_seq']}"     
    else:
        return 'No DNA sequence input' #почему то не работает, хотя когда ничего не вводится там сотит пробел (ord=32) 


@app.route("/random_gen", methods=['POST'])
def input_random(): #симуляция рандомной генерации, далее нужно подключать модуль
    try:
        random_length = int(request.form.get('random_length'))
        if random_length > 10:
            test_output = random_seq(random_length)
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
    return render_template('repeats.html', tandem_found = '', tract_number = test_querry['homopol_tract_number'])


@app.route("/repeats", methods=['POST'])
def input_tandem(): #ввод длины повтора, его обработка и вывод
    try:
        tandem_length = int(request.form.get('tandem_length'))
        sequence_fold = ts.fold(test_querry['input_seq'], tandem_length)
        test_querry['tandem_list'] = ts.tandem_repeat(sequence_fold)
        return render_template('repeats.html', tandem_found = len(test_querry['tandem_list']))
    except (TypeError, IndexError, ValueError):
        return render_template('repeats.html', tandem_found = '')



@app. route("/tandem_report")
def tandem_report_page(): #заготовка странциы с описание найдленых повторов в упододавимой форме
    formated_repeats = []
    return render_template('tandem_report.html', repeats = formated_repeats)



@app.route("/tandem_report", methods=['POST'])
def tandem_report(): #обработка кнопки для показа найденых повторов (отчет уже готов когда произведен поиск
    if test_querry['tandem_list'] is not None and test_querry['tandem_list'] != []:
        formated_repeats = []
        for (count, repeat) in enumerate(test_querry['tandem_list']):
            formated_repeats.append(ts.format_seq(repeat, count+1))
        #return f"{test_querry['tandem_list']}" #пока примитивный вывод 
        return render_template('tandem_report.html', repeats=formated_repeats, homopol_tracts = test_querry['homopol_tract'])      
    else:
        return render_template('tandem_report.html', repeats=['No repeats found'], homopol_tracts = test_querry['homopol_tract'])   



@app. route("/poly_tract", methods=['POST'])
def poly_tract_finder(): #кнопка поиска поиск гомопимерных трактов
    #пока последовательнотсь будет браться из input как разнести последовательности из дургих источнико я пока не знаю
    test_querry['homopol_tract'] = polytract_finder(test_querry['input_seq'])
    test_querry['homopol_tract_number'] = len(test_querry['homopol_tract'])
    return redirect(url_for('repeat_page'))



@app. route("/poly_tract_report", methods=['POST'])
def poly_tract_report(): #кнопка показа найденых повторов
    if test_querry['homopol_tract'] is not None and test_querry['homopol_tract'] != {}:
        formated_tracts = format_homopol(test_querry['homopol_tract'])
        return render_template('tandem_report.html', homopol_tracts = formated_tracts)
    else:
        return render_template('tandem_report.html', homopol_tracts = ['No homopolymer tracts found'])


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
        min_content = gc.gc_search(test_querry['gc_content'],min) #словарь с минимальным контентом
        return f'Minimal GC is {min_content["gc_content"]:.2f} within region(s): {" ".join(min_content["frame"])} bp'
    else:
        return 'Please calculate content before'
   

@app.route('/gc_content_max', methods=['POST'])
def gc_max_report():  #ввод участков с минимальными GC
    if test_querry['gc_content'] is not None:
        max_content = gc.gc_search(test_querry['gc_content'], max) #словарь с максимальным контентом
        return f'Maximal GC is {max_content["gc_content"]:.2f} within region(s): {" ".join(max_content["frame"])} bp'
    else:
        return 'Please calculate content before'






if __name__ == '__main__':
    app.run(debug=True)
