import sys
import csv
from datetime import date, timedelta

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
    def toString(self):
        return "{0},{1},{2}".format(self.group, self.name, self.daysUnavailable)

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
    print("The following arguments are required: \Entities filename, Start date (YYYY-MM-DD), Number of weeks, Days, Minimum number of days between shifts")
    exit()

#sys.argv[0] is the .py file
entitiesFile = sys.argv[1]
dateStart = date.fromisoformat(sys.argv[2])
numWeeks = int(sys.argv[3])
days = sys.argv[4].split(',')
numDaysBetweenShifts = int(sys.argv[5])

arrEntities = []
with open(entitiesFile) as bf:
    bfr = csv.DictReader(bf)
    for row in bfr:
        entity = Entity(row['Name'], row['Group'], days, row['Days Unavailable'].split(';'))
        arrEntities.append(entity)
        print(entity.toString())

arrShifts = []
numDays = numWeeks * 7
for i in range(numDays):
    shiftDate = dateStart + timedelta(i)
    shiftDay = shiftDate.strftime('%a').lower()
    if shiftDay in days:
        shift = Shift(shiftDate, shiftDay)
        print(shift.toString())