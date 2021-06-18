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

Note that the schedule may have gaps where it was not possible to place any entity.

## Implementation Plan
This program does not ensure that all constraints are perfectly met, as that would require the inputs to be completely non-contradictory. Instead, it prioritizes the provided types of constraints and attempts to minimize and evenly distribute violations of those constraints across the scheduled entities.

### Constraints
In order of priority:
1. Days Unavailable - An entity should never be scheduled for a day that it is not available.
1. Shift distribution - Make sure that all entities have roughly equal numbers of shifts over the entire period.
1. Minimum number of days between shifts - Attempt to respect the minimum amount of time between shifts.
1. Group membership - Attempt to diversify the groups of the entities that are scheduled for a given week.
1. Day distribution - Try to ensure that each entity has shifts across a variety of the days they are available.

### Pseudocode
1. Generate the list of all shifts.
1. Sort the entities in order of number of constraints.
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
