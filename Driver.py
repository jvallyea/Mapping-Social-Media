from datetime import date, timedelta
from collections import defaultdict
import numpy as np
import csv
import sys
import os
import urllib
import zipfile
from Tkinter import Tk, Label, Button, Entry, OptionMenu, StringVar
import tkMessageBox

class GDELT_GUI:

    def __init__(self, master):
        self.master = master
        master.title('GDELT News Analysis')

        ### To create buttons and text fields

        self.id_label = Label(master, text="GDELT GKG Database")

        self.date_download = Label(master, text="DOWNLOAD GKG DATA FROM 1 DAY")

        self.date_field = Label(master, text="Please enter the day you want to download below: (YYYYMMDD)")
        self.date_entry = Entry(master)
        self.download_button = Button(master, text="Download", command=self.download)

        self.multiple_date_download = Label(master, text="DOWNLOAD GKG DATA FROM A DATE RANGE")
        self.multiple_date_field_start = Label(master, text="Please enter the day you want to start downloading from:")
        self.multiple_date_entry_start = Entry(master)
        self.multiple_date_field_end = Label(master, text="Please enter the day you wish to stop downloading at:")
        self.multiple_date_entry_end = Entry(master)
        self.multiple_download_button = Button(master, text="Download", command=self.multiple_download)

        self.analyze_field = Label(master, text="Please enter the day you would like to get geographic data for: (YYYYMMDD)")
        self.analyze_entry = Entry(master)
        self.analyze_keyword = Label(master, text="Please enter the text you would like to analyze:")
        self.keyword = StringVar()
        self.keyword.set("")
        self.keyword_entry = OptionMenu(master, self.keyword, "ENV_DEFORESTATION", "WB_1980_AGRO_FORESTRY", "WB_1057_SUSTAINABLE_FOREST_MANAGEMENT", "WATER_SECURITY", "ENV_SPECIESENDANGERED")
        self.analyze_button = Button(master, text="Analyze", command=self.get_latlong)

        self.leadership_field = Label(master, text="Analyze the leading actors in the space on a SINGLE date")
        self.leadership_entry_field = Label(master, text="Please enter the day you would like to get leadership data for: (YYYYMMDD)")
        self.leadership_entry = Entry(master)
        self.leadership_analyze = Label(master, text="Please select the text you would like to analyze:")
        self.leadership_keyword = StringVar()
        self.leadership_keyword.set("")
        self.leadership_keyword_entry = OptionMenu(master, self.leadership_keyword, "ENV_DEFORESTATION", "WB_1980_AGRO_FORESTRY", "WB_1057_SUSTAINABLE_FOREST_MANAGEMENT", "WATER_SECURITY")
        self.leadership_analyze_button = Button(master, text="Analyze", command=self.get_leadership)

        self.multiple_leadership_field = Label(master, text="Analyzing leading actors in the space on a date RANGE")
        self.multiple_leadership_field_start = Label(master, text="Please enter the day you want to start downlaoding from:")
        self.multiple_leadership_entry_start = Entry(master)
        self.multiple_leadership_field_end = Label(master, text="Please enter the day you wish to stop downloading at:")
        self.multiple_leadership_entry_end = Entry(master)
        self.multiple_leadership_analyze = Label(master, text="Please select the text you would like to analyze:")
        self.multiple_leadership_keyword = StringVar()
        self.multiple_leadership_keyword.set("")
        self.multiple_leadership_keyword_entry = OptionMenu(master, self.multiple_leadership_keyword, "ENV_DEFORESTATION", "WB_1980_AGRO_FORESTRY", "WB_1057_SUSTAINABLE_FOREST_MANAGEMENT", "WATER_SECURITY")
        self.multiple_leadership_analyze_button = Button(master, text="Analyze", command=self.get_multiple_leadership)

        ### To arrange buttons and text fields in window

        self.id_label.grid(row=0, column=0)
        self.date_field.grid(row=2, column=0)
        self.date_entry.grid(row=2, column=2)
        self.download_button.grid(row=3, column=2)
        self.multiple_date_download.grid(row=4, column=0)
        self.multiple_date_field_start.grid(row=5, column=0)
        self.multiple_date_entry_start.grid(row=5, column=2)
        self.multiple_date_field_end.grid(row=6, column=0)
        self.multiple_date_entry_end.grid(row=6, column=2)
        self.multiple_download_button.grid(row=7, column=2)
        self.analyze_field.grid(row=8, column=0)
        self.analyze_entry.grid(row=8, column=2)
        self.analyze_keyword.grid(row=9, column=0)
        self.keyword_entry.grid(row=9, column=2)
        self.analyze_button.grid(row=10, column=2)
        self.leadership_field.grid(row=11, column=0)
        self.leadership_entry_field.grid(row=12, column=0)
        self.leadership_entry.grid(row=12, column=2)
        self.leadership_analyze.grid(row=13, column=0)
        self.leadership_keyword_entry.grid(row=13, column=2)
        self.leadership_analyze_button.grid(row=14, column=2)
        self.multiple_leadership_field.grid(row=15, column=0)
        self.multiple_leadership_field_start.grid(row=16, column=0)
        self.multiple_leadership_entry_start.grid(row=16, column=2)
        self.multiple_leadership_field_end.grid(row=17, column=0)
        self.multiple_leadership_entry_end.grid(row=17, column=2)
        self.multiple_leadership_analyze.grid(row=18, column=0)
        self.multiple_leadership_keyword_entry.grid(row=18, column=2)
        self.multiple_leadership_analyze_button.grid(row=19, column=2)

    def download(self):
        date = self.date_entry.get()
        localDestination = "Datasets/" + date + ".gkg.csv.zip"
        URLpath = "http://data.gdeltproject.org/gkg/" + date + ".gkg.csv.zip"
        resultFilePath, responseHeaders = urllib.urlretrieve(URLpath, localDestination)
        zip_ref = zipfile.ZipFile(resultFilePath, 'r')
        zip_ref.extractall('Datasets')
        zip_ref.close()
        os.remove("Datasets/" + date + ".gkg.csv.zip")

    def multiple_download(self):
        start_date = self.multiple_date_entry_start.get()
        end_date = self.multiple_date_entry_end.get()
        d1 = date(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:8]))
        d2 = date(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:8]))
        delta = d2-d1
        days_to_download = [str(d1 + timedelta(days=x)) for x in range((d2-d1).days + 1)]
        days_to_download =  " ".join(days_to_download)
        dates = days_to_download.replace("-", "")
        date_array = dates.split(" ")
        for i in range(len(date_array)):
            local_date = date_array[i]
            localDestination = "Datasets/" + local_date + ".gkg.csv.zip"
            URLpath = "http://data.gdeltproject.org/gkg/" + local_date + ".gkg.csv.zip"
            resultFilePath, responseHeaders = urllib.urlretrieve(URLpath, localDestination)
            zip_ref = zipfile.ZipFile(resultFilePath, 'r')
            zip_ref.extractall('Datasets')
            zip_ref.close()
            os.remove("Datasets/" + local_date + ".gkg.csv.zip")


    def get_latlong(self):
        try:
            date = self.analyze_entry.get()
        except IOError:
            tkMessageBox.showinfo("ERROR", "The date you entered has not been downloaded yet.")
        unzipped_file = "Datasets/" + date + ".gkg.csv"
        g = open(unzipped_file)
        reader = csv.reader(g, delimiter = ",")
        data = list(reader)
        row_count = len(data)
        g.close()

        f = open(unzipped_file)
        headers = f.readline()

        latitude_array = []
        longitude_array = []

        query = self.keyword.get()
        if query == "":
            tkMessageBox.showinfo("ERROR", "You haven't entered a keyword query")
            return None
        for i in range(row_count-3):
            row = f.readline()
            row = row.split("\t")
            if query in row[3].split(";"):
                for entry in row[4].split(";"):
                    try:
                        latitude_array.append(float((entry.split("#"))[4]))
                        longitude_array.append(float((entry.split("#"))[5]))
                    except ValueError:
                        latitude_array.append(0)
                        longitude_array.append(0)

        with open("Carto Data/" + date + "_" + query + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            number_of_columns = len(latitude_array)
            column_array = range(number_of_columns)
            for i in column_array:
                text = latitude_array[i],longitude_array[i]
                writer.writerow(text)

    def get_leadership(self):
        local_date = self.leadership_entry.get()
        query = self.leadership_keyword.get()
        unzipped_file = "Datasets/" + local_date + ".gkg.csv"

        g = open(unzipped_file)
        reader = csv.reader(g, delimiter = ",")
        data = list(reader)
        row_count = len(data)
        g.close()

        f = open(unzipped_file)
        headers = f.readline()

        actor_array = []
        organization_array = []
        for i in range(row_count-3):
            row = f.readline()
            row = row.split("\t")
            if query in row[3].split(";"):
                actors = row[5].split(";")
                for actor in actors:
                    if actor not in [item[0] for item in actor_array] and actor != "":
                        actor_array.append([actor, 1])
                    else:
                        for i in range(len(actor_array)):
                            if actor == actor_array[i][0]:
                                actor_array[i][1] += 1

                organizations = row[6].split(";")
                for organization in organizations:
                    if organization not in organization_array:
                        organization_array.append(organization)


        actor_array = list(reversed(sorted(actor_array, key=lambda x:int(x[1]))))

        with open("Person Data/" + local_date + "_" + query + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            number_of_columns = len(actor_array)
            column_array = range(number_of_columns)
            for i in column_array:
                text = actor_array[i][0],actor_array[i][1]
                writer.writerow(text)

    def get_multiple_leadership(self):
        start_date = self.multiple_leadership_entry_start.get()
        end_date = self.multiple_leadership_entry_end.get()
        query = self.multiple_leadership_keyword.get()
        d1 = date(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:8]))
        d2 = date(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:8]))
        delta = d2-d1
        days_to_analyze = [str(d1 + timedelta(days=x)) for x in range((d2-d1).days + 1)]
        days_to_analyze = " ".join(days_to_analyze)
        dates = days_to_analyze.replace("-","")
        date_array = dates.split(" ")
        actor_array = []
        csv.field_size_limit(sys.maxsize)
        for i in range(len(date_array)):
            local_date = date_array[i]
            unzipped_file = "Datasets/" + local_date + ".gkg.csv"

            g = open(unzipped_file)
            reader = csv.reader(g, delimiter = ",")
            data = list(reader)
            row_count = len(data)
            g.close()

            f = open(unzipped_file)
            headers = f.readline()

            for i in range(row_count-3):
                row = f.readline()
                row = row.split("\t")
                if query in row[3].split(";"):
                    actors = row[5].split(";")
                    for actor in actors:
                        if actor not in [item[0] for item in actor_array] and actor != "":
                            actor_array.append([actor, 1])
                        else:
                            for i in range(len(actor_array)):
                                if actor == actor_array[i][0]:
                                    actor_array[i][1] += 1
        actor_array = list(reversed(sorted(actor_array, key=lambda x:int(x[1]))))

        with open("Person Data/" + start_date + "-" + end_date + "_" + query + ".csv", 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            column_array = range(len(actor_array))
            for i in column_array:
                text = actor_array[i][0],actor_array[i][1]
                writer.writerow(text)

root = Tk()
gui = GDELT_GUI(root)
root.mainloop()
