from flask import Flask, render_template, request, redirect, url_for, flash



app = Flask(__name__)


@app.route("/get_querry")
def index(): #обрабатываем главную страницу
    title = "DNA feature finder"
    return render_template('index.html', page_title=title, querry_length = '', remove_count = -1)
    
         
@app.route("/get_querry", methods=['POST'])
def input_seq():
    try:
        title = "DNA feature finder"
        dna_query = request.form.get('dna_querry')
        dna_query_lengh = len(dna_query)
        return render_template('index.html',page_title=title, querry_length = dna_query_lengh, remove_count = -1)
    except (TypeError, IndexError):
        return render_template('index.html', page_title=title, querry_length = '')


if __name__ == '__main__':
    app.run(debug=True)
