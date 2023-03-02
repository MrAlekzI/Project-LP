from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index(): #обрабатываем главную страницу
    title = "DNA feature finder"
    
    return render_template('index.html', page_title=title, querry_length = 777, remove_count=0)

if __name__ == '__main__':
    app.run(debug=True)