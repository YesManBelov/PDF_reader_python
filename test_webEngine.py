import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, Qt
from forms.reader_webEngine import Ui_MainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView



class PDFReader(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.page_number = None
        self.pdf_images = None
        self.web = QWebEngineView(self.widget)
        self.btn_upload.clicked.connect(self.upload_file)

    def upload_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', "PDF Files (*.pdf);;All Files (*)")
        if file_name[0]:
            self.page_number = 0
            self.read_pdf(file_name[0])


    def read_pdf(self, file_name):
        self.web.resize(900, 500)
        self.web.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web.load(QUrl(f"file:///{file_name}"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFReader()
    window.show()
    sys.exit(app.exec_())
