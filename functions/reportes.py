import os
import pandas as pd
import mysql.connector
from fpdf import FPDF
import mysql.connector
from flask import Flask, render_template, send_from_directory

#app = Flask(__name__)

def obtener_datos(Username):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="23200181",
        database="gestion_espacios"
    )
    query = f"SELECT nombre, apellido, correo, contra FROM Usuarios WHERE correo = '{Username}';"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def generar_pdf(Username):
    df = obtener_datos(Username)
    if not df.empty:
        pdf = PDF()
        pdf.add_page()
        header = ['Nombre', 'Apellido', 'Correo', 'Contraseña']                     #Encabezados
        datos = df.values.tolist()
        pdf.tabla_registro(header, datos)
        pdf.output(f'Reporte_registro.pdf')

class PDF(FPDF):
    def header(self):
        titulo_registro = 'REPORTE DE REGISTRO'
        self.set_font(family='Times', style='B', size=30)
        # Color de fondo (azul)
        self.set_fill_color(0, 0, 255)
        # Color de texto (Blanco)
        self.set_text_color(255, 255, 255)
        self.cell(w=0, h=15, txt=titulo_registro, border=0, align='C', ln=1, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(10)
        
    def tabla_registro(self, header, datos):
        self.set_font(family='Arial', style='B', size=12)
        ancho_columnas = [30, 60, 60, 40]                                        # Ajustar los anchos de columna
        
        #Encabezados de la tabla
        for i in range(len(header)):
            self.set_fill_color(255,255,0)
            self.cell(ancho_columnas[i], 7, header[i], 1, 0, 'C', fill=True)
        self.ln()
        
        #Escribir los datos de la tabla
        self.set_font(family='Arial', size=8)
        for fila in datos:
            for i in range(len(fila)):
                self.cell(ancho_columnas[i], 7, str(fila[i]), 1, 0, fill=False)
            self.ln()

generar_pdf('jose.pereda@unmsm.edu.pe')

"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargar/<Username>')
def descargar(Username):
    generar_pdf(Username)
    return send_from_directory('static/reportes', f'reporte_{Username}.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
"""