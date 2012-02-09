#!/usr/bin/python

import sys

#todo:
# - usages need to be read and selected externally
# - MARV needs support
# - *= style assignment needs to be handled correctly
# - if final result is obviously wrong, i.e. always zero
#   or contains null or undefined values, try alternate assignments;
#   at present, last matching assignment is just used.
# - profile or dataFinders need replacement with values

#pivs contains all profile item values that the usage dictates are
#required for the calculation.
#divs contains all data item values
pivs=['distance']
divs=['EF']
ivs=pivs
ivs.extend(divs)

#if data or profileFinders are found this stops them breaking code
#but should be handled with an AMEE lookup, or sensible default
ivs.append('FINDER')

def is_number(s):
  try:
      float(s)
      return True
  except ValueError:
      return False

#the x*=y and similar lines should be translated to
#x=x*y and treated as assignment lines - for now they are ignored :)
def is_line_assignment(line):
  return ('=' in line and not '==' in line and not '!=' in line
  and not '*=' in line and not '/=' in line and not '+=' in line
  and not '-=' in line)

#could this line be the final line in the calculation
#returnValues should be read, but for now they are ignored :)
#in python not a is true if the string is empty
def is_final(line):
  return (len(line)>0 and not '{' in line and not '}' in line and not line=='0'
  and not 'returnValues' in line and not line.find('//')==0)

#split up an arithmetic expression into a list of variables
def getVariableList(s):
  if '=' in s:
    s=s.split('=')[1]
  s=s.replace('(','')
  s=s.replace(')','')  
  s=s.replace('/','*')
  s=s.replace('+','*')
  s=s.replace('-','*')
  vv=s.split('*')
  ss=[]
  for v in vv:
    ss.append(v.strip(' ').strip('\t'))
  return ss

#take a list of variables and return that list with PIVs and DIVs removed
def removeItemValues(varList,ivs):
  unidentifiedVarList=list(varList)
  for v in varList:
    print v
    if v in ivs or is_number(v):
      unidentifiedVarList.remove(v)  
  return unidentifiedVarList

eqdict={}

file=open(sys.argv[1])
for line in file:
  line=line.strip('\n').strip(';').strip(' ').strip('\t').strip(' ')
  if is_line_assignment(line):
    ls=line.split('=')
    if 'Finder' in ls[1]:
      ls[1]='FINDER'  
    eqdict[ls[0].strip(' ')]=ls[1].strip(' ')
  if is_final(line):
    final=line
    print final

print eqdict

varList=getVariableList(final)
unidentifiedVarList=removeItemValues(varList,ivs)

while unidentifiedVarList:
  print unidentifiedVarList
  for v in unidentifiedVarList:
    final=final.replace(v,'('+eqdict[v]+')')
  varList=getVariableList(final)
  unidentifiedVarList=removeItemValues(varList,ivs)

print final
