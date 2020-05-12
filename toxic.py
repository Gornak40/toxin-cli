#!/bin/python3
from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
from re import search
from prettytable import PrettyTable
from sys import argv
from urllib.request import urlretrieve
from progressbar import ProgressBar, Bar
from time import sleep


def table(head, *args):
    T = PrettyTable(['#'] + head)
    for x in zip(range(1, len(args[0]) + 1), *args):
        T.add_row(x)
    print(T)
    while True:
        try:
            ind = int(input('# '))
            if 1 <= ind <= len(args[0]):
                return ind - 1
        except ValueError:
            pass
        except KeyboardInterrupt:
            exit(0)
    return ind


urlbs = lambda x: BeautifulSoup(get(x).content, 'lxml')
enc = lambda x: str(x.encode('cp1251'))[2:-1].replace('\\x', '%').upper()
date = lambda x: x[x.find(',') - 4:x.find(',')]
dur = lambda x: search(r'\d\d\:\d\d', x).group(0) if search(r'\d\d\:\d\d', x) else None
good = lambda x: [i for i in filter(bool, x)]
rate = lambda x: search(r'/(\d+)\.', x).group(0)[1:-1]


main = 'http://filmitorrent.net'
home = '''http://filmitorrent.net/index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&result_from=1&story='''
name = ' '.join(argv[1:])
# name = 'Джон уик' #
url = home + enc(name)
bs = urlbs(url)
films = bs.select('#dle-content > div.post > div.post-title > a')
names = [x.text.strip() for x in films]
links = [x.get('href') for x in films]
films = bs.select('#dle-content > div.post > div.data > span:nth-child(1)')
dates = [date(x.text.strip()) for x in films]
films = bs.select('#dle-content > div.post > div.post-story')
durat = good([dur(x.text.strip()) for x in films])
css = '#dle-content > div.post > div.data > div.cell2 > img'
rates = [i.get('src') for i in bs.select(css)]
rates = ['https://rating.kinopoisk.ru/{}.xml'.format(rate(i)) for i in rates]
films = [urlbs(x) for x in rates]
rkino = [round(float(x.select('rating > kp_rating')[0].text), 1) for x in films]
rimdb = [round(float(x.select('rating > imdb_rating')[0].text), 1) for x in films]

head = ['Название', 'Длительность', 'Год', 'Кинопоиск', 'IMDB']
ind = table(head, names, durat, dates, rkino, rimdb)
url = links[ind]


bs = urlbs(url)
css = '#dle-content > div.post > div.post-story > table'
films = bs.select(css)[0]
films = films.select('tbody > tr')
torrs = [main + x.select('td > a')[0].get('href') for x in films]
films = [x.select('td > b') for x in films]
sizes = [float(x[1].text.strip('\xa0GB')) for x in films]
seeds = [int(x[2].text) for x in films]
peers = [int(x[3].text) for x in films]
head = ['Размер', 'Сиды', 'Пиры']
ind = table(head, sizes, seeds, peers)
urlretrieve(torrs[ind], 'tor.torrent')


bar = ProgressBar(maxval=100).start()
for i in range(101):
    bar.update(i)
    sleep(0.01)
bar.finish()
