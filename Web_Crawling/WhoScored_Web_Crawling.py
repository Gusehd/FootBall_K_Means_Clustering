from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pandas.io.html import read_html
import time
import pandas as pd
import numpy as np

url = "https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/7811/Stages/17590/PlayerStatistics/England-Premier-League-2019-2020"
defensivePath = '//*[@id="statistics-table-defensive"]'
offensivePath = '//*[@id="statistics-table-offensive"]'
passingPath = '//*[@id="statistics-table-passing"]'

defensiveName = "Defensive"
offensiveName = "Offensive"
passingName = "Passing"

sleepTime = 2
defensiveDF = ['Player', 'Player.1', 'Apps', 'Mins', 'Tackles', 'Inter', 'Fouls', 'Offsides', 'Clear', 'Drb', 'Blocks', 'OwnG', 'Rating']
offensiveDF = ['Player', 'Player.1', 'Apps', 'Mins', 'Goals', 'Assists', 'SpG', 'KeyP', 'Drb', 'Fouled', 'Off', 'Disp', 'UnsTch', 'Rating']
passingDF = ['Player', 'Player.1', 'Apps', 'Mins','Assists','KeyP','AvgP','PS%','Crosses','LongB','ThrB', 'Rating']

#browser = Service(".\chromedriver.exe")
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)

def getEnsive(name, columsTable, xmlPath):
    time.sleep(sleepTime)
    defense = driver.find_element_by_link_text(name)
    defense.click()

    time.sleep(sleepTime)
    all_player = driver.find_element_by_link_text('All players')
    all_player.click()

    time.sleep(sleepTime)
    page = driver.find_element_by_link_text('last')
    total_page = int(page.get_attribute('data-page'))

    df_defensive = pd.DataFrame(columns = columsTable)


    for i in np.arange(total_page)+1 :
        time.sleep(sleepTime)
        table = driver.find_element_by_xpath(xmlPath)
        table_html= table.get_attribute('innerHTML')
        df2 = read_html(table_html)[0]
        df_defensive = pd.concat([df_defensive, df2], axis=0)
        driver.find_element_by_link_text('next').click()

    return df_defensive


df1 = getEnsive(defensiveName, defensiveDF, defensivePath)
df2 = getEnsive(offensiveName, offensiveDF, offensivePath)
df3 = getEnsive(passingName, passingDF, passingPath)
df = pd.concat([df1, df2, df3], axis = 1)
df = df.T.drop_duplicates().T

df3
print(df3)

df.reset_index(drop=True, inplace=True)

def toCsv(tableName, path,check):
    tableName = tableName.reset_index()
    tableName.drop(['index','Player'] , axis=1, inplace=True)
    spl = tableName['Player.1'].str.split(',')

    name = []
    for i in range(len(spl)):
        a = spl[i][0]
        name.append(a)
    tableName['name']= name

    age = []
    for i in range(len(spl)):
        a = int(spl[i][1])
        age.append(a)
    tableName['age'] = age

    position1 = []
    for i in range(len(spl)):
        a = spl[i][2]
        position1.append(a)
    tableName['position1']=position1

    position2 = []
    for i in range(len(spl)):
        if len(spl[i]) > 3 :
            a = spl[i][3]
        else :
            a = np.nan
        position2.append(a)
    tableName['position2'] = position2

    tableName.drop('Player.1', axis =1, inplace=True)
    if check == 0:
        tableName = tableName.iloc[:,[11,12,13,14,0,1,2,3,4,5,6,7,8,9,10]]
        tableName.to_csv(path, sep=',', encoding='utf_8_sig')
    else:
        tableName = tableName.iloc[:, [10,11, 12, 13, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
        tableName.to_csv(path, sep=',', encoding='utf_8_sig')

defensiveCsv = toCsv(df1, "./defensive.csv",0)
offensiveCsv = toCsv(df2, "./offensive.csv",0)
passingCsv = toCsv(df3, "./passing.csv",1)