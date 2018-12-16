import requests
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re
import urllib2
import pandas as pd
import logging
import optionals

# def getWords(request):
#     return request.split()

def getListOfNewspaper(file):
    logging.info('getListOfNewspaper')
    df = pd.read_csv(file,header=0,names=['index','racine','racine_recherche','addword','scale','full_links','className','div'],dtype={'scale':np.float64,'full_links':np.bool})
    df['scale'] = df['scale']/10
    # df['full_links'] = df['full_links'].map({'True':True,'False':False})
    df.set_index('index')
    return df


def takeRandomElements(list):
    number_of_articles = 3
    randomElements = list.sample(n=number_of_articles)
    if debug :
        logging.debug('takeRandomElements - print randomElements')
        print(randomElements)
    return randomElements

def getBestSort(possibilities):
    nb = len(possibilities[0])
    avgList = []
    sqrdList = []
    tempList = []
    for possibility in possibilities :
        avgList,sqrdList,tempList=getAvgSqrdTemp(possibility,nb,avgList,sqrdList,tempList)
    bestchoice = 0
    if debug :
        logging.debug('getBestSort - print different lists')
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
        logging.debug('takeRandomElements - final choice : %s ; %s ; %s',avgList[bestchoice],sqrdList[bestchoice],tempList[bestchoice])
        print(avgList[bestchoice],sqrdList[bestchoice],tempList[bestchoice])
    return bestchoice

def getAvgSqrdTemp(possibility,nb,avgList,sqrdList,tempList):
    avg = sum(newspaper[4] for newspaper in possibility)/float(nb)
    avgList.append(avg)
    sqrd = sum(newspaper[4]**2 for newspaper in possibility)/float(nb)
    sqrdList.append(sqrd)
    temp = sqrd/(0.00001+avg)
    tempList.append(temp)
    return avgList,sqrdList,tempList

def doMultipleSelections(db):
    logging.info('doMultipleSelections')
    number_of_selections = 50
    possibilities = []
    for i in range(number_of_selections):
        possibilities.append(takeRandomElements(db).values)
    bestchoice = getBestSort(possibilities)
    if debug :
        logging.debug('doMultipleSelections - choix final')
        printList(possibilities[bestchoice])
    return possibilities[bestchoice]

def getListofURL(requestSplitted,list):
    logging.info('getListofURL')
    listOfUrl = []
    for newsPaper in list :
        url = newsPaper[2]
        for word in requestSplitted :
            url+=str(word)+newsPaper[3]
        listOfUrl.append([newsPaper[0],url])
    if debug :
        logging.debug('getListofURL - print list')
        printList(listOfUrl)
    return listOfUrl

def getArticles(listofpages,db):
    logging.info('getArticles')
    listofarticles = []
    for index,page in listofpages :
        # r = requests.get(page)
        # print(r.text)
        # r2 = rh.HTML(html=page)
        # print(r2.links)
        html_page = urllib2.urlopen(page)
        soup = BeautifulSoup(html_page,'lxml')
        links = []
        if debug:
            logging.debug('getArticles - newspaper : %s',db.loc[db['index']==index]['racine'].values[0])
        for div in soup.find_all(db.loc[db['index']==index]['div'].values[0], {'class': db.loc[db['index']==index]['className'].values[0]}):
            for link in div.find_all('a'):#, attrs={'href': re.compile('^'+db.loc[db['index']==index]['racine'].values[0])}):
                l = getLinkName(link,index)
                if not(l in links):
                    links.append(l)
        randomLink = chooseRandom(links)
        listofarticles.append(randomLink)
    return listofarticles

def getLinkName(link,index):
    l = ''
    if not(db.loc[db['index']==index]['full_links'].values[0]):
        l = db.loc[db['index']==index]['racine'].values[0]
    return l+link.get('href')

def chooseRandom(list):
    return random.choice(list)

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
    logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s',level=logging.DEBUG)
    logging.info('Started')
    debug = False
    SEARCH = sys.argv[1:]
    file = 'db.csv'
    db = getListOfNewspaper(file)
    listofnewspaper = doMultipleSelections(db)
    listofsearchurl = getListofURL(SEARCH,listofnewspaper)
    listofarticles = getArticles(listofsearchurl,db)
    optionals.printList(listofarticles)
    logging.info('End')
