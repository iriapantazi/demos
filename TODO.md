# Iria tasks
## Primary
- replace print statements with log statements. Investigate the use of the "logging" library that comes with Python. [OK]
- the code uses hardcoded values. can we make it configurable?
- time diffing is complicated. Can we simplify all the logic (unix timestamps)?
  - compareTime: no input validation, no exception handling.
  - checkLastTimeExecutedRequests: wrong documentation.
  - getDateTimeFormatted: too elaborate.

- get severity codes from API once and for all. hence avoid hard-coding for assigning colors.
- tox package

## Secondary
- write a small paragraph why logging is preferable to print statements.
