# pip install pyqt5
# pip install pymupdf
# pip install pillow

import sys
import fitz

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPen, QPainter
from PyQt5.QtCore import Qt, QRect
from PIL import Image


class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super(CustomLabel, self).__init__(parent)
        self.data_rectangles = {}
        self.start_point = None
        self.end_point = None
        self.rectangle = None
        self.page = None

    def mousePressEvent(self, event):
        """Считывание стартовой координаты при нажатии левой кнопки мыши"""
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = event.pos()

    def mouseMoveEvent(self, event):
        """Считывание координат при движении мыши, если зажата левая кнопка"""
        if event.buttons() == Qt.LeftButton:
            self.end_point = event.pos()
            # обновление виджета, чтобы сработал метод paintEvent
            self.update()

    def mouseReleaseEvent(self, event):
        """Добавление прямоугольника в словарь при отпускании мыши"""
        if self.rectangle:
            # если 1 прямоугольник
            self.data_rectangles[self.page] = self.rectangle
        print(self.data_rectangles)

    def paintEvent(self, event):
        """Метод отрисовки прямоугольника"""
        super(CustomLabel, self).paintEvent(event)

        # создание кисти для рисования
        painter = QPainter(self)
        pen = QPen(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)
        # если была нажата левая кнопка мыши и сдвинута мышь
        if self.start_point and self.end_point:
            self.rectangle = QRect(self.start_point, self.end_point).normalized()
            painter.drawRect(self.rectangle)

        # если был создан прямоугольник на текущей странице до этого
        elif self.page in self.data_rectangles:
            painter.drawRect(self.data_rectangles[self.page])

    def clear_rectangle(self):
        self.start_point = None
        self.end_point = None
        self.rectangle = None


class PDFReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 900)
        self.setMinimumSize(QtCore.QSize(800, 900))
        self.setWindowTitle("pdf reader")

        # создание центрального виджета
        self.centralwidget = QtWidgets.QWidget(self)

        # Добавление пустых виджетов на центральный
        self.widget_control = QtWidgets.QWidget(self.centralwidget)
        self.widget_reader = QtWidgets.QWidget(self.centralwidget)
        self.widget_page_number = QtWidgets.QWidget(self.centralwidget)

        #  создание слоёв с политикой выравнивания
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_control)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_reader)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_page_number)

        # добавление виджетов на вертикальный слой
        self.verticalLayout.addWidget(self.widget_control)
        self.verticalLayout.addWidget(self.widget_reader)
        self.verticalLayout.addWidget(self.widget_page_number)

        # добавление кнопок на верхний виджет
        self.btn_upload = QtWidgets.QPushButton(self.widget_control)
        self.btn_upload.setText("Загрузить")

        self.btn_back = QtWidgets.QPushButton(self.widget_control)
        self.btn_back.setText("<<")
        self.btn_back.setEnabled(False)

        self.btn_next = QtWidgets.QPushButton(self.widget_control)
        self.btn_next.setText(">>")
        self.btn_next.setEnabled(False)

        # добавление элементов на верхний горизонтальный слой
        self.horizontalLayout.addWidget(self.btn_upload)
        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.spacerItem)
        self.horizontalLayout.addWidget(self.btn_back)
        self.horizontalLayout.addWidget(self.btn_next)

        # добавление изменённого объекта Label для возможности рисования на нём
        self.label_reader = CustomLabel(self.widget_reader)

        # добавление элементов на средний горизонтальный слой
        self.horizontalLayout_2.addWidget(self.label_reader)

        # добавление элемента для показа номера страницы на нижний виджет
        self.label_page = QtWidgets.QLabel(self.widget_page_number)
        self.label_page.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_page.setAlignment(QtCore.Qt.AlignCenter)

        # добавление на нижний слой
        self.horizontalLayout_3.addWidget(self.label_page)

        # политика выравнивания относительно друг друга
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_control.sizePolicy().hasHeightForWidth())
        self.widget_control.setSizePolicy(sizePolicy)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_reader.sizePolicy().hasHeightForWidth())
        self.widget_reader.setSizePolicy(sizePolicy)

        # выдвижение виджетов на передний план
        self.widget_control.raise_()
        self.widget_reader.raise_()
        self.widget_page_number.raise_()

        # добавление всех элементов на главное окно
        self.setCentralWidget(self.centralwidget)

        # привязка функций к кнопкам
        self.btn_upload.clicked.connect(self.upload_file)
        self.btn_next.clicked.connect(lambda: self.change_page(step=1))
        self.btn_back.clicked.connect(lambda: self.change_page(step=-1))

        # номер страницы
        self.page_number = None
        # словарь для хранения изображений страниц
        self.pdf_images = {}

    def upload_file(self):
        """Загрузка файла"""
        file_name = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', "PDF Files (*.pdf)")

        # если файл выбран, то начать генерацию
        if file_name[0]:
            self.generate_pages(file_name[0])

    def generate_pages(self, file_name):
        """Генерация словаря для хранения изображений страниц"""
        with fitz.open(file_name) as file:
            for page in range(file.page_count):
                # {номер страницы: страница в виде объекта pixmap}
                self.pdf_images[page] = file[page].get_pixmap()
        self.page_number = 0
        self.read_pdf()

    def read_pdf(self):
        """Загрузка страницы в объект CustomLabel"""
        image = self.pdf_images[self.page_number]

        # преобразование с помощью создания png
        # png_name = 'image_page.png'
        # image.save(png_name)
        # image_px = QPixmap(png_name)

        # преобразование страницы из pixmap в изображение с помощью pillow (без создания файла)
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        qt_image = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGB888)
        image_px = QPixmap.fromImage(qt_image)

        # загрузка изображения в CustomLabel
        self.label_reader.setPixmap(image_px)
        self.label_reader.setAlignment(Qt.AlignCenter)

        # привязываем номер страницы к объекту self.label_reader
        self.label_reader.page = self.page_number

        # отображение номера страницы
        self.label_page.setText(str(self.page_number + 1))

        # включение кнопок после загрузки файла
        self.btn_back.setEnabled(True)
        self.btn_next.setEnabled(True)

    def change_page(self, step):
        """Изменение страницы"""
        self.page_number += step

        # проверка номера страницы на валидность
        if self.page_number < len(self.pdf_images) | self.page_number >= 0:
            self.label_reader.clear_rectangle()
            self.read_pdf()
        else:
            self.page_number -= step


if __name__ == '__main__':
    print("Starting", sys.argv[0])
    app = QApplication([])
    window = PDFReader()
    window.show()
    sys.exit(app.exec_())
