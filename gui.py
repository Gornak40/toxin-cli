#!/bin/python3
import sys, webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit,
    QLCDNumber, QGridLayout, QLabel, QMessageBox,
    QProgressBar, QComboBox, QStatusBar, QTableWidget,
    QTableWidgetItem, QAbstractItemView
    )
from PyQt5.QtGui import (
    QIcon, QPixmap
    )
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt


ICON = 'icon.ico'
DONATE = 'https://money.yandex.ru/to/410017272059424'


class ToxicUI(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		self.place()

	def initUI(self):
		self.setWindowTitle('Toxic')
		self.setWindowIcon(QIcon(ICON))
		self.lineEdit = QLineEdit()
		self.searchBtn = QPushButton()
		self.searchBtn.setText('Поиск')
		self.donateLbl = QLabel()
		self.donateLbl.setText('''Автор: Александр Горбунов (Gornak40)
Почта: s-kozelsk@yandex.ru
ВК/Телеграм: @gornak40
GitHub/Codeforces: @Gornak40''')
		self.donateBtn = QPushButton()
		self.donateBtn.setText('Спасибо')
		self.statusBar = QStatusBar()
		self.statusBar.showMessage('Добро пожаловать')
		pal = self.statusBar.palette()
		pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor('green'))
		self.statusBar.setPalette(pal)
		self.table = QTableWidget()
		self.table.hide()
		self.setFixedSize(0, 0)

	def place(self):
		self.grid = QGridLayout()
		self.grid.setSpacing(5)
		self.grid.addWidget(self.lineEdit, 0, 0, 1, 1)
		self.grid.addWidget(self.searchBtn, 0, 1, 1, 1)
		self.grid.addWidget(self.donateLbl, 1, 0, 1, 1)
		self.grid.addWidget(self.donateBtn, 1, 1, 1, 1)
		self.grid.addWidget(self.statusBar, 2, 0, 1, 2)
		self.grid.addWidget(self.table, 3, 0, 1, 2)
		self.setLayout(self.grid)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = ToxicUI()
	ex.show()
	sys.exit(app.exec())