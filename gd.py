import datetime as dt
from collections import defaultdict
import numpy as np
import csv
import os
import urllib
import zipfile
import csv

def median(list):
    return np.median(np.array(list))


date = raw_input("What day would you like to download? (YYYYMMDD)")
localDestination = "Datasets/" + date + ".gkg.csv.zip"
URLpath = "http://data.gdeltproject.org/gkg/" + date + ".gkg.csv.zip"
resultFilePath, responseHeaders = urllib.urlretrieve(URLpath, localDestination)
zip_ref = zipfile.ZipFile(resultFilePath, 'r')
zip_ref.extractall('Datasets')
zip_ref.close()

unzipped_file = "Datasets/" + date + ".gkg.csv"
g = open(unzipped_file)

reader = csv.reader(g, delimiter = ",")
data = list(reader)
row_count = len(data)
print row_count

g.close()

f = open(unzipped_file)

headers = f.readline()

latitude_array = []
longitude_array = []
tone_array = []
actor_array = []
organization_array = []
for i in range(row_count-3):
    row = f.readline()
    row = row.split("\t")
    if 'ENV_DEFORESTATION' in row[3].split(";"):
        print 'Number %d has an article on deforestation ' %i
        tone_array.append([float((row[7].split(","))[0]),float((row[7].split(","))[3])])

        if row[5].split(";") not in actor_array:
            actor_array.append(row[5].split(";"))

        if row[6].split(";") not in organization_array:
            organization_array.append(row[6].split(";"))

        for entry in row[4].split(";"):
            try:
                latitude_array.append(float((entry.split("#"))[4]))
                longitude_array.append(float((entry.split("#"))[5]))
            except ValueError:
                latitude_array.append(0)
                longitude_array.append(0)
    if 'WB_1980_AGRO_FORESTRY' in row[3].split(";"):
        print 'Number %d has an article on agroforestry'  %i
        tone_array.append([float((row[7].split(","))[0]),float((row[7].split(","))[3])])

        if row[5].split(";") not in actor_array:
            actor_array.append(row[5].split(";"))

        if row[6].split(";") not in organization_array:
            organization_array.append(row[6].split(";"))

        for entry in row[4].split(";"):
            try:
                latitude_array.append(float((entry.split("#"))[4]))
                longitude_array.append(float((entry.split("#"))[5]))
            except ValueError:
                latitude_array.append(0)
                longitude_array.append(0)
    if 'WB_1057_SUSTAINABLE_FOREST_MANAGEMENT' in row[3].split(";"):
        print 'Number %d has an article on sustainable forest management' %i
        tone_array.append([float((row[7].split(","))[0]),float((row[7].split(","))[3])])

        if row[5].split(";") not in actor_array:
            actor_array.append(row[5].split(";"))

        if row[6].split(";") not in organization_array:
            organization_array.append(row[6].split(";"))

        for entry in row[4].split(";"):
            try:
                latitude_array.append(float((entry.split("#"))[4]))
                longitude_array.append(float((entry.split("#"))[5]))
            except ValueError:
                latitude_array.append(0)
                longitude_array.append(0)
# tone = []
# polarity = []
# for i in range(len(tone_array)):
#     tone.append(tone_array[i][0])
# for i in range(len(tone_array)):
#     polarity.append(tone_array[i][1])
#
# # print sum(tone)/len(tone)
# # print median(tone)
# #
# # print sum(polarity)/len(polarity)
# # print median(polarity)


with open(date + '.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    number_of_columns = len(latitude_array)
    column_array = range(number_of_columns)
    for i in column_array:
        text = latitude_array[i],longitude_array[i]
        writer.writerow(text)

with open(date + 'ToneAndPolarity' + '.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    number_of_columns = len(tone_array)
    column_array = range(number_of_columns)
    for i in column_array:
        text = tone_array[i][0],tone_array[i][1]
        writer.writerow(text)

with open(date + "Actors" + ".csv", 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    number_of_columns = len(actor_array)
    column_array = range(number_of_columns)
    for i in column_array:
        text = actor_array[i],''
        writer.writerow(text)
