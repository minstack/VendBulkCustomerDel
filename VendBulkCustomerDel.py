import csv
from VendApi import *
from collections import defaultdict
from VendBulkCustomerDelGUI import *
import re
import datetime as dt
from os.path import expanduser
import threading
import Queue

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
        gui.setReadyState()
        return

    if not gui.isChecklistReady():
        gui.setStatus("Please make sure checklist is completed...")
        gui.setReadyState()
        return

    pattern = re.compile("^.+[.]csv$", re.IGNORECASE)

    for file in gui.csvList:
        if pattern.match(file) is None:
            gui.setStatus("Please make sure the selected files are .csv file...")
            gui.setReadyState()
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
        gui.setReadyState()
        return

    gui.setStatus("Retreived {0} customers...".format(len(customers)))

    gui.setStatus("Matching IDs to provided customer code...")
    codeToId = getCustCodeToId(customers)

    custCodeToDelete = []
    for file in gui.csvList:
        filepath = gui.csvFileDict[file]
        custCodeToDelete.extend(getColumn(filepath, 'customer_code'))

    numCustToDelete = len(custCodeToDelete)
    if  numCustToDelete == 0:
        gui.setStatus("Please make sure the provided CSV has customer_code column...")
        gui.setReadyState()
        return

    gui.setStatus("Found {0} customers to delete...".format(numCustToDelete))

    #probably a better way for this but straight forward without much thinking
    #range = numCustToDelete//4
    #subArrs = []
    #subArrs.append(custCodeToDelete[:range])
    #subArrs.append(custCodeToDelete[range:(2*range)])
    #subArrs.append(custCodeToDelete[(2*range):(3*range)])
    #subArrs.append(custCodeToDelete[(3*range):])

    subArrs = getSubLists(custCodeToDelete, 8)

    print(len(subArrs))
    #time.sleep(60)

    outQueue = Queue.Queue()
    threads = []
    for subarr in subArrs:
        tempThread = threading.Thread(target=deleteCustomers, args=(subarr,codeToId,numCustToDelete, api,outQueue,))
        threads.append(tempThread)
        tempThread.start()
        

    for thread in threads:
        thread.join()

    results = []
    result ={
        204: [],
        500: [],
        404: []
    }

    for thread in threads:
        results.append(outQueue.get())

    status_codes = [204,500,404]

    for r in results:
        result[status_codes[0]].extend(r[status_codes[0]])
        result[status_codes[1]].extend(r[status_codes[1]])
        result[status_codes[2]].extend(r[status_codes[2]])

    gui.setStatus("Successfully deleted {0} customers...".format(len(result[204])))

    resultCsv = None

    if len(result[500]) > 0:
        resultCsv = processFailedCustomers(result[500], codeToId)

    setResultMessage(result, resultCsv)

def getSubLists(arr, numSubs):
    range = len(arr)//numSubs
    subArrs = []

    i = 0
    while i < (numSubs-1):
        start = i * range
        end = (i+1) * range
        subArrs.append(arr[start:end])
        i += 1

    subArrs.append(arr[(i*range):])

    return subArrs

def setResultMessage(result, resultCsv):
    failedCsv = None
    openSalesCsv = None

    if resultCsv:
        failedCsv = resultCsv.get('failedcust', None)
        openSalesCsv = resultCsv.get('opensales', None)

    successfulDeletes = len(result[204])

    msg = "{0} customers were successfully deleted.\n".format(successfulDeletes)

    if failedCsv:
        msg += "{0} could not be deleted. \nSaved {1} to desktop.\n".format(len(result[500]), failedCsv)

    if openSalesCsv:
        msg += "Saved {0} to desktop.".format(openSalesCsv)

    gui.setResult(msg)
    gui.btnReset.config(state=NORMAL)
    #print(msg)

    #reset gui, status etc.

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

    return filenames

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
    return writeListToCSV(salesList, "invoice_number", "open_sales")

def writeListToCSV(list, colHeader, title):
    #generic list to csv function
    if colHeader:
        list.insert(0, colHeader)

    filename = api.getPrefix() + dt.datetime.now().strftime("%Y-%m-%dT%H:%M") + title + ".csv"

    gui.setStatus("Writing {0}...".format(filename))

    desktop = expanduser("~") + '/' + 'Desktop/'

    with open(desktop + filename, "wb") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in list:
            writer.writerow([row])

    gui.setStatus("Write {0} completed...".format(filename))

    return filename

def deleteCustomers(custCodeToDelete, codeToId, totalCust, api, outQueue=None):
    #global resultDict

    resultDict = {
        500: [],
        404: [],
        204: []
    }

    global deletedCust
    deletedCust = 0
    #print(codeToId)
    for code in custCodeToDelete:
        codeToDel = codeToId.get(str(code), None)
        if codeToDel is None:
            continue

        response = api.deleteCustomer(codeToDel)
        #print(response)
        resultDict[response].append(code)
        gui.setStatus("Deleting customer {0} out of {1}".format(deletedCust, totalCust))

        if response == 204:
            deletedCust += 1 #only count successful deletes

    #gui.setStatus("Successfully deleted {0} customers...".format())
    if outQueue:
        outQueue.put(resultDict)
        return
    #print(resultDict)
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
