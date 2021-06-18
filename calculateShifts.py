import sys
import csv
from datetime import date

class Entity:
    def __init__(self, name, group, days, daysUnavailable):
        self.name = name
        self.group = group
        self.daysUnavailable = daysUnavailable
        self.numCompromises = 0
        self.done = False
        self.lastShift = None
        self.countPerDay = {}
        for day in days:
            self.countPerDay[day] = 0
    def isAvailable(self, day):
        return day in self.daysUnavailable
    def assigned(self, date, day):
        self.lastShift = date
        self.countPerDay[day] += 1

class Shift:
    def __init__(self, date, day):
        self.date = date
        self.day = day
        self.assigned = None
    def assign(self, entity):
        self.assigned = entity
        entity.assigned(self.date, self.day)
    def toString(self):
        if self.assigned == None:
            return "{0},{1},,".format(self.date, self.day)
        else:
            return "{0},{1},{2},{3}".format(self.date, self.day, self.assigned.group, self.assigned.name)

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
        print(row['Name'], row['Group'], row['Days Unavailable'])