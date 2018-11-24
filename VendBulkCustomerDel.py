import csv
from VendApi import *
from Tkinter import *
from collections import defaultdict
from VendBulkCustomerDelGUI import *

gui = None
api = None

def getColumn(csv, colName):
    columns = defaultdict(list) # each value in each column is appended to a list

    with open('vend-customers-DELETE.csv') as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k
    return columns[colName]

def deleteCustomers():
    api = VendApi("sungstore", "KWDZNSo67gRgSGAU3G2vT_IMDDT611m9s40eVisq")
    print(api.getCustomers())

if __name__ == "__main__":

    gui = VendBulkCustomerDelGUI(deleteCustomers)
    #root = Tk()
    #__initWidgets(root)

    gui.main()

    #root.mainloop()
