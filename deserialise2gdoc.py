#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Copyright (C) 2011 AMEE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = ('andrew@amee.com (Andrew Conway)')

try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string
import csv
import compdata

class SimpleCRUD:

  def __init__(self, email, password):
    self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'Spreadsheets GData Sample'
    self.gd_client.ProgrammaticLogin()
    self.curr_key = ''
    self.curr_wksht_id = ''
    self.compdata = compdata.Compdata();
    feed = self.gd_client.GetSpreadsheetsFeed()
    self._PrintFeed(feed)
    id_parts = feed.entry[0].id.text.split('/')
    self.curr_key = id_parts[len(id_parts) - 1]
    # Get the list of worksheets, select the first one for now
    feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
    self._PrintFeed(feed)
    id_parts = feed.entry[0].id.text.split('/')
    self.curr_wksht_id = id_parts[len(id_parts) - 1]

  def _CellsGetAction(self):
    # Get the feed of cells
    feed = self.gd_client.GetCellsFeed(self.curr_key, self.curr_wksht_id)
    self._PrintFeed(feed)

  def _CellsUpdateAction(self, row, col, inputValue):
    entry = self.gd_client.UpdateCell(row=row, col=col, inputValue=inputValue, 
        key=self.curr_key, wksht_id=self.curr_wksht_id)
    if isinstance(entry, gdata.spreadsheet.SpreadsheetsCell):
      print 'Updated!'

  def _PrintFeed(self, feed):
    for i, entry in enumerate(feed.entry):
      if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
        print '%s %s\n' % (entry.title.text, entry.content.text)
      elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        print '%s %s %s' % (i, entry.title.text, entry.content.text)
        # Print this row's value for each column (the custom dictionary is
        # built using the gsx: elements in the entry.)
        print 'Contents:'
        for key in entry.custom:  
          print '  %s: %s' % (key, entry.custom[key].text) 
        print '\n',
      else:
        print '%s %s\n' % (i, entry.title.text)

  #this is slow, need to batch it up with lists!
  def _PutData(self):
    ic=1
    for item in self.compdata.header:
	self._CellsUpdateAction(1, ic, item)
	ic=ic+1
    
    ir=2
    for row in self.compdata.rows:
      for ic in range(1,self.compdata.data_col):
	self._CellsUpdateAction(ir, ic, row[ic-1])
      #insert user and algorithm column
      self._CellsUpdateAction(ir, self.compdata.data_col+1, self.compdata.user_value)
      self._CellsUpdateAction(ir, self.compdata.data_col+2, self._GetFormula(ir,self.compdata.data_col,self.compdata.data_col+1))	
      ir=ir+1  
    
  def _GetFormula(self, row, data_col, user_col):
    formula='='+string.uppercase[data_col-1]
    formula+=str(row)
    formula+='*'
    formula+=string.uppercase[user_col-1]
    formula+=str(row)
    return formula

  def Run(self):
    #self._GetFormula(2,3,4)
    self.compdata.loadDef('cars_def.csv')    
    self.compdata.loadData('cars.csv')
    self._PutData()
    #self._CellsGetAction()


def main():
  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw="])
  except getopt.error, msg:
    print 'python deserialise2gdoc.py --user [username] --pw [password] '
    sys.exit(2)
  
  user = ''
  pw = ''
  key = ''
  # Process options
  for o, a in opts:
    if o == "--user":
      user = a
    elif o == "--pw":
      pw = a

  if user == '' or pw == '':
    print 'python deserialise2gdoc.py --user [username] --pw [password] '
    sys.exit(2)
        
  sample = SimpleCRUD(user, pw)
  sample.Run()



if __name__ == '__main__':
  main()