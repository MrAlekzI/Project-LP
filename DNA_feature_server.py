
from flask import Flask, render_template, request, redirect, url_for, flash
from random import randint, choice


app = Flask(__name__)

test_querry = { 'input_seq': None,
                'remove_count': -1,
                'random_seq':None,
                'is_random': 0,
                'tandem_test':0,
                'redirect_test':None,
                'homopol_tract': 0, 
                'homopol_tract_type': None} #словарь для тестирования функций 

@app.route("/")
def index(): #обрабатываем главную страницу
    title = "DNA feature finder"
    return render_template('index.html', page_title=title, querry_length = '', remove_count = test_querry['remove_count'], is_random=test_querry['is_random'] )
        

@app.route("/", methods=['POST'])
def input_seq(): #запрос последовательности из окна
    try:
        title = "DNA feature finder"
        dna_query = request.form.get('dna_querry')
        test_querry['input_seq'] = dna_query #здесь будет применена функция форматирования, запись в словарь
        dna_query_lengh = len(test_querry['input_seq'])
        return render_template('index.html',page_title=title, querry_length = dna_query_lengh, remove_count = test_querry['remove_count'])
    except (TypeError, IndexError):
        return render_template('index.html', page_title=title, remove_count = test_querry['remove_count'],  querry_length = '')

@app.route("/input_report", methods=['POST'])
def input_report(): #обрабатываем кнопку показа введенной последоваьельности после ввода и форматирования
    title = 'Input sequence after formating'
    activate = int(request.form.get('import_report_hidden') )
    if activate == 1: 
        if test_querry['input_seq'] != None or test_querry['input_seq'] != ' ': #условие как-то не арботает почему-то
            return f"{test_querry['input_seq']}"     
        else:
            return 'No DNA sequence input' #почему то не работает, хотя когда ничего не вводится там сотит пробел (ord=32) 

@app.route("/random_gen", methods=['POST'])
def input_random(): #симуляция рандомной генерации, далее нужно подключать модуль
    try:
        title = "DNA feature finder"
        random_length = int(request.form.get('random_length'))
        if random_length > 0:
            test_output = ''.join(map(str, [choice('atgc') for nucleotide in range(random_length)]))
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
    title = 'Random DNA sequence'
    if test_querry['random_seq'] != None:
        activate = int(request.form.get('random_report_hidden') )
        if activate == 1:            
            return f"{test_querry['random_seq']}"       
    else:
        return 'No DNA generated'    


@app.route("/repeats")
def repeat_page(): #страница работы с повторами
    title = 'Repeats and content'
    return render_template('repeats.html', page_title=title, tandem_found = test_querry['tandem_test'], tract_number = test_querry['homopol_tract'])

@app.route("/repeats", methods=['POST'])
def input_tandem(): #ввод длины повтора, его обработка и вывод
    try:
        title = 'Repeats and content'
        tandem_length = request.form.get('tandem_length')
        tandem_lengh_test = int(tandem_length)*10 #переменная для тестирвоания кнопки
        test_querry['tandem_test'] = tandem_lengh_test #для тестирования вывода
        return render_template('repeats.html', page_title=title, tandem_found = test_querry['tandem_test'])
    except (TypeError, IndexError, ValueError):
        return render_template('repeats.html', page_title=title, tandem_found = '')

'''   
@app. route("/tandem_report")
def tandem_report_page(): #заготовка странциы с описание найдленых повторов в упододавимой форме
    title = 'Found tandem repeats'
    return redirect(url_for('repeats')) 
'''

@app.route("/tandem_report", methods=['POST'])
def tandem_report(): #обработка кнопки для показа найденых повторов (отчет уже готов когда произведен поиск)
    title = 'Repeats and content'
    if test_querry['tandem_test'] > 0:
        activate = int(request.form.get('report_hidden') )
        if activate == 1:  
            test_querry['redirect_test'] = test_querry['tandem_test']*10 #тестовый вывод обработки
            return f"{test_querry['redirect_test']}" #пока примитивный вывод       
    else:
        return 'No repeats found'
    
@app. route("/poly_tract", methods=['POST'])
def poly_tract_finder(): #кнопка поиска поиск гомопимерных трактов
    title = 'Repeats and content'
    activate = int(request.form.get('poly_tract_hidden') )
    if activate == 1:
    #взятие значения из словаря симулирует вызов модуля по поиску гомоповторов и создание записи в том же словаре симулирует формирование рпорта
        test_querry['homopol_tract'] = randint(0, 5)
        if  test_querry['homopol_tract']:
           test_querry['homopol_tract_type'] = choice('atgc') 

        return redirect(url_for('repeat_page'))

'''
@app. route("/poly_tract_report")
def poly_tract_report_page(): #заготовка странциы с описание найдленых гомополимероных участков в упододавимой форме
    title = 'Homopolymer tracts
    return render_template('homopolymer_report.html', title=title)
'''

@app. route("/poly_tract_report", methods=['POST'])
def poly_tract_report(): #кнопка поиска поиск гомопимерных трактов
    title = 'Homopolymer tracts'
    activate = int(request.form.get('poly_tract_report_hidden'))
    if test_querry['homopol_tract'] > 0:
        if activate == 1:
        #вызоп вызов тип тракта
            return f'Type of homopolymer: {test_querry["homopol_tract_type"]}'
    else:
        return f'No homopolymer tracts'





if __name__ == '__main__':
    app.run(debug=True)
