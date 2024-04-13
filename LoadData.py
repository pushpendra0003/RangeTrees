import csv

with open("Data.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=",")
    readCSV = list(readCSV)
    print(readCSV)
    
    