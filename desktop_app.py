import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import Error

class JobOfferCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD de Ofertas de Empleo")
        self.conn = psycopg2.connect(
            dbname="task_manager_db",
            user="postgres",
            password="12345678",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

        # Campos de entrada
        tk.Label(root, text="Título").grid(row=0, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(root, text="Empresa").grid(row=1, column=0)
        self.company_entry = tk.Entry(root)
        self.company_entry.grid(row=1, column=1)

        tk.Label(root, text="URL").grid(row=2, column=0)
        self.url_entry = tk.Entry(root)
        self.url_entry.grid(row=2, column=1)

        # Botones
        tk.Button(root, text="Crear", command=self.create).grid(row=3, column=0)
        tk.Button(root, text="Leer", command=self.read).grid(row=3, column=1)
        tk.Button(root, text="Actualizar", command=self.update).grid(row=4, column=0)
        tk.Button(root, text="Eliminar", command=self.delete).grid(row=4, column=1)

        # Área de texto para resultados
        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.grid(row=5, column=0, columnspan=2)

    def create(self):
        try:
            query = """
                INSERT INTO job_market_joboffer (title, company, url, date_posted, source, location, salary)
                VALUES (%s, %s, %s, CURRENT_DATE, 'Manual', %s, %s)
            """
            self.cursor.execute(query, (
                self.title_entry.get(),
                self.company_entry.get(),
                self.url_entry.get(),
                None,  # location (opcional, puede ser NULL)
                None   # salary (opcional, puede ser NULL)
            ))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Oferta creada")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def read(self):
        self.result_text.delete(1.0, tk.END)
        self.cursor.execute("SELECT title, company, url FROM job_market_joboffer")
        rows = self.cursor.fetchall()
        for row in rows:
            self.result_text.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]}\n")

    def update(self):
        try:
            query = "UPDATE job_market_joboffer SET title = %s, company = %s WHERE url = %s"
            self.cursor.execute(query, (self.title_entry.get(), self.company_entry.get(), self.url_entry.get()))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Oferta actualizada")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def delete(self):
        try:
            query = "DELETE FROM job_market_joboffer WHERE url = %s"
            self.cursor.execute(query, (self.url_entry.get(),))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Oferta eliminada")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = JobOfferCRUD(root)
    root.mainloop()