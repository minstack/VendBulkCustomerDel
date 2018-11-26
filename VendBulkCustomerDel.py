import csv
from VendApi import *
from collections import defaultdict
from VendBulkCustomerDelGUI import *
import re

gui = None
api = None

def getColumn(csvFile, colName):
    columns = defaultdict(list) # each value in each column is appended to a list

    with open(csvFile) as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k
    return columns[colName]

def startProcess():
    if not gui.entriesHaveValues():
        ## error
        gui.setStatus("Please check values for prefix, token and CSV...")
        return

    if not gui.isChecklistReady():
        gui.setStatus("Please make sure checklist is completed...")
        return

    pattern = re.compile("^.+[.]csv$", re.IGNORECASE)
    if pattern.match(gui.csvFilePath) is None:
        gui.setStatus("Please make sure the selected file is .csv file...")
        return


    api = VendApi(gui.txtPrefix.get(), gui.txtToken.get())

    processCustomers(api)

    #print(api.getCustomers())

def processCustomers(api):
    gui.setStatus("Retreiving customers...")
    customers = api.getCustomers()

    if customers is None:
        gui.setStatus("Please double check that prefix/token are correct...")
        return

    gui.setStatus("Retreived {0} customers...".format(len(customers)))

    gui.setStatus("Matching IDs to provided customer code...")
    codeToId = getCustCodeToId(customers)

    custCodeToDelete = getColumn(gui.csvFilePath, 'customer_code')
    numCustToDelete = len(custCodeToDelete)
    if  numCustToDelete == 0:
        gui.setStatus("Please make sure the provided CSV has customer_code column...")
        return

    gui.setStatus("Found {0} to delete...".format(numCustToDelete))

    result = deleteCustomers(custCodeToDelete, codeToId, numCustToDelete)



def deleteCustomers(custCodeToDelete, codeToId, totalCust):
    resultDict = {
        200: [],
        500: []
    }

    i = 1
    for code in custCodeToDelete:

        response = api.deleteCustomer(codeToId[code])
        resultDict[response].append(code)
        gui.setStatus("Deleting customer {0} out of {1}".format(i, totalCust))

        i = len(resultDict[200]) #only counts successful deletes

    gui.setStatus("Successfully delete {0} customers...".format(i))

    return resultDict

def getCustCodeToId(customers):
    codeToId = {}

    for cust in customers:
        codeToId[cust['customer_code']] = cust['id']

    return codeToId

if __name__ == "__main__":

    gui = VendBulkCustomerDelGUI(startProcess)

    gui.main()
