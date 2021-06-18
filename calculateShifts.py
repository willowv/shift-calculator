import sys
import csv
from datetime import date

if len(sys.argv) != 6:
    print("The following arguments are required: \nBoats filename, Start date (YYYY-MM-DD), Number of weekends, Patrol days, Minimum number of weeks between patrols")
    exit()

#sys.argv[0] is the .py file
boatsFile = sys.argv[1]
dateStart = date.fromisoformat(sys.argv[2])
numWeekends = sys.argv[3]
arrPatrolDays = sys.argv[4].split(',')
numWeeksBetweenShifts = sys.argv[5]

with open(boatsFile) as bf:
    bfr = csv.DictReader(bf)
    for row in bfr:
        print(row['Name'], row['Flotilla'], row['Days Unavailable'])