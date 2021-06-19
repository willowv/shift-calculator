import sys
import csv
from math import ceil
from datetime import date, timedelta

# Define classes
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

# Read command line arguments
if len(sys.argv) != 6:
    print("The following arguments are required: \nEntities filename, Start date (YYYY-MM-DD), Number of weeks, Days, Minimum number of days between shifts")
    exit()

# sys.argv[0] is the .py file
entitiesFile = sys.argv[1]
dateStart = date.fromisoformat(sys.argv[2])
numWeeks = int(sys.argv[3])
days = sys.argv[4].split(',')
numDaysBetweenShifts = timedelta(int(sys.argv[5]))

# Populate data structures
arrEntities = []
with open(entitiesFile) as bf:
    bfr = csv.DictReader(bf)
    for row in bfr:
        entity = Entity(row['Name'], row['Group'], days, row['Days Unavailable'].split(';'))
        arrEntities.append(entity)

arrShifts = []
numDays = numWeeks * 7
for i in range(numDays):
    shiftDate = dateStart + timedelta(i)
    shiftDay = shiftDate.strftime('%a').lower()
    if shiftDay in days:
        shift = Shift(shiftDate, shiftDay)
        arrShifts.append(shift)

numShifts = len(arrShifts)
numEntities = len(arrEntities)
shiftsPerEntity = ceil(numShifts / numEntities)
daysPerShift = ceil(numDays / shiftsPerEntity)

for entity in arrEntities:
    if not entity.done:
        shiftCandidates = []

        # Look for the next ideal shift
        def availableShift(shift):
            return shift.day not in entity.daysUnavailable and shift.assigned == None

        shiftCandidatesC = list(filter(availableShift, arrShifts))
        if len(shiftCandidatesC) == 0:
            entity.done = True
            continue

        def lateEnoughShift(shift):
            return entity.lastShift == None or shift.date - entity.lastShift > numDaysBetweenShifts

        shiftCandidatesB = list(filter(lateEnoughShift, shiftCandidatesC))
        if len(shiftCandidatesB) == 0:
            # if there's no candidates in B, use C
            shiftCandidates = shiftCandidatesC
        else:
            def soonEnoughShift(shift):
                comparisonDate = dateStart
                if not entity.lastShift == None:
                    comparisonDate = entity.lastShift

                return shift.date - comparisonDate < timedelta(daysPerShift + 2)

            shiftCandidatesA = list(filter(soonEnoughShift, shiftCandidatesB))
            if len(shiftCandidatesA) == 0:
                # if there's no candidates in A, use B
                shiftCandidates = shiftCandidatesB
            else:
                shiftCandidates = shiftCandidatesA

        
        def balanceExistingDays(shift):
            return entity.countPerDay[shift.day]
        
        shiftCandidates.sort(key=balanceExistingDays)
        shiftCandidates[0].assign(entity)

for shift in arrShifts:
    print(shift.toString())