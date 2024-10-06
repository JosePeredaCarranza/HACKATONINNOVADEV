from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        titulo_registro = 'REPORTE DE REGISTRO'
        self.set_font(family='Times', style='B', size=30)
        self.set_fill_color(0, 0, 255)
        self.set_text_color(255, 255, 255)
        self.cell(w=0, h=15, txt=titulo_registro, border=0, align='C', ln=1, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(10)


    def tabla_registro(self, header, datos):
        self.set_font(family='Arial', style='B', size=12)
        ancho_columnas = [20, 20, 35, 35, 45, 30]

        if len(header) != len(ancho_columnas):
            raise ValueError("El número de encabezados no coincide con el número de columnas.")

        for i in range(len(header)):
            self.set_fill_color(255,255,0)
            self.cell(ancho_columnas[i], 7, header[i], 1, 0, 'C', fill=True)
        self.ln()

        self.set_font(family='Arial', size=8)
        for fila in datos:
            for i in range(len(fila)):
                self.cell(ancho_columnas[i], 7, str(fila[i]), 1, 0, 'C', fill=False)
            self.ln()