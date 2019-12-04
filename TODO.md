# what Iria has to do more

- set a default file to write the output
- assert that the file is in the same directory
- assert that even if file exists it is valid
- finish test_printFormattedData
- finish test_requestStatusFromServer
- in writeAndSaveData assemble all exceptions in one
- add validation for url (None, '', ...)
- patcher for test_createStatusURL module
- complete test_printFormattedData
- which of the two versions of test_checkLastTimeExecutedRequests looks better?
- test_returnValidModesString
- test_returnValidAllModesString
- may be some validation cases not considered by developer
- maybe use patch when needing in a test function that requires 
  a local variable from the corresponding function.
- which of two versions for writeAndSaveData to keep?
- what validation to include in associateStatusColor ?
- In the tests do I have to test individually every Exception that can be raised?
- why './tests/test_trainsLinesStatus.py' does not work, while pytest works
- cannot import modules error has to do sth w/ __init__ and directories?

#Questions to myself
- How can I test the argument parser?
- How can I print the parser help when user parses invalid arguments?

# Iria tasks (by Leonidas)
NB The ones I did are marked with [OK], otherwise with [-].

## Primary
- replace print statements with log statements. Investigate the use of the "logging" library that comes with Python. [OK]
- the code uses hardcoded values. can we make it configurable? [OK]
- time diffing is complicated. Can we simplify all the logic (unix timestamps)? [OK]
  - compareTime: no input validation, no exception handling. [OK]
  - checkLastTimeExecutedRequests: wrong documentation. [OK]
  - getDateTimeFormatted: too elaborate. [OK]


## Secondary
- write a small paragraph why logging is preferable to print statements. [-]
