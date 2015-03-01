import urllib2
import time
import datetime
import os
import csv
import json
from dateutil.parser import parse

def getStocks():
    SnP100File = 'S&P100.txt'
    SnPData = open(SnP100File,'r').read()
    splitSnPData = SnPData.split('\n')
    
    stocksToPull = []
    for eachLine in splitSnPData:
        splitLine = eachLine.split('\t')
        stocksToPull.append(splitLine[0])
        
    print stocksToPull
    return stocksToPull


def pullData(stock):
    try:
        today = datetime.date.today()
        saveDir = os.path.dirname(__file__) + "\\TempData"
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)

        print '\nCurrently pulling',stock
        urlToVisit = 'http://real-chart.finance.yahoo.com/table.csv?s=%s&d=%d&e=%d&f=%d&g=d&a=11&b=12&c=2000&ignore=.csv' % (stock, today.month - 1, today.day, today.year)
        # end: d is month-1, e is day, f is year
        # start: a is month-1, b is day, c is year

        print urlToVisit
        sourceCode = urllib2.urlopen(urlToVisit).read()
        fileDir = os.path.dirname(__file__) + '\\TempData'
        fileName = "tmp" + stock + ".txt"
        filePath = os.path.join(fileDir, fileName)
        print 'Pulled',stock
        text_file = open(filePath, "w")
        text_file.write(sourceCode)
        print stock + ".txt file created"

        text_file.close()
        text_file = open(filePath, "r")
        # text_file.seek(0)
        saveDir = os.path.dirname(__file__) + '\\TempData'
        saveName = "Output" + stock + ".txt"
        jsonName = "Output" + stock + ".json"
        savePath = os.path.join(saveDir, saveName)
        jsonPath = os.path.join(saveDir, jsonName)
        saveFile = open(savePath, "w")
        saveFile.write(text_file.readline())
        for line in reversed(text_file.readlines()):
            saveFile.write(line)

        saveFile.close()
        text_file.close()

        csvfile = open(savePath, 'r')
        jsonfile = open(jsonPath, 'w')

        fieldnames = ("Date", "Adj Close")

        size = len(list(csv.DictReader(csvfile, fieldnames)))
        csvfile.seek(0)

        reader = csv.DictReader(csvfile, fieldnames)

        cnt = 0

        jsonfile.write('[\n')

        firstrow = True
        for row in reader:
            content = list(row[i] for i in fieldnames)
            if firstrow is False:
                parseddate = parse(str(content[0]))
                content[0] = int(time.mktime(parseddate.timetuple()) * 1000)
                content[1] = round(float(content[1]), 2)
                json.dump(content, jsonfile)
                if cnt < size - 1:
                    jsonfile.write(',\n')
            firstrow = False
            cnt += 1

        jsonfile.write('\n]')

        return sourceCode
                
    except Exception, e:
        print 'main loop', str(e)

                
def csvFlipper(readFileName, saveFileName):
    readFilePath = os.path.join(saveDir, readFileName)
    readFile = open(readFilePath,'r')
    saveFilePath = os.path.join(saveDir, saveFileName)
    saveFile = open(saveFilePath, 'w')
    saveFile.write(readFile.readline())  #To keep header
    
    for line in reversed(readFile.readlines()):
        saveFile.write(line)
    
    readFile.close()
    saveFile.close()


def printStock(sourceCode):
    dates = []
    for lines in sourceCode[1:]:
        dates.append(lines.split(',')[0])
    close = []
    for lines in sourceCode[1:]:
        close.append(float(lines.split(',')[-1]))

    # plt.plot(dates,close)
    # plt.ylabel('Adj Close')
    # plt.xlabel('Dates')
