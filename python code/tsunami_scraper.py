# -*- coding: utf-8 -*-

import os
import csv
import requests
from bs4 import BeautifulSoup

# Function to obtain the list of tsunamis that occured in the world.
def createTsunamiList (ourUrl,itemList):
    # Download the webpage with the requests library.
    page = requests.get(ourUrl)
    # If download was successful proceed.
    if page.status_code == 200:
        # We parse the downloaded webpage with the BeautifulSoup library.
        ourContent = BeautifulSoup(page.content, "html.parser")
        # Analyzing the html structure we detect that the table that contains
        # the data that we want to obtain, is the third one (index=2).
        tsunamiTable = (ourContent.findAll('table'))[2]
        # We are nost interested in the first three rows as they just contain
        # the headers of the table. We will get all rows from the 4th till
        # the last one.
        for row in tsunamiTable.findAll('tr')[3::]:
            # For each row we want to find all the cells.
            rowCells = row.findAll('td')
            # We get the text of each cell we are interested on.
            year = rowCells[0].find(text=True)
            month = rowCells[1].find(text=True)
            day = rowCells[2].find(text=True)
            validity = rowCells[6].find(text=True)
            causeCode = rowCells[7].find(text=True)
            earthquakeMagnitude = rowCells[8].find(text=True)
            locationCountry = rowCells[12].find(text=True)
            locationName = rowCells[13].find(text=True)
            locationLat = rowCells[14].find(text=True)
            locationLong = rowCells[15].find(text=True)
            maxWaterHeight = rowCells[16].find(text=True)
            runups = rowCells[17].find(text=True)
            numDeaths = rowCells[21].find(text=True)
            numInjuries = rowCells[23].find(text=True)
            descrDamage = rowCells[26].find(text=True)
            numDestroyedHouses = rowCells[27].find(text=True)
            # With the data we obtained from each table row, we create 
            # a new item that will be a row in the future csv file. It is a
            # list with the different tsunami attributes.
            item = [year,month,day,validity,causeCode,earthquakeMagnitude,locationCountry,locationName,locationLat,locationLong,maxWaterHeight,runups,numDeaths,numInjuries,descrDamage,numDestroyedHouses]
            # We add each item to the list of items
            itemList.append(item)
        return

# We define the website that we want to scrap. 
#tsunamisUrl = 'https://www.ngdc.noaa.gov/nndc/struts/results?bt_0=2018&st_0=2018&type_8=EXACT&query_8=None+Selected&op_14=eq&v_14=&st_1=&bt_2=&st_2=&bt_1=&bt_10=&st_10=&ge_9=&le_9=&bt_3=&st_3=&type_19=EXACT&query_19=None+Selected&op_17=eq&v_17=&bt_20=&st_20=&bt_13=&st_13=&bt_16=&st_16=&bt_6=&st_6=&ge_21=&le_21=&bt_11=&st_11=&ge_22=&le_22=&d=7&t=101650&s=70'   
tsunamisUrl = 'https://www.ngdc.noaa.gov/nndc/struts/results?bt_0=&st_0=&type_8=EXACT&query_8=None+Selected&op_14=eq&v_14=&st_1=&bt_2=&st_2=&bt_1=&bt_10=&st_10=&ge_9=&le_9=&bt_3=&st_3=&type_19=EXACT&query_19=None+Selected&op_17=eq&v_17=&bt_20=&st_20=&bt_13=&st_13=&bt_16=&st_16=&bt_6=&st_6=&ge_21=&le_21=&bt_11=&st_11=&ge_22=&le_22=&d=7&t=101650&s=70'

# We create the list of tsunamis that occurred worldwide, adding first the 
# header to the list, and afterwards calling the createTsunamiList function to 
# obtain the data about all tsunamis.
tsunamiList = []
headerList = ['year','month','day','validity','causeCode','earthquakeMagnitude','locationCountry','locationName','locationLat','locationLong','maxWaterHeight','runups','numDeaths','numInjuries','descrDamage','numDestroyedHouses']
tsunamiList.append(headerList)
createTsunamiList(tsunamisUrl, tsunamiList)

# We define the name and location of the csv file that is going to be generated.
filename = 'tsunamis_dataset.csv'
currentDir = os.path.dirname(__file__)
filePath = os.path.join(currentDir, filename)

# We finally write all tsunami data in a csv file with the csv library.  
with open(filePath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for tsunamiElement in tsunamiList:
            writer.writerow(tsunamiElement)