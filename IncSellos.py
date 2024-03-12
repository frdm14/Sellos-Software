import io
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import filedialog, messagebox
from decimal import Decimal

def agregar_imagen_a_pdf(pdf_path, imagen1_path, imagen2_path, pdf_salida_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()

        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)

            # Calcular el ancho y alto de la página actual en puntos
            page_width, page_height = map(Decimal, page.mediaBox.upperRight)

            # Imagen 1 un poco más abajo
            image1_width = Decimal(125)  # Ancho de la primera imagen
            image1_height = Decimal(175)  # Alto de la primera imagen
            x_coordinate1 = (page_width - image1_width) * Decimal(0.9)
            y_coordinate1 = Decimal(page_height) - image1_height - Decimal(35)  # Ajusta este valor para cambiar la posición vertical

            packet1 = io.BytesIO()
            can1 = canvas.Canvas(packet1, pagesize=(page_width, page_height))
            can1.drawImage(imagen1_path, float(x_coordinate1), float(y_coordinate1), width=float(image1_width),
                            height=float(image1_height))
            can1.save()
            packet1.seek(0)
            new_pdf1 = PyPDF2.PdfFileReader(packet1)
            page.mergePage(new_pdf1.getPage(0))

            # Imagen 2 al final del texto centrada
            image2_width = Decimal(100)  # Ancho de la segunda imagen
            image2_height = Decimal(75)  # Alto de la segunda imagen
            x_coordinate2 = (page_width - image2_width) / Decimal(2)  # Centrado horizontalmente
            y_coordinate2 = Decimal(90)

            packet2 = io.BytesIO()
            can2 = canvas.Canvas(packet2, pagesize=(page_width, page_height))
            can2.drawImage(imagen2_path, float(x_coordinate2), float(y_coordinate2), width=float(image2_width),
                            height=float(image2_height))
            can2.save()
            packet2.seek(0)
            new_pdf2 = PyPDF2.PdfFileReader(packet2)
            page.mergePage(new_pdf2.getPage(0))

            pdf_writer.addPage(page)

        with open(pdf_salida_path, 'wb') as pdf_output:
            pdf_writer.write(pdf_output)

        messagebox.showinfo("Operación Completada",
                            f"Sello agregado y mensaje guardado en {pdf_salida_path} exitosamente.")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Agregar Sello")

        # Etiqueta del título
        self.label_titulo = tk.Label(root, text="Programa para Agregar Sello a PDF", font=("Helvetica", 16, "bold"))
        self.label_titulo.pack(pady=10)  # Añadir espacio arriba y abajo

        # Etiquetas
        self.label_pdf = tk.Label(root, text="Seleccionar archivo PDF:")
        self.label_pdf.pack()

        self.label_imagen1 = tk.Label(root, text="Seleccionar imagen 1:")
        self.label_imagen1.pack()

        self.label_imagen2 = tk.Label(root, text="Seleccionar imagen 2:")
        self.label_imagen2.pack()

        # Botones para seleccionar archivos
        self.btn_pdf = tk.Button(root, text="Seleccionar PDF", command=self.seleccionar_pdf)
        self.btn_pdf.pack(pady=5)  # Añadir espacio debajo del botón

        self.btn_imagen1 = tk.Button(root, text="Seleccionar Imagen 1", command=self.seleccionar_imagen1)
        self.btn_imagen1.pack(pady=5)

        self.btn_imagen2 = tk.Button(root, text="Seleccionar Imagen 2", command=self.seleccionar_imagen2)
        self.btn_imagen2.pack(pady=5)

        # Botón para ejecutar la operación
        self.btn_agregar = tk.Button(root, text="Agregar Sello", command=self.agregar_imagen_al_pdf)
        self.btn_agregar.pack(pady=10)

    def seleccionar_pdf(self):
        self.ruta_pdf = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        self.label_pdf.config(text=f"Seleccionar archivo PDF: {self.ruta_pdf}")

    def seleccionar_imagen1(self):
        self.ruta_imagen1 = filedialog.askopenfilename(filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg")])
        self.label_imagen1.config(text=f"Seleccionar imagen 1: {self.ruta_imagen1}")

    def seleccionar_imagen2(self):
        self.ruta_imagen2 = filedialog.askopenfilename(filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg")])
        self.label_imagen2.config(text=f"Seleccionar imagen 2: {self.ruta_imagen2}")

    def agregar_imagen_al_pdf(self):
        try:
            ruta_salida = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
            if ruta_salida:
                agregar_imagen_a_pdf(self.ruta_pdf, self.ruta_imagen1, self.ruta_imagen2, ruta_salida)
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()