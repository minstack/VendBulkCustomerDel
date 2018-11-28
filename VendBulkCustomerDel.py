import csv
from VendApi import *
from collections import defaultdict
from VendBulkCustomerDelGUI import *
import re
import datetime as dt

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


    global api
    api = VendApi(gui.txtPrefix.get(), gui.txtToken.get())

    processCustomers(api)

    #print(api.getCustomers())

def processCustomers(api):
    gui.setStatus("Retreiving customers...")
    customers = api.getCustomers()

    if customers is None or len(customers) == 0:
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

    gui.setStatus("Found {0} customers to delete...".format(numCustToDelete))

    result = deleteCustomers(custCodeToDelete, codeToId, numCustToDelete, api)
    resultCsv = None

    if len(result[500]) > 0:
        resultCsv = processFailedCustomers(result[500], codeToId)


    setResultMessage(result, resultCsv)

def setResultMessage(result, resultCsv):
    failedCsv = None
    openSalesCsv = None

    if resultCsv:
        failedCsv = resultCsv.get('failedcust', None)
        openSalesCsv = resultCsv.get('opensales', None)

    successfulDeletes = len(result[204])

    msg = "{0} customers were successfully deleted.\n".format(successfulDeletes)

    if failedCsv:
        msg += "{0} could not be deleted. Exported list to {1}\n".format(len(result[500]), failedCsv)

    if openSalesCsv:
        msg += "Exported open sales linked to customers to {0}".format(openSalesCsv)

    gui.setResult(msg)

def processFailedCustomers(failedCustomers, codeToId):
    filenames = {}

    filenames['failedcust'] = writeCustomersToCSV(failedCustomers)

    gui.setStatus("Retreiving open sales...")
    openSales = api.getOpenSales()

    #print(openSales)
    #print('after get open sales')
    # filter opensales based on customers to delete
    failedCustomers.remove('customer_code')
    matchedOpenSales = getOpenSaleMatch(failedCustomers, codeToId, openSales)

    filenames['opensales'] = writeOpenSalesToCsv(matchedOpenSales)

def getOpenSaleMatch(custList, codeToId, salesList):

    tempReverse = {}
    # id to code to linearly check if sale is attached to customer
    # trying to be deleted
    for code in custList:
        id = codeToId[code]
        tempReverse[id] = code

    saleInvoices = []
    for sale in salesList:
         custCode = tempReverse.get(sale['customer_id'], None)

         if custCode is None:
             continue

         saleInvoices.append(sale['invoice_number'])

    return saleInvoices


def writeCustomersToCSV(custList):
    return writeListToCSV(custList, "customer_code", "failed_customers")

def writeOpenSalesToCsv(salesList):
    return writeListToCSV(salesList, "invoice_number", "open_sales_to_delete")

def writeListToCSV(list, colHeader, title):
    #generic list to csv function
    if colHeader:
        list.insert(0, colHeader)

    filename = api.getPrefix() + dt.datetime.now().strftime("%Y-%m-%dT%H:%M") + title + ".csv"

    gui.setStatus("Writing {0}...".format(filename))

    with open("./" + filename, "wb") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in list:
            writer.writerow([row])

    gui.setStatus("Write {0} completed...".format(filename))

    return filename

def deleteCustomers(custCodeToDelete, codeToId, totalCust, api):
    resultDict = {
        500: [],
        404: [],
        204: []
    }

    i = 0
    print(codeToId)
    for code in custCodeToDelete:
        codeToDel = codeToId.get(str(code), None)
        if codeToDel is None:
            continue

        response = api.deleteCustomer(codeToDel)
        #print(response)
        resultDict[response].append(code)
        gui.setStatus("Deleting customer {0} out of {1}".format(i, totalCust))

        i = len(resultDict[204]) #only count successful deletes

    gui.setStatus("Successfully deleted {0} customers...".format(i))

    print(resultDict)
    return resultDict

def getCustCodeToId(customers):
    codeToId = {}

    for cust in customers:
        #print(cust['customer_code'])
        codeToId[str(cust['customer_code']).lstrip("0")] = cust['id']

    return codeToId

if __name__ == "__main__":

    gui = VendBulkCustomerDelGUI(startProcess)

    gui.main()
