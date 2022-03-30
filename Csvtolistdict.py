#Written by: Stuart Anderson
#Copyright Tobu Pengin, LLC. 2021
#Loads a comma delimited csv into a list dict.  Requires manual key setting in this source.
import csv

data = []

with open('/home/stuart/Documents/peeps.csv', newline='') as csvfile:
    d = csv.reader(csvfile, delimiter=',')
    for first_name,last_name,age,gender in d:
        data.append({'first_name':first_name,'last_name':last_name,'age':age,'gender':gender})

