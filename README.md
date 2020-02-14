# **Utility for tube/tram/DLR/overground lines status**
---

This utility is a small program written in Python 
that prints information on the status of lines 
provided by the tfl API. The user can specify 
whether they need the status of all the lines 
(tube, tram, DLR and London Overground), or any 
one of them, by parsing the appropriate 
arguments when running the program. 
The output of the request is printed on the 
standard output, and saved in a file named 
`outputLinesStatus.csv`. 

## **Getting started**

### **Prerequisites**
The program is written in Python 3.6 and can run 
with Python versions 3.7 and 3.8. The program will 
exit if it is used Python 2.7.
It is suggested that the user creates a virtual environment, 
and installs the package requirements with the command 
`pip install -r requirements.txt`.

### **Running the tests**
After having installed the required packages, the user should 
run the tests by using the command  
`pytest` or `python -m unittest tests/test_trainsLinesStatus.py`. 

## **Information on input and output**

### **Example input** 
![image](img/example_output.png "Output Example")

### **Example output** 
![image](img/example_output.png "Output Example")

### **Log files**

## **Further Amendments**
There is a number of corrections/amendments that will be done 
in due time. These include:
- fix the timestamp in LOGFILE
- Option of defining logging level through an integer
- Uppercase in logging lever to be asserted or corrected by program
- Reduce hard-coded values
- PEP8 assessment
- Include tests for parser
- Merge duplicate tests and account for all exceptions
- Critical log messages that lead to system exit to be printed on stdout
- Mock logger
- Support for Python 3.4 and 3.5
- If new request with a different valid mode is performed within less than ttl seconds, 
then either do the request, or print only the requested mode(s) requested

## **Authors** 
If you have any suggestions/corrections, 
please contct [Iria Pantazi](iria.a.pantazi@gmail.com).


