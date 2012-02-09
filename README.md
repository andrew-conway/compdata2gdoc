compdata2gdoc
=============

This code takes a file of data and a definition and turns it into a gdoc spreadsheet with formulas.

You need to have http://code.google.com/p/gdata-python-client/ available. Full instructions for
installing using and testing are here: http://code.google.com/apis/gdata/articles/python_client_lib.html

Usage
-----

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

algoread
========

algoread is a script which will extract a much simpler and de-amee-ified algo from an AMEE algo.

It's tested on some real AMEE algos but cannot yet handle dataFinders or MARV or some of
the more involved algos with complex structures, e.g. stationary combustion.

Usage
-----
The start of the code will need to be editted to specify data item and profile item values.

./algoread.py algo-file

There's a lot of messy output at the moment, but the final line will be a simple, one line summary of the calculation performed by the algo.
