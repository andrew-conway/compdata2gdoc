compdata2gdoc
=============

This code takes a file of data and a definition and turns it into a gdoc spreadsheet with formulas.

You need to have http://code.google.com/p/gdata-python-client/ available. Full instructions for
installing using and testing are here: http://code.google.com/apis/gdata/articles/python_client_lib.html

Usage:

./deserialise2gdoc.py --user username -pw password

Note: at present it will find the first spreadsheet in your google account and start overwriting it, so best create a new one or better still use it on a google account you don't rely on for anything else!

To do:
* option to create or specify existing spreadsheet
* implement against AMEE
* implement against AB's gravity example schema
Later:
* remove 26 column limitation on spreadsheets

Idea:
Four types data to help specify the computation (like cols in a spreadsheet)
* choices: values that describe each row (like drilldowns), e.g. manufacturer and model of car
* parameters: this has a given value (like a data item value), e.g. kgCO2/km
* inputs: this can be set by the user (like a profile item value), e.g. distance
* outputs: this is a value computed by a formula from arithmetic operations on data, user and possibly other algos

By chaining algos together a series of steps in an operation can be set out. As viewed in spreadsheet this is just series of columns with formulas.

Parsing AMEE algorithms:
1. Pick a usage
2. Identify required profile item values
3. grep the algo for those PIV names => PIV_lines
4. find the last line where a required PIV is mentioned
5. if this does not contain an = sign it is a return value, if not skip to step 7
6. determine what PIV and DIVs are mentioned, if no other variables appear, we're done, otherwise continue...
7. for each mentioned unidentified variable, search back through the algorithm for it on the LHS of an = sign and repeat recursively until no unidentified variables are left
