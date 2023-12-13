import sys
import fitz

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from forms.reader_textBrowser import Ui_MainWindow


class PDFReader(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_upload.clicked.connect(self.upload_file)
        self.btn_next.clicked.connect(lambda: self.change_page_t(step=1))
        self.btn_back.clicked.connect(lambda: self.change_page_t(step=-1))

    def upload_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', "PDF Files (*.pdf);;All Files (*)")
        if file_name[0]:
            self.generate_pages(file_name[0])

    def generate_pages(self, file_name):
        self.pages = {}
        with fitz.open(file_name) as file:
            for page in range(file.page_count):
                print(file[page].get_text())
                self.pages[page] = file[page].get_text()

        self.page_number = 0
        self.read_pdf()

    def read_pdf(self):
        self.textBrowser.setPlainText(self.pages[self.page_number])
        self.label_page.setText(str(self.page_number + 1))

    def change_page_t(self, step):
        self.page_number += step
        if self.page_number < len(self.pages) and self.page_number >= 0:
            self.read_pdf()
        else:
            self.page_number -= step



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFReader()
    window.show()
    sys.exit(app.exec_())
