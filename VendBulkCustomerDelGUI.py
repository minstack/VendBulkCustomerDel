from Tkinter import *
import threading
from tkFileDialog import askopenfilename

class VendBulkCustomerDelGUI:

    def __init__(self, deletefunc):
        self.__deletefunc = deletefunc
        self.root = Tk()
        self.root.geometry("500x350")
        self.root.resizable(0,0)
        self.root.title("Vend Bulk Customer Delete")
        self.root.pack_propagate(0)
        header = Label(self.root, text="Bulk Customer Delete", bd=1, font="Helvetica 18 bold", bg="#41B04B", fg="white")
        header.pack(side=TOP, anchor=W, fill=X)

        # container for the main widgets
        mainFrame = Frame(self.root)
        mainFrame.pack(padx=20, pady=10)

        lblStorePrefix = Label(mainFrame, text="Store Prefix:", font="Helvetica 14 bold")
        lblStorePrefix.grid(row=1, column=0, sticky=E)

        lblToken = Label(mainFrame, text="Token:", font="Helvetica 14 bold")
        lblToken.grid(row=2, column=0, sticky=E)

        lblCsv = Label(mainFrame, text="CSV File:", font="Helvetica 14 bold")
        lblCsv.grid(row=3, column=0, sticky=E)

        #textboxes
        self.txtPrefix = Entry(mainFrame)
        self.txtToken = Entry(mainFrame)
        self.txtPrefix.grid(row=1,column=1, sticky=W)
        self.txtToken.grid(row=2,column=1, sticky=W)

        csvframe = Frame(mainFrame)
        self.txtCsv = Entry(csvframe)
        self.btnOpenCsvDialog = Button(csvframe, text="...", font="Helvetica 14 bold", command=self.openFile)
        self.txtCsv.pack(side=LEFT)
        self.btnOpenCsvDialog.pack()
        csvframe.grid(row=3,column=1, sticky=W)

        self.statusMsg = StringVar()
        self.lblStatus = Label(self.root, textvariable=self.statusMsg, bd=1, relief=SUNKEN, anchor=W, bg="#41B04B", fg="white", font="Helvetica 14 italic")
        self.lblStatus.pack(side=BOTTOM, fill=X)

        btnframe = Frame(mainFrame)
        self.btnDelCust = Button(btnframe, text="Delete Customers", command=self.startThread)
        self.btnDelCust.pack(side=RIGHT)
        self.btnReset = Button(btnframe, text="Reset", command=self.reset)
        self.btnReset.pack()
        btnframe.grid(row=4, column=1)

        checklistFrame = Frame(mainFrame, width=200, height=200, bd=1)
        Label(checklistFrame, text="Checklist", font="Helvetica 15 bold").grid(row=0)
        checklistFrame.grid(row=0, column=2, rowspan=3)

        self.paConfirmation = BooleanVar()
        self.tokenExpiry = BooleanVar()
        chkPaConfirm = Checkbutton(checklistFrame, text="PA Confirmation", variable=self.paConfirmation)
        chkPaConfirm.grid(row=1, sticky=W)
        chkTokenExpiry = Checkbutton(checklistFrame, text="Token Expiry Set", variable=self.tokenExpiry)
        chkTokenExpiry.grid(row=2, sticky=W)

        resultFrame = Frame(mainFrame)
        resultFrame.grid(row=5,column=0, columnspan=3, rowspan=4)

        self.resultText = StringVar()
        resultLabel = Message(resultFrame, textvariable=self.resultText,font="Helvetica 16 bold", width=200)
        resultLabel.pack(pady=10)

    def reset(self):
        self.txtToken.delete(0,END)
        self.txtPrefix.delete(0,END)
        self.txtCsv.delete(0,END)
        self.paConfirmation.set(0)
        self.tokenExpiry.set(0)


    def entriesHaveValues(self):
        return (len(self.txtPrefix.get().strip()) > 0) and (len(self.txtToken.get().strip()) > 0) and (len(self.txtCsv.get().strip()) > 0)

    def startThread(self):
        self.setStatus("")
        thr = threading.Thread(target=self.__deletefunc, args=(), kwargs={})

        thr.start()

    def isChecklistReady(self):
        return self.tokenExpiry.get() and self.paConfirmation.get()

    def openFile(self):
        self.txtCsv.delete(0,END)
        filename = askopenfilename(parent=self.root)
        self.txtCsv.insert(0, filename)
        self.csvFilePath = filename
        #print(filename)

    def setStatus(self, msg):
        self.statusMsg.set(msg)

    def setResult(self, msg):
        self.resultText.set(msg)

    def main(self):
        self.root.mainloop()
