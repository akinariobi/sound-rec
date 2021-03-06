import numpy as np
from sklearn.externals import joblib
from math import *
import operator

"""
Предсказание (массив чисел) это вектор, который представляет распределения вероятностей списка потенциальных результатов.
"""
# словарь, где будут храниться пары: песня-предсказание (типы данных: строка-массив)
# пример: {'Был-пацан.mp3': [1,1,0,1,...], ...}
songLibrary = {}
counter = 0
# predictions = joblib.load('UserTestSongs.prediction')
# подгружаем полученные в predictions.py предсказания
predictions = joblib.load('predictions.data')
rockPredictions = joblib.load('extraRock.prediction')

# сопоставляем полученные предсказания с названиями треков
with open('songTitles.txt') as f:
   for line in f:
       songLibrary[line.strip('\n')] = predictions[counter]
       counter += 1

# incubus.txt содержит названия хитов лучшей в мире группы incubus, записанные в этот файл построчно
# мы сопоставляем каждую песню с предсказаниями полученными для жанра роцк и добавляем эти пары в словарь
# songLibrary
rockCounter = 0
with open('incubus.txt') as f:
   for line  in f:
       songLibrary[line.strip('\n')] = rockPredictions[rockCounter]
       rockCounter += 1

# берем одну из песен великолепной группы incubus и ищем топ 10 самых похожих на неё в созданном ранее словаре songLibrary
querySong = "Cocoa Butter Kisses (ft Vic Mensa & Twista) (Prod by Cam for JUSTICE League & Peter Cottont (DatPiff Exclusive)"

# получаем массив с распределением вероятностей соответствующий анализируемой песне
# элементы в массиве predictions в данном случае представляют собой векторы распределения вероятностей
querySongData = songLibrary[querySong]

# удаляем анализируемую песню из словаря, чтобы не было дубликатов 
del songLibrary[querySong]

# находим топ 10 похожих песен

# инициализируем словарь, куда будем грузить похожие песни
topSongs = {}

# обходим каждый элемент словаря со всеми предсказаниями в цикле
for key, value in songLibrary.iteritems():
    # считаем дистанцию между треком, для которого ищем похожие и каждым треком, записанным в словарь songLibrary
    # метод linalg.norm: возвращает норму матрицы или вектора
    dist = np.linalg.norm(querySongData-songLibrary[key])
    # создаем пару: дистанция-название_композиции и добавляем эту пару в словарь topSongs
    topSongs[key] = dist

# сортируем треки в словаре по величине дистанции, от самой маленькой (наиболее похожие) до самой большой (наименее похожие)
sortedSongs = sorted(topSongs.items(), key=operator.itemgetter(1))
# берем первые 10 треков с самыми маленькими дистанциями между ними и эталонным треком
sortedSongs = sortedSongs[:10]

# очередной бесполезный вывод в консоль
for value in sortedSongs:
    print value


# получаем координаты первых 10 песен для дальнейшей визуализации 
topSongDistances = {}
for val in sortedSongs:

    topSongDistances[val[0]] = songLibrary[val[0]]

topSongDistances[querySong] = querySongData

# print topSongDistances

# joblib.dump(topSongDistances, 'kanyeHeartless.playlist')
