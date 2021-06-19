# Shift Calculator
Given a set of entities with constraints, calculate a schedule of shifts for them that maximally respects those constraints.

## Usage
Ensure that your computer has Python installed by running `python --version` on the command line.

If it does not, you can download Python here: https://www.python.org/downloads

Download the calculateShifts.py file from [Releases](https://github.com/willowv/shift-calculator/releases) (you may also find sampleEntities.csv useful).

This program is run from the command line. It takes an input file and records the generated schedule in an output file. The following arguments are required:
- Entities filename (e.g. foo.csv) - this is your input file, see the requirements below for what it should look like.
- Start date (YYYY-MM-DD)
- Number of weeks
- Days with shifts, using lowercase, shortened day names separated with semi-colons (e.g. fri;sat;sun)
- Minimum number of days between shifts

For example:
```
python calculateShifts.py boats.csv 2021-08-01 10 fri;sat;sun 6
```

### Entities File Requirements
The Entities file should be a comma-separated values (CSV) file with the following columns:
- Name
- Group - not currently used by the program, but will be included in the output in case you want to see how different groups are distributed in the schedule.
- Days Unavailable - specify which days of the week this entity is unavailable using lowercase, shortened day names separated with semi-colons (e.g. fri;sat;sun).

See sampleEntities.csv for an example!

## Output
The program will output an output.csv file with the following columns:
- Date
- Day of the week
- Group
- Name

The schedule will attempt to minimize constraint violations but since these constraints can come into conflict the schedule will not be perfect. We recommend allowing substitutions if you use this schedule directly.

Additionally, the program will print some debug output to the console. For each entity, it will share the nunmber of times their constraints were compromised, and the distribution of their shifts across the different days.

## Implementation Plan
Below are some details about how the program works, if you are interested.

### Constraints
This program does not ensure that all constraints are perfectly met, as that would require the inputs to be completely non-contradictory. Instead, it prioritizes the provided types of constraints and attempts to minimize and evenly distribute violations of those constraints across the scheduled entities.

In order of priority:
1. Days Unavailable - An entity should never be scheduled for a day that it is not available.
1. Shift distribution - Make sure that all entities have roughly equal numbers of shifts over the entire period.
1. Minimum number of days between shifts - Attempt to respect the minimum amount of time between shifts.
1. Day distribution - Try to ensure that each entity has shifts across a variety of the days they are available.

### Pseudocode
1. Generate the list of all shifts.
1. Initially sort entities from most to least day restrictions.
1. For each entity that is not "Done":
   1. Look for next ideal shift.
   1. If it's unoccupied, take it.
   1. If it's occupied, relax a restriction and look for a new ideal shift. Increment this entity's compromise count by 1.
   1. If we're on the last restriction (Days Available), skip this entity and mark it as "Done" rather than violating that restriction.
1. Check if there are still shifts unassigned AND entities that are not "Done".
    - If so, sort entities by number of compromises from most to least, and then loop through them again. This ensures that entities that have compromised the most get first pick each round.
1. Output the schedule to output.csv.

Required data structures:
- List of shifts with date, day, and assigned entity
- List of entities with name, group, days unavailable, number of compromises, and done marker
