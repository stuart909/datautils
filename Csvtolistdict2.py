
#Written by: Stuart Anderson
#Copyright Tobu Pengin, LLC. 2021
#Loads CSV with first row key headers into a list of dicts
import csv

data = []
path = "/path_here/file"

with open(path, newline='') as csvfile:
    d = csv.reader(csvfile, delimiter=',')
    for n,row in enumerate(d):
        if n == 0:
            keys = [k for k in row]
        else:
            tmp = {}
            for v in row:
                tmp.update({keys[row.index(v)]:v})
            data.append(tmp)


    

