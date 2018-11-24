import VendApi as api
import Tkinter as tk
import csv
from collections import defaultdict

# will move this code to separate function if I need to pull any other columns
# most likely not
def getCustomerCodes(csv):
    columns = defaultdict(list) # each value in each column is appended to a list

    with open('vend-customers-DELETE.csv') as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k
    return columns['customer_code']


root = tk.Tk()






root.mainloop()
