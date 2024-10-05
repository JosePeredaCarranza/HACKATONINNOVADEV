from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def index():
    return render_template('index.html')

@app.route('/aulas')
def index():
    return render_template('index.html')

@app.route('/laboratorios')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
