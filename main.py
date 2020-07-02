#!/bin/python3
from gui import *
from requests import get
from bs4 import BeautifulSoup
from re import search
from urllib.request import urlretrieve


urlbs = lambda x: BeautifulSoup(get(x).content, 'lxml')
enc = lambda x: str(x.encode('cp1251'))[2:-1].replace('\\x', '%').upper()
date = lambda x: x[x.find(',') - 4:x.find(',')]
dur = lambda x: search(r'\d\d\:\d\d', x).group(0) if search(r'\d\d\:\d\d', x) else None
good = lambda x: [i for i in filter(bool, x)]
rate = lambda x: search(r'/(\d+)\.', x).group(0)[1:-1]
main = 'http://torrminator.com'
home = '''{}/index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&result_from=1&story='''.format(main)


class Toxic:
	def __init__(self):
		self.app = QApplication(sys.argv)
		self.ex = ToxicUI()
		self.connect()
		self.showUI()

	def connect(self):
		self.ex.searchBtn.clicked.connect(self.searchFunc)
		self.ex.donateBtn.clicked.connect(self.donateFunc)
		self.ex.table.doubleClicked.connect(self.chooseFunc)

	def showUI(self):
		self.ex.show()
		sys.exit(self.app.exec())

	def donateFunc(self):
		webbrowser.open(DONATE)

	def message(self, mes):
		self.ex.statusBar.showMessage(mes)

	def searchFunc(self):
		self.message('Кликнете дважды на понравившейся фильм')
		self.name = self.ex.lineEdit.text()
		self.url = home + enc(self.name)
		self.bs = urlbs(self.url)
		self.films = self.bs.select('#dle-content > div.post > div.post-title > a')
		self.names = [x.text.strip() for x in self.films]
		self.links = [x.get('href') for x in self.films]
		self.films = self.bs.select('#dle-content > div.post > div.data > span:nth-child(1)')
		self.dates = [date(x.text.strip()) for x in self.films]
		self.films = self.bs.select('#dle-content > div.post > div.post-story')
		self.durat = good([dur(x.text.strip()) for x in self.films])
		self.css = '#dle-content > div.post > div.data > div.cell2 > img'
		self.rates = [i.get('src') for i in self.bs.select(self.css)]
		self.rates = ['https://rating.kinopoisk.ru/{}.xml'.format(rate(i)) for i in self.rates]
		self.films = [urlbs(x) for x in self.rates]
		self.rkino = [round(float(x.select('rating > kp_rating')[0].text), 1) for x in self.films]
		self.rimdb = [round(float(x.select('rating > imdb_rating')[0].text), 1) for x in self.films]
		self.head = ['Название', 'Длительность', 'Год', 'Кинопоиск', 'IMDB']
		self.setTable(self.head, self.names, self.durat, self.dates, self.rkino, self.rimdb)

	def chooseFunc(self):
		self.ind = self.ex.table.selectedItems()[0].row()
		self.message('Выберите файл фильма {}'.format(self.names[self.ind]))
		self.url = self.links[self.ind]
		self.bs = urlbs(self.url)
		self.css = '#dle-content > div.post > div.post-story > table'
		self.films = self.bs.select(self.css)[0]
		self.films = self.films.select('tbody > tr')
		self.torrs = [main + x.select('td > a')[0].get('href') for x in self.films]
		self.films = [x.select('td > b') for x in self.films]
		self.sizes = [float(x[1].text.strip('\xa0GB')) for x in self.films]
		self.seeds = [int(x[2].text) for x in self.films]
		self.peers = [int(x[3].text) for x in self.films]
		self.head = ['Размер', 'Сиды', 'Пиры']
		self.setTable(self.head, self.sizes, self.seeds, self.peers)

		self.ex.table.doubleClicked.disconnect()
		self.ex.table.doubleClicked.connect(self.fileFunc)

	def fileFunc(self):
		self.message('Торрент файл загружен')
		self.indt = self.ex.table.selectedItems()[0].row()
		self.filename = '{} ({}).torrent'.format(self.names[self.ind], self.dates[self.ind])#.replace(' ', '_')
		urlretrieve(self.torrs[self.indt], self.filename)
		self.ex.table.hide()
		self.ex.setFixedSize(0, 0)
		self.ex.lineEdit.clear()
		self.ex.table.doubleClicked.disconnect()
		self.ex.table.doubleClicked.connect(self.chooseFunc)

	def setTable(self, head, *args):
		self.ex.table.clear()
		self.ex.table.setColumnCount(len(head))
		self.ex.table.setRowCount(len(args[0]))
		self.ex.table.setHorizontalHeaderLabels(head)
		for i in range(len(args)):
			for j in range(len(args[i])):
				self.ex.table.setItem(j, i, QTableWidgetItem(str(args[i][j])))
		self.ex.table.resizeColumnsToContents()
		self.ex.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.ex.setMinimumSize(QSize(650, 480))
		self.ex.table.show()


if __name__ == '__main__':
	Toxic()