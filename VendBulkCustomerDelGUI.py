from Tkinter import *
import threading

class VendBulkCustomerDelGUI:

    def __init__(self, deletefunc):
        self.__deletefunc = deletefunc
        self.root = Tk()
        self.root.title("Vend Bulk Customer Delete")

        header = Label(self.root, text="Bulk Customer Delete", bd=1, font="Helvetica 18 bold", bg="#41B04B", fg="white")
        #label.grid(row=0, column=0, columnspan=3)
        header.pack(side=TOP, anchor=W, fill=X)

        mainFrame = Frame(self.root,width=600, height=400)
        mainFrame.pack(padx=20, pady=10)
        #mainFrame.grid(padx=20, pady=10)



        lblStorePrefix = Label(mainFrame, text="Store Prefix:", font="Helvetica 14 bold")
        lblStorePrefix.grid(row=1, column=0, sticky=E)

        lblToken = Label(mainFrame, text="Token:", font="Helvetica 14 bold")
        lblToken.grid(row=2, column=0, sticky=E)

        lblCsv = Label(mainFrame, text="CSV File:", font="Helvetica 14 bold")
        lblCsv.grid(row=3, column=0, sticky=E)

        self.txtPrefix = Entry(mainFrame)
        self.txtToken = Entry(mainFrame)
        self.txtPrefix.grid(row=1,column=1, sticky=W)
        self.txtToken.grid(row=2,column=1, sticky=W)

        csvframe = Frame(mainFrame)
        self.txtCsv = Entry(csvframe)
        self.openCsvDialog = Button(csvframe, text="...", font="Helvetica 14 bold") #need to make command
        self.txtCsv.pack(side=LEFT)
        self.openCsvDialog.pack()
        csvframe.grid(row=3,column=1, sticky=W)

        self.statusMsg = StringVar()
        self.lblStatus = Label(self.root, textvariable=self.statusMsg, bd=1, relief=SUNKEN, anchor=W, bg="#41B04B", fg="white")
        self.lblStatus.pack(side=BOTTOM, fill=X)


        self.btnDelCust = Button(mainFrame, text="Delete Customers", command=self.startThread)
        self.btnDelCust.grid(row=4, columnspan=2)

        checklistFrame = Frame(mainFrame, width=200, height=200)
        checklistFrame.grid(row=1, column=2, rowspan=4)

    def entriesHaveValues(self):
        return (len(self.txtPrefix.get().strip()) > 0) and (len(self.txtToken.get().strip()) > 0) and (len(self.txtCsv.get().strip()) > 0)

    def startThread(self):
        self.setStatus("")
        thr = threading.Thread(target=self.__deletefunc, args=(), kwargs={})

        thr.start()

    def setStatus(self, msg):
        self.statusMsg.set(msg)

    def main(self):
        self.root.mainloop()
