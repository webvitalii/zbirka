from PySide6.QtWidgets import QWidget, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QFileDialog
import csv
import os

class CsvPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file_path = None

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.csv_file_path_input = QLineEdit()
        self.csv_file_path_input.setPlaceholderText("Enter CSV file path")
        self.layout.addWidget(self.csv_file_path_input)

        self.select_csv_file_btn = QPushButton("Select CSV file")
        self.select_csv_file_btn.clicked.connect(self.select_csv_file)
        self.layout.addWidget(self.select_csv_file_btn)
        
        self.csv_fields_input = QLineEdit()
        self.csv_fields_input.setPlaceholderText("Enter CSV fields to export in new file")
        self.layout.addWidget(self.csv_fields_input)
        
        self.create_csv_file_btn = QPushButton("Create new CSV file")
        self.create_csv_file_btn.clicked.connect(self.create_new_csv_file)
        self.layout.addWidget(self.create_csv_file_btn)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)
        
        
    def select_csv_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV files (*.csv)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                file_path = file_paths[0]
                self.selected_file_path = file_path
                self.csv_file_path_input.setText(self.selected_file_path)
                # Paste list of fields from csv file into the csv_fields_input
                with open(file_path, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    self.csv_fields_input.setText(','.join(next(reader)))

    def create_new_csv_file(self):
        if hasattr(self, 'selected_file_path'):
            selected_fields = self.csv_fields_input.text()
            if selected_fields:
                selected_fields = selected_fields.split(',')
                with open(self.selected_file_path, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    fieldnames = reader.fieldnames
                    filtered_fieldnames = [field for field in fieldnames if field.strip() in selected_fields]
                    new_file_path = os.path.join(os.path.dirname(self.selected_file_path), 'updated.csv')
                    with open(new_file_path, 'w', newline='') as new_csvfile:
                        writer = csv.DictWriter(new_csvfile, fieldnames=filtered_fieldnames)
                        writer.writeheader()
                        for row in reader:
                            filtered_row = {key: row[key] for key in filtered_fieldnames}
                            writer.writerow(filtered_row)
                    self.output_text.append("New CSV file created successfully.")
                    # Rename the new file to updated.csv
                    os.rename(new_file_path, os.path.join(os.path.dirname(self.selected_file_path), 'updated.csv'))
            else:
                self.output_text.append("Cancelled saving new CSV file.")
        else:
            self.output_text.append("Please enter CSV fields to export.")

