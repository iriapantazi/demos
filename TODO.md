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
- what validation to include in associateStatusColor ?
- In the tests do I have to test individually every Exception that can be raised?
- why './tests/test_trainsLinesStatus.py' does not work, while pytest works
- cannot import modules error has to do sth w/ __init__ and directories?
- How can I test the argument parser?

- fix requirements.txt and requirements-dev.txt. 
  Create new env and start from scratch. 

- implement cli argument to control logging level.

- since we use getattr, could you showcase the use of hasattr() and
  setattr()? Also, we do not error check where we call getattr.


# Iria Done
---

- fixed name conventions 

- the code uses hardcoded values. can we make it configurable? [NOT DONE]
  LEONIDAS: afto to 300 ekei den einai [iria DONE] 

- Replaced str.format() with f-strings

- How can I print the parser help when user parses invalid arguments?

- writeAndSaveData(): can we split it up in more functions? 
  it should make things more easily tested.

- time diffing is complicated. 
  Can we simplify all the logic (unix timestamps)? [OK]
  - compareTime: no input validation, no exception handling. [OK]
  - checkLastTimeExecutedRequests: wrong documentation. [OK]
  - getDateTimeFormatted: too elaborate. [OK]


# Iria tasks (by Leonidas)
## Primary

- read the documentation of setuptools.py. 
  what does find_packages() do inside my setup.py?
  - Setuptools is used by python developers when they want
    to release a package on PyPI, which is the main repository
    for python packages, as well as python interpreters. 
    When using the 'pip install' command, packages from PyPI
    are installed on one's computer.
    The module setup() contains information about building 
    (and installing) a package, as well as metadata regarding the 
    developer(s), maintainers, mailing lists, etc.

## Secondary
- write a small paragraph why logging is preferable to print statements. [OK]
  - Logging has 5 levels of information that can be stored in a separate file.
    It is also preferred, because these additional information 
    are kept in a file rather than creating a fuss in the standard output.
    Logging levels are 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'CRITICAL' 
    in hierarchical order from least to most important.
    The developer can also define additional logging levels, but is is not 
    recommended, since it may create a clash when modules of third parties
    are used. By default, the messages logged are the ones with level 
    warning and above, but the logging module can be configured to include
    lower levels.







