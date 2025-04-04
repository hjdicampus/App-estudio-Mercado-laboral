import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
import psycopg2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Ofertas de Empleo")
        self.setGeometry(100, 100, 600, 400)

        # Conexión a la base de datos
        self.conn = psycopg2.connect(
            dbname="job_task_db",
            user="postgres",
            password="password",  # Cambia esto por tu contraseña real
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

        # Interfaz principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Formulario para añadir oferta
        self.title_input = QLineEdit(self)
        self.company_input = QLineEdit(self)
        self.location_input = QLineEdit(self)

        self.layout.addWidget(QLabel("Título"))
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(QLabel("Empresa"))
        self.layout.addWidget(self.company_input)
        self.layout.addWidget(QLabel("Ubicación"))
        self.layout.addWidget(self.location_input)

        # Botones de acción
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Añadir Oferta", self)
        self.add_button.clicked.connect(self.add_job)
        self.update_button = QPushButton("Actualizar Seleccionada", self)
        self.update_button.clicked.connect(self.update_job)
        self.delete_button = QPushButton("Eliminar Seleccionada", self)
        self.delete_button.clicked.connect(self.delete_job)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        self.layout.addLayout(button_layout)

        # Tabla para mostrar ofertas
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Título", "Empresa", "Ubicación"])
        self.table.itemSelectionChanged.connect(self.load_selected_job)
        self.layout.addWidget(self.table)

        self.central_widget.setLayout(self.layout)

        # Cargar datos iniciales
        self.load_jobs()

    def load_jobs(self):
        """Carga todas las ofertas de empleo en la tabla"""
        self.cursor.execute("SELECT id, title, company, location FROM job_market_joboffer")
        rows = self.cursor.fetchall()
        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def add_job(self):
        """Añade una nueva oferta a la base de datos"""
        title = self.title_input.text()
        company = self.company_input.text()
        location = self.location_input.text()
        try:
            self.cursor.execute(
                "INSERT INTO job_market_joboffer (title, company, location, publication_date, source_id) "
                "VALUES (%s, %s, %s, CURRENT_DATE, 1) RETURNING id",
                (title, company, location)
            )
            job_id = self.cursor.fetchone()[0]
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Oferta añadida correctamente.")
            self.load_jobs()
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo añadir la oferta: {str(e)}")

    def load_selected_job(self):
        """Carga los datos de la oferta seleccionada en los campos de entrada"""
        selected = self.table.selectedItems()
        if selected:
            row = self.table.currentRow()
            self.title_input.setText(self.table.item(row, 1).text())
            self.company_input.setText(self.table.item(row, 2).text())
            self.location_input.setText(self.table.item(row, 3).text())

    def update_job(self):
        """Actualiza la oferta seleccionada"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Selecciona una oferta para actualizar.")
            return
        row = self.table.currentRow()
        job_id = self.table.item(row, 0).text()
        title = self.title_input.text()
        company = self.company_input.text()
        location = self.location_input.text()
        try:
            self.cursor.execute(
                "UPDATE job_market_joboffer SET title = %s, company = %s, location = %s WHERE id = %s",
                (title, company, location, job_id)
            )
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Oferta actualizada correctamente.")
            self.load_jobs()
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar la oferta: {str(e)}")

    def delete_job(self):
        """Elimina la oferta seleccionada"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Selecciona una oferta para eliminar.")
            return
        row = self.table.currentRow()
        job_id = self.table.item(row, 0).text()
        reply = QMessageBox.question(self, "Confirmar", "¿Seguro que quieres eliminar esta oferta?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM job_market_joboffer WHERE id = %s", (job_id,))
                self.conn.commit()
                QMessageBox.information(self, "Éxito", "Oferta eliminada correctamente.")
                self.load_jobs()
                self.clear_inputs()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la oferta: {str(e)}")

    def clear_inputs(self):
        """Limpia los campos de entrada"""
        self.title_input.clear()
        self.company_input.clear()
        self.location_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())