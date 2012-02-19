import csv
import json

#Loads definitions and data from the JSON schema and puts it in convenient python lists and dicts
#This is primarily useful for mapping the schema into a spreadsheet with formulas, but also
#can be easily adapted to create a python class that implements the schema.
class Compdata:

  def __init__(self):
    self.header = None

  def loadJSON(self, filename):
    f=open(filename)
    j=json.load(f)
    print j['definitions']
    f.close()

    contexts=[]
    inputs=[]
    parameters=[]
    outputs=[]

    #sort each definition into the appropriate list
    for d in j['definitions']:
      print d['role']
      if d['role'] == 'context':
	contexts.append(d)
      elif d['role'] == 'input':
	inputs.append(d)
      elif d['role'] == 'parameter':
	parameters.append(d)
      elif d['role'] == 'output':
	outputs.append(d)

    #create a list describing the header, as is conventional in the first row of a spreadsheet
    self.header=[]
    for d in contexts:
      self.header.append(d['label'])
    for d in parameters:
      self.header.append(d['label'])
    for d in inputs:
      self.header.append(d['label'])
    for d in outputs:
      self.header.append(d['label'])

    print self.header

    #assumption is that there is one algorithm, but we use a dict here in case we have more in the future
    algorithm=j['algorithm']
    sides=algorithm.split('=')
    algodict={}
    algodict[sides[0].strip(' ')]='='+sides[1].strip(' ').strip(';')

    #now create lists for each row that would be in a spreadsheet
    self.rows=[]
    self.rows=[]
    for c in j['contexts']:
      row=[]
      self.rows.append(row)
      for d in contexts:
	row.append(c['values'][d['label']])
      for d in parameters:
	row.append(c['values'][d['label']])
      for d in inputs:
	row.append('') #blank, but should detect default values
      for d in outputs:
	row.append(algodict[d['label']])
      print row
