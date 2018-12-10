import requests
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

# def getWords(request):
#     return request.split()

def getListOfNewspaper():
    listOfnewspaper = [
    ['https://www.humanite.fr/search/','%20',-1.0],
    ['https://www.marianne.net/recherche?k=','+',-0.8],
    ['https://www.liberation.fr/recherche/?sort=-publication_date_time&period=last_180&period_start_day=0&period_start_month=0&period_start_year=0&period_end_day=0&period_end_month=0&period_end_year=0&editorial_source=&paper_channel=&q=','+',-0.6],
    ['https://www.lexpress.fr/recherche?q=','+',-0.4],
    ['https://www.lemonde.fr/recherche/?page_num=1&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=10&end_month=12&end_year=2018&sort=desc&keywords=','+',-0.2],
    ['https://www.la-croix.com/Recherche/','%20',0.2],
    ['https://www.lepoint.fr/recherche/index.php?query=','%20',0.4],
    ['http://recherche.lefigaro.fr/recherche/','%20',0.6],
    ['https://www.lejdd.fr/recherche?query=','+',0.8],
    ['https://recherche.lesechos.fr/recherche.php?exec=1&texte=','+',1.0]
    ]
    return listOfnewspaper
    # 'liberation','lenouvelobs','lexpress','lemonde','lacroix',
    # 'lepoint','lefigaro','jdd','echos','tribune']

def printList(list):
    for e in list:
        print e

def takeRandomElements(list):
    number_of_articles = 3
    randomElements = random.sample(list,number_of_articles)
    if debug :
        print('Random Elements')
        print(randomElements)
    return randomElements

def getBestSort(possibilities):
    nb = len(possibilities[0])
    avgList = []
    sqrdList = []
    tempList = []
    for possibility in possibilities :
        avg = sum(newspaper[2] for newspaper in possibility)/float(nb)
        avgList.append(avg)
        sqrd = sum(newspaper[2]**2 for newspaper in possibility)/float(nb)
        sqrdList.append(sqrd)
        temp = sqrd/(0.00001+avg)
        tempList.append(temp)
    bestchoice = 0
    if debug :
        print('Avg')
        print(avgList)
        print('Sqrd')
        print(sqrdList)
        print('tempList')
        print(tempList)
    for i in range(nb):
        if abs(tempList[i]) > abs(tempList[bestchoice]) :
            bestchoice = i
    if debug :
        print('Final')
        print(avgList[bestchoice],sqrdList[bestchoice],tempList[bestchoice])
    return bestchoice

def doMultipleSelections():
    number_of_selections = 50
    possibilities = []
    db = getListOfNewspaper()
    for i in range(number_of_selections):
        possibilities.append(takeRandomElements(db))
    bestchoice = getBestSort(possibilities)
    if debug :
        print('Choix final')
        printList(possibilities[bestchoice])
    return possibilities[bestchoice]


def getListofURL(requestSplitted,list):
    listOfUrl = []
    for newsPaper in list :
        url = newsPaper[0]
        for word in requestSplitted :
            url+=str(word)+newsPaper[1]
        listOfUrl.append(url)
    printList(listOfUrl)
    return listOfUrl

if __name__ == "__main__":
    # SEARCH = "gilets jaunes"
    debug = False
    SEARCH = sys.argv[1:]
    T = []
    for i in range(10000):
        listofnewspaper = doMultipleSelections()
        listofurl = getListofURL(SEARCH,listofnewspaper)
        T+=listofurl
    plt.hist(T)
    plt.show()
