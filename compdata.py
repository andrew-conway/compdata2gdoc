import csv

class Compdata:

  def __init__(self):
    self.choices = None
    self.data = None
    self.user = None
    self.algo = None
    self.user_value = '10.0'
    self.header = None
    self.rows = None
    self.data_col = None
    
  def loadDef(self, filename):
    rows = csv.reader(open(filename))
    #simple-minded, one of each for now
    choices=rows.next()
    self.choices=choices
    data=rows.next()
    self.data = data[1]
    user=rows.next()
    self.user = user[1]
    algo=rows.next()
    self.algo = algo[1]
    
  #this is slow, need to batch it up with lists!
  def loadData(self, filename):
    csvdata = csv.reader(open(filename))
    self.header=csvdata.next()
    self.rows=[]
    self.data_col=self.header.index(self.data)+1
    self.header.append(self.user)
    self.header.append(self.algo)
    for row in csvdata:
      row.append(self.user_value)
      row.append(self.algo)
      self.rows.append(row)
    print self.header
    print self.rows