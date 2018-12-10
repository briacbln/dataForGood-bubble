import requests
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re
import urllib2
import pandas as pd

# def getWords(request):
#     return request.split()

def getListOfNewspaper(file):
    df = pd.read_csv(file,header=0,names=['index','racine','racine_recherche','addword','scale'])
    df['scale'] = df['scale'].convert_objects(convert_numeric=True)
    df.set_index('index')
    return df
    # 'liberation','lenouvelobs','lexpress','lemonde','lacroix',
    # 'lepoint','lefigaro','jdd','echos','tribune']

def printList(list):
    for e in list:
        print(e)

def takeRandomElements(list):
    number_of_articles = 3
    randomElements = list.sample(n=number_of_articles)
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
        for newspaper in possibility :
            print (newspaper,newspaper[3],type(newspaper[3]))
        avg = sum(newspaper[4] for newspaper in possibility)/float(nb)
        avgList.append(avg)
        sqrd = sum(newspaper[4]**2 for newspaper in possibility)/float(nb)
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

def doMultipleSelections(db):
    number_of_selections = 50
    possibilities = []
    for i in range(number_of_selections):
        possibilities.append(takeRandomElements(db).values)
    bestchoice = getBestSort(possibilities)
    if debug :
        print('Choix final')
        printList(possibilities[bestchoice])
    return possibilities[bestchoice]

def getListofURL(requestSplitted,list):
    listOfUrl = []
    for newsPaper in list :
        url = newsPaper[2]
        for word in requestSplitted :
            url+=str(word)+newsPaper[3]
        listOfUrl.append([newsPaper[0],url])
    printList(listOfUrl)
    return listOfUrl

def getArticles(listofpages,db):
    listofarticles = []
    for index,page in listofpages :
        # r = requests.get(page)
        # print(r.text)
        # r2 = rh.HTML(html=page)
        # print(r2.links)
        html_page = urllib2.urlopen(page)
        soup = BeautifulSoup(html_page,'lxml')
        if debug:
            print(db.loc[db['index']==index]['racine'].values[0])
        for link in soup.findAll('a'):#, attrs={'href': re.compile('^'+db.loc[db['index']==index]['racine'].values[0])}):
            print(link.get('href'))
        # break
    return listofarticles

def test(nb):
    debug = False
    T = []
    for i in range(nb):
        listofnewspaper = doMultipleSelections()
        listofurl = getListofURL('test',listofnewspaper)
        T+=listofurl
    plt.hist(T)
    plt.show()




if __name__ == "__main__":
    # SEARCH = "gilets jaunes"
    debug = True
    SEARCH = sys.argv[1:]
    file = 'db.csv'
    db = getListOfNewspaper(file)
    listofnewspaper = doMultipleSelections(db)
    listofsearchurl = getListofURL(SEARCH,listofnewspaper)
    listofarticles = getArticles(listofsearchurl,db)
