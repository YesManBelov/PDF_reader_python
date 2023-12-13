import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPen, QPainter
from PyQt5.QtCore import Qt, QRect


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

        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # добавление элементов на верхний горизонтальный слой
        self.horizontalLayout.addWidget(self.btn_upload)
        self.horizontalLayout.addWidget(self.spacerItem)
        self.horizontalLayout.addWidget(self.btn_back)
        self.horizontalLayout.addWidget(self.btn_next)

        # добавление изменённого объекта Label для возможности рисования на нём
        self.label_reader = QLabel(self.widget_reader)
        self.horizontalLayout_2.addWidget(self.label_reader)

        # добавление элемента для показа номера страницы на нижний виджет
        self.label_page = QLabel(self.widget_page_number)
        self.horizontalLayout_3.addWidget(self.label_page)
        self.label_page.setAlignment(QtCore.Qt.AlignCenter)

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

        self.widget_control.raise_()
        self.widget_reader.raise_()
        self.widget_page_number.raise_()

        self.setCentralWidget(self.centralwidget)


