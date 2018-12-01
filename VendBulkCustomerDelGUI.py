from Tkinter import *
import threading
from tkFileDialog import askopenfilename

class VendBulkCustomerDelGUI:

    def __init__(self, deletefunc):
        self.__deletefunc = deletefunc
        self.root = Tk()
        self.root.geometry("650x450")
        self.root.resizable(0,0)
        self.root.title("Vend Bulk Customer Delete")
        self.root.pack_propagate(0)
        header = Label(self.root, text="Bulk Customer Delete", bd=1, font="Helvetica 18 bold", bg="#41B04B", fg="white")
        header.pack(side=TOP, anchor=W, fill=X)

        # container for the main widgets
        mainFrame = Frame(self.root)
        mainFrame.pack(padx=20, pady=10)

        self.__loadUserInputs__(mainFrame)
        self.__loadButtons__(mainFrame)
        self.__loadCsvControl__(mainFrame)
        self.__loadCheckListControl__(mainFrame)
        self.__loadMessageControls__(mainFrame)

    def __loadUserInputs__(self, mainFrame):
        lblStorePrefix = Label(mainFrame, text="Store Prefix:", font="Helvetica 14 bold")
        lblStorePrefix.grid(row=1, column=0, sticky=E)

        lblToken = Label(mainFrame, text="Token:", font="Helvetica 14 bold")
        lblToken.grid(row=2, column=0, sticky=E)

        lblCsv = Label(mainFrame, text="CSV File:", font="Helvetica 14 bold")
        #lblCsv.grid(row=3, column=0, sticky=E)

        #textboxes
        self.txtPrefix = Entry(mainFrame)
        self.txtToken = Entry(mainFrame)
        self.txtPrefix.grid(row=1,column=1, sticky=W)
        self.txtToken.grid(row=2,column=1, sticky=W)

        csvframe = Frame(mainFrame)
        self.txtCsv = Entry(csvframe)

        #self.txtCsv.pack(side=LEFT)
        #self.btnOpenCsvDialog.pack()
        #csvframe.grid(row=3,column=1, sticky=W)

    def __loadButtons__(self, mainFrame):
        btnframe = Frame(mainFrame)
        self.btnDelCust = Button(btnframe, text="Delete Customers", command=self.startThread)
        self.btnDelCust.pack(side=RIGHT)
        self.btnReset = Button(btnframe, text="Reset", command=self.reset)
        self.btnReset.pack()
        btnframe.grid(row=4, column=1)

    def __loadCsvControl__(self, mainFrame):
        self.csvList = []
        self.csvFileDict = {}
        self.csvListbox = Listbox(mainFrame, listvariable=self.csvList, width=25, bd=0.5, selectmode='single')


        #csvHeader.grid(row=0, column=2)
        self.csvListbox.grid(row=1, column=2, rowspan=3)

        csvFrame = Frame(mainFrame)

        csvHeader = Label(csvFrame, text="CSV Files", font="Helvetica 14 bold")
        csvHeader.pack(side=LEFT)

        csvFrame.grid(row=4, column=2, sticky=E)
        self.btnOpenCsvDialog = Button(csvFrame, text="+", font="Helvetica 14 bold", command=self.openFile)
        self.btnOpenCsvDialog.pack(side=LEFT)
        self.btnDeleteFile = Button(csvFrame, text="-", font="Helvetica 14 bold", command=self.deleteFileFromList)
        self.btnDeleteFile.pack()

    def __loadCheckListControl__(self, mainFrame):
        checklistFrame = Frame(mainFrame, width=200, height=200, bd=1)
        #Label(mainFrame, text="Checklist", font="Helvetica 14 bold").grid(row=0, column=3)
        checklistFrame.grid(row=3, column=1)

        self.paConfirmation = BooleanVar()
        self.tokenExpiry = BooleanVar()
        self.chkPaConfirm = Checkbutton(checklistFrame, text="PA Confirmation", variable=self.paConfirmation)
        self.chkPaConfirm.grid(row=1, sticky=W)
        self.chkTokenExpiry = Checkbutton(checklistFrame, text="Token Expiry Set", variable=self.tokenExpiry)
        self.chkTokenExpiry.grid(row=2, sticky=W)

    def __loadMessageControls__(self, mainFrame):
        self.statusMsg = StringVar()
        self.lblStatus = Label(self.root, textvariable=self.statusMsg, bd=1, relief=SUNKEN, anchor=W, bg="#41B04B", fg="white", font="Helvetica 14 italic")
        self.lblStatus.pack(side=BOTTOM, fill=X)

        resultFrame = Frame(mainFrame)
        resultFrame.grid(row=5,column=0, columnspan=3, rowspan=4)

        self.resultText = StringVar()
        resultLabel = Message(resultFrame, textvariable=self.resultText,font="Helvetica 16", width=500)
        resultLabel.pack(pady=15)

    def reset(self):
        self.setStatus("")
        self.setReadyState()
        self.txtToken.delete(0,END)
        self.txtPrefix.delete(0,END)
        self.paConfirmation.set(0)
        self.tokenExpiry.set(0)
        del self.csvList[:]
        self.csvListbox.delete(0,END)
        self.csvFileDict = {}
        self.setResult("")

    def deleteFileFromList(self):
        selected = self.csvListbox.curselection()

        if not selected:
            return

        self.csvListbox.delete(selected[0])
        self.csvFileDict.pop(self.csvList[selected[0]], None)
        del self.csvList[selected[0]]

    def entriesHaveValues(self):
        return (len(self.txtPrefix.get().strip()) > 0) and (len(self.txtToken.get().strip()) > 0) and (len(self.csvList) > 0)

    def startThread(self):
        self.setStatus("")
        self.setDeletingState()
        thr = threading.Thread(target=self.__deletefunc, args=(), kwargs={})

        thr.start()
        #self.setReadyState()

    def isChecklistReady(self):
        return self.tokenExpiry.get() and self.paConfirmation.get()

    def openFile(self):
        #self.txtCsv.delete(0,END)
        filepath = askopenfilename(parent=self.root)
        tempArr = filepath.split("/")

        filename = tempArr[len(tempArr)-1]

        if self.csvFileDict.get(filename, None) is not None:
            self.setStatus("{0} has been added already.".format(filename))
            return

        self.csvFileDict[filename] = filepath
        self.csvList.append(filename)

        self.csvListbox.insert(END, filename)


    def setStatus(self, msg):
        self.statusMsg.set(msg)

    def setResult(self, msg):
        self.resultText.set(msg)

    def setDeletingState(self):
        self.btnReset.config(state=DISABLED)
        self.btnDelCust.config(state=DISABLED)
        self.btnOpenCsvDialog.config(state=DISABLED)
        self.btnDeleteFile.config(state=DISABLED)
        self.txtToken.config(state=DISABLED)
        self.txtPrefix.config(state=DISABLED)
        self.chkPaConfirm.config(state=DISABLED)
        self.chkTokenExpiry.config(state=DISABLED)
        self.root.update()

    def setReadyState(self):
        self.btnReset.config(state=NORMAL)
        self.btnDelCust.config(state=NORMAL)
        self.btnOpenCsvDialog.config(state=NORMAL)
        self.btnDeleteFile.config(state=NORMAL)
        self.txtToken.config(state=NORMAL)
        self.txtPrefix.config(state=NORMAL)
        self.chkPaConfirm.config(state=NORMAL)
        self.chkTokenExpiry.config(state=NORMAL)
        self.root.update()

    def main(self):
        self.root.mainloop()
