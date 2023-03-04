from flask import Flask, render_template, request, redirect, url_for, flash



app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index(): #обрабатываем главную страницу
    try:
        dna_querry = '' #чтобы страница не выдвала ошибку, почему то не видит если вынести в глобальные
        title = "DNA feature finder"
        if request.method == 'POST':   
            dna_querry = request.form.get('dna_querry') 
            dna_querry_lengh=len(dna_querry) 
            return render_template('index.html', page_title=title, querry_length = dna_querry_lengh, remove_count=0,)
    except TypeError: #пока последовательность не введена почему то dna_qurry ==None
        return render_template('index.html', page_title=title, querry_length = '', remove_count=0,)
         

if __name__ == '__main__':
    app.run(debug=True)
