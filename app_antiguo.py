from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'miguel123456'
app.config['MYSQL_DB'] = 'gestion_espacios'

conexion = MySQL(app)

@app.route('/')
def index():
    data={
        'titulo': 'Fue ',
        'contenido': 'Holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    }
    return render_template('login.html', data = data)

@app.route('/cursos')
def listar_nombres():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql = "SELECT nombre FROM gestion_espacios.usuarios ORDER BY nombre DESC"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        print(cursos)
        data['mensaje'] = 'Exito'
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug= True, port= 5000)