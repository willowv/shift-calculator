# Shift Calculator
Given a set of entities with constraints, calculate a schedule of shifts for them that maximally respects those constraints.

## Usage
The following arguments are required:
- Entities filename (e.g. foo.csv)
- Start date (YYYY-MM-DD)
- Number of weeks
- Days with shifts (e.g. fri,sat,sun)
- Minimum number of days between shifts

### Entities File Requirements
The Entities file should be a comma-separated values (CSV) file with the following columns:
- Name
- Group - the program will attempt to avoid using members of just one group in a given week.
- Days Unavailable - specify which days of the week this entity is unavailable.

## Output
The program will output an output.csv file with the following columns:
- Date
- Day of the week
- Group
- Name

## Basic Plan
This program does not ensure that all constraints are perfectly met, as that would require the inputs to be completely non-contradictory. Instead, it prioritizes the provided types of constraints and attempts to minimize and evenly distribute violations of those constraints across the scheduled entities.

### Constraints
In order of priority:
1. Days Unavailable - An entity should never be scheduled for a day that it is not available.
1. Even distribution - Make sure that all entities have roughly equal numbers of shifts over the entire period.
1. Minimum number of weeks between shifts - Attempt to respect the minimum amount of time between shifts.
1. Group membership - Attempt to diversify the groups of the entities that are scheduled for a given week.