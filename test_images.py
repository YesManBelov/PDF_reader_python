# import sys
# import fitz
#
# from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel
# from PyQt5.QtGui import QPixmap, QImage, QPen, QPainter
# from PyQt5.QtCore import QUrl, Qt, QRect
# from forms.reader_images import Ui_MainWindow
# from PIL import Image
#
# from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel
# from PyQt5.QtGui import QPixmap, QImage, QPen, QPainter
# from PyQt5.QtCore import QUrl, Qt, QRect
# from forms.reader_images import Ui_MainWindow
# from PIL import Image
#
#
# class CustomLabel(QLabel):
#     def __init__(self, parent=None):
#         super(CustomLabel, self).__init__(parent)
#         self.start_point = None
#         self.end_point = None
#         self.rectangle = None
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.start_point = event.pos()
#             self.end_point = event.pos()
#
#     def mouseMoveEvent(self, event):
#         if event.buttons() == Qt.LeftButton:
#             self.end_point = event.pos()
#             self.update()
#
#     def paintEvent(self, event):
#         super(CustomLabel, self).paintEvent(event)
#         painter = QPainter(self)
#         pen = QPen(Qt.red)
#         pen.setWidth(2)
#         painter.setPen(pen)
#
#         if self.start_point and self.end_point:
#             self.rectangle = QRect(self.start_point, self.end_point).normalized()
#             painter.drawRect(self.rectangle)
#
#     def clear_rectangle(self):
#         self.start_point = None
#         self.end_point = None
#         self.rectangle = None
#         self.update()
#
#
# class PDFReader(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.page_number = None
#         self.pdf_images = None
#         self.btn_back.setEnabled(False)
#         self.btn_next.setEnabled(False)
#         self.btn_upload.clicked.connect(self.upload_file)
#         self.btn_next.clicked.connect(lambda: self.change_page(step=1))
#         self.btn_back.clicked.connect(lambda: self.change_page(step=-1))
#
#     def upload_file(self):
#         file_name = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', "PDF Files (*.pdf)")
#         if file_name[0]:
#             self.page_number = 0
#             self.generate_pages(file_name[0])
#
#     def generate_pages(self, file_name):
#         self.pdf_images = {}
#         with fitz.open(file_name) as file:
#             for i in range(file.page_count):
#                 self.pdf_images[i] = file[i].get_pixmap()
#         self.page_number = 0
#         self.read_pdf()
#
#     def read_pdf(self):
#         image = self.pdf_images[self.page_number]
#
#         # преобразование с помощью создания png
#         # png_name = 'image_page.png'
#         # image.save(png_name)
#         # image_px = QPixmap(png_name)
#
#         # преобразование с помощью pillow (без создания файла)
#         pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
#         qt_image = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGB888)
#         image_px = QPixmap.fromImage(qt_image)
#
#         self.label_reader.setPixmap(image_px)
#         self.label_reader.setAlignment(Qt.AlignCenter)
#         self.label_page.setText(str(self.page_number + 1))
#         self.btn_back.setEnabled(True)
#         self.btn_next.setEnabled(True)
#
#     def change_page(self, step):
#         self.page_number += step
#         if self.page_number < len(self.pdf_images) | self.page_number >= 0:
#             self.read_pdf()
#         else:
#             self.page_number -= step
#
#
# if __name__ == '__main__':
#     app = QApplication([])
#     window = PDFReader()
#     window.show()
#     sys.exit(app.exec_())
