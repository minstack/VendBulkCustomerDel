from Tkinter import *

class VendBulkCustomerDelGUI:

    def __init__(self):
        self.root = Tk()
        self.root.title("Vend Bulk Customer Delete")
        mainFrame = Frame(self.root,width=600, height=400)
        mainFrame.pack(side=LEFT,anchor=N)
        mainFrame.grid(padx=20, pady=10)

        label = Label(mainFrame, text="Bulk Customer Delete", font="Helvetica 18 bold")
        label.grid(row=0, column=0, columnspan=3)

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

        self.btnDelCust = Button(mainFrame, text="Delete Customers")

        checklistFrame = Frame(mainFrame, width=200, height=200)
        checklistFrame.grid(row=1, column=2, rowspan=4)

    def main(self):
        self.root.mainloop()
