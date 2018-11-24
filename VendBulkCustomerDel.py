import csv
from VendApi import *
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
    if (not gui.entriesHaveValues()):
        ## error
        print("in error text")
        gui.setStatus("Please check values for prefix, token and CSV...")
        return
    else:
        api = VendApi(gui.txtPrefix.get(), gui.txtToken.get())

        processCustomers(api)

        print(api.getCustomers())

def processCustomers(api):
    gui.setStatus("Retreiving customers...")
    customers = api.getCustomers()
    gui.setStatus("Retreived {0} customers...".format(len(customers)))

    gui.setStatus("Matching IDs to provided customer code...")
    codeToId = getCustCodeToId(customers)


def getCustCodeToId(customers):
    codeToId = {}

    for cust in customers:
        codeToId[cust['customer_code']] = customers['id']

    return codeToId

if __name__ == "__main__":

    gui = VendBulkCustomerDelGUI(deleteCustomers)
    #root = Tk()
    #__initWidgets(root)

    gui.main()

    #root.mainloop()
