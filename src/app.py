#Librerias o frameworks que se utiliza

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
import smtplib, re, os, pandas as pd
from config import config

#Models

from models.ModelUser import ModelUser
from models.ModelSpreadsheets import ModelSpreadsheets

#Entities
from models.entities.User import User
from models.entities.PDF import PDF


app=Flask(__name__)

db=MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


#Ruta principal (redirije al login) ---------------------------------------------------------------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

#Ruta Login ---------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = User(0, "", "", request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.contra:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Ta mal la contraseña...")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    
#Ruta Logout ------------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#Ruta home (Pantalla principal) -------------------------------------------------------------------------------------
@app.route('/home')
@login_required
def home():
    return render_template('home/home.html')

#Ruta aulas (Pantalla con la información de las aulas) --------------------------------------------------------------
@app.route('/aulas')
@login_required
def aulas():
    return render_template('aulas/aulas.html')

#Ruta Register -------------------------------------------------------------------------------------------------------
@app.route('/register')
@login_required
def register():
    return render_template('register/register.html')

#Ruta Register single (individual) ------------------------------------------------------------------------------------
@app.route('/register/single', methods=['GET','POST'])
@login_required
def registerSingle():
    if request.method == "POST":
        if request.form['username'] and request.form['codigo'] and request.form['dni'] and request.form['names'] and request.form['lastnames'] and request.form['rol']:
            user = User(0, request.form['codigo'], request.form['dni'], request.form['username'], " ", request.form['names'], request.form['lastnames'], request.form['rol'])
            validacion_campos= verificar_campos(request.form['username'], request.form['codigo'], request.form['dni'], request.form['rol'], request.form['names'], request.form['lastnames'],)
            if validacion_campos == True:
                register_user = ModelUser.register(db, user)
                if register_user!=None:
                    pdf=generar_pdf(user)
                    send_email("Bienvenido", user.correo,  f"""Hola {user.nombre}, se te acaba de adjuntar un pdf con tus nuevos datos.
                               - La contraseña de este documento encriptado es su DNI""", pdf)
                    flash(f"Registro exitoso, se ha enviado un correo a {user.correo}")

                    flash(f"Registro exitoso {user.contra}")
                    eliminar_archivo(pdf)
                    return render_template('register/register_single.html')
                else:
                    flash("Registro fallido")
                    return render_template('register/register_single.html')
            else:
                flash(validacion_campos)
                return render_template('register/register_single.html')
    else:
        return render_template('register/register_single.html')

#Ruta Register plural (archivo) --------------------------------------------------------------------------------------------
@app.route('/register/plural', methods=['GET','POST'])
@login_required
def registerPlural():
    if request.method == "POST":
        if 'csvFile' in request.files and request.files['csvFile'].filename != '':
            file = request.files['csvFile']
            filename=secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(file_path)
                flash(f"Archivo {filename} guardado exitosamente.")
            except Exception as error:
                flash(f"Error al guardar el archivo: {str(error)}")
                return render_template('register/register_plural.html')
            
            if filename.endswith('.csv'):
                registrar_usuarios_desde_archivo(file_path, 'csv')
                eliminar_archivo(file_path)
                return render_template('register/register_plural.html')
            elif filename.endswith('.xlsx'):
                registrar_usuarios_desde_archivo(file_path, 'excel')
                eliminar_archivo(file_path)
                return render_template('register/register_plural.html')
            else:
                eliminar_archivo(file_path)
                flash('Por favor, sube un archivo con formato .csv o .xlsx')
                return render_template('register/register_plural.html')
        else:
                flash('No se ha subido ningún archivo')
                return render_template('register/register_plural.html')
    else:
        return render_template('register/register_plural.html')

#Ruta Reset password (pedido) --------------------------------------------------------------------------------------------
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = ModelUser.get_by_mail(db,email)
        if user != None:
            token = user.generate_token(user.correo)
            reset_url = url_for('reset_password', token=token, _external=True)
            send_email('Restablecimiento de contraseña',user.correo,
                       f'Sigue el enlace para restablecer tu contraseña: {reset_url}')
            flash('Te hemos enviado un correo con las instrucciones para restablecer tu contraseña.')
            return render_template('reset_password/reset_password_request.html')
        else:
            flash('No existe ninguna cuenta con ese correo electrónico.')
        return render_template('reset_password/reset_password_request.html')
    return render_template('reset_password/reset_password_request.html')

#Ruta Register password (cambio) --------------------------------------------------------------------------------------------
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = User.verify_token(token)
    if not email:
        flash('El enlace de restablecimiento es inválido o ha expirado.')
        return redirect(url_for('reset_password_request'))

    if request.method == 'POST':
        password = request.form['password']
        password_1 = request.form['password_1']
        patron= r"^[a-zA-Z0-9]{9,}$"
        result=re.match(patron, password)
        result_1=re.match(patron, password_1)
        user = ModelUser.get_by_mail(db,email)
        if user != None:
            if result and result_1:
                if password == password_1:
                    if ModelUser.change_password(db,user,password) != None:
                        send_email("Cambio de contraseña exitoso", user.correo, f"Hola {user.nombre}, tu contraseña ha sido actualizada correctamente")
                        flash('Tu contraseña ha sido actualizada correctamente.')
                        return redirect(url_for('login'))
                else:
                    flash('Las contraseñas no son iguales.')
                    return render_template('reset_password/reset_password.html')
            else:
                flash('La nueva contraseña debe tener 9 dígitos como mínimo y estar compuesta de solo letras y números.')
                return render_template('reset_password/reset_password.html')
        else:
            flash('No se encontró ningún usuario con ese correo electrónico.')
            return redirect(url_for('reset_password_request'))
    return render_template('reset_password/reset_password.html')

#Funcion Enviar Correo (gmail) --------------------------------------------------------------------------------------------
def send_email(asunto, correo, mensaje, pdf = None):
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login("osoriodeprueba@gmail.com", "zbfp wokl xtxg haru")

        msg = MIMEMultipart()
        msg["From"] = "osoriodeprueba@gmail.com"
        msg["To"] = correo
        msg["Subject"] = asunto

        msg.attach(MIMEText(mensaje, 'plain'))

        if pdf:
            with open(pdf, 'rb') as adjunto:
                parte = MIMEBase('application', 'octet-stream')
                parte.set_payload(adjunto.read())
                encoders.encode_base64(parte)
                parte.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf)}')
                msg.attach(parte)

        servidor.sendmail("osoriodeprueba@gmail.com", correo, msg.as_string())
    except Exception as e:
        return f"Hubo un error al enviar el correo: {str(e)}"
    finally:
        servidor.quit()
    return "Correo enviado"

#Funcion Verificar campos -------------------------------------------------------------------------------------------------------------
def verificar_campos(correo, codigo, dni, rol, nombres, apellidos):
    campos_vacios = []
    patron= r"^[a-zA-Z]{4,12}\.[a-zA-Z]{4,12}@unmsm\.edu\.pe$"
    result=re.match(patron, correo)
    if not result:
        campos_vacios.append('correo institucional')
    if not str(codigo).strip():
        campos_vacios.append('codigo')
    if not str(dni).strip():
        campos_vacios.append('dni')
    if not nombres.strip():
        campos_vacios.append('nombre')
    if not apellidos.strip():
        campos_vacios.append('apellidos')
    if rol not in ("Estudiante" ,"Profesor" , "Administrador"):
        campos_vacios.append('rol')
    if campos_vacios:
        return f'Los siguientes campos son requeridos: {", ".join(campos_vacios)}'
    else:
        return True

#Funcion Leer archivos y registar (csv o xlsx) --------------------------------------------------------------------------------------------
def registrar_usuarios_desde_archivo(file_path, file_type):
    if file_type == 'csv':
        data = pd.read_csv(file_path)
    elif file_type == 'excel':
        data = pd.read_excel(file_path)
    if ModelSpreadsheets.checkFormat(data):
        filas = ModelSpreadsheets.countRows(data)
        usuarios_registrados = 0

        for i in range(filas):

            validacion_campos_tabla = verificar_campos(data.iloc[i, 2], data.iloc[i, 0],data.iloc[i, 1],data.iloc[i, 5], data.iloc[i, 3], data.iloc[i, 4])

            if validacion_campos_tabla == True:

                user_tabla = User(0, data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2], " ", data.iloc[i, 3], data.iloc[i, 4], data.iloc[i, 5])
                register_user_tabla = ModelUser.register(db, user_tabla)
                if register_user_tabla:
                    pdf=generar_pdf(user_tabla)
                    send_email("Bienvenido", user_tabla.correo, f"""Hola {user_tabla.nombre}, se te acaba de adjuntar un pdf con tus nuevos datos.
                               - La contraseña de este documento encriptado es su DNI""", pdf)
                    eliminar_archivo(pdf)
                    usuarios_registrados += 1
                else:
                    flash(f"Registro fallido para el usuario en la fila {i+2}")
            else:
                flash(f"Error en la validación de la fila {i+2}. Motivo: {validacion_campos_tabla}")

        flash(f'{usuarios_registrados} usuarios registrados exitosamente desde el archivo {file_type.upper()}.')
    else:
        flash("El formato no cuenta con los campos correctos")

#Funcion generar pdf ----------------------------------------------------------------------------------------------------
def generar_pdf(user):
        pdf = PDF()
        pdf.add_page()
        header = ['Código', 'DNI','Nombres', 'Apellidos', 'Correo', 'Contraseña']
        datos = [[user.codigo, user.dni, user.nombre, user.apellido, user.correo, user.contra]]
        pdf.tabla_registro(header, datos)
        nombre_pdf = f'Reporte_registro_{user.nombre}.pdf'
        pdf.output(nombre_pdf)
        # Añadir contraseña con PyPDF2
        reader = PdfReader(nombre_pdf)
        writer = PdfWriter()

        # Copiar páginas del lector al escritor
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Establecer una contraseña
        password = user.dni
        writer.encrypt(password)

        # Guardar el PDF protegido
        nombre_pdf_protegido = f'Reporte_registro_protegido_{user.nombre}.pdf'
        with open(nombre_pdf_protegido, "wb") as output_pdf:
            writer.write(output_pdf)

        if os.path.exists(nombre_pdf):
            os.remove(nombre_pdf)

        return nombre_pdf_protegido

#Funcion eliminar archivos --------------------------------------------------------------------------------------------
def eliminar_archivo(nombre):
    if os.path.exists(nombre):
        os.remove(nombre)

#Funcion para el error 401 (Not login) ---------------------------------------------------------------------------------
def status_401(error):
    return redirect(url_for('login'))

#Funcion para el error 404 (Página no econtrada) ------------------------------------------------------------------------
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

#Main -------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run(debug= True, port= 5000)