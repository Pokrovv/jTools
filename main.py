from tkinter import *
from tkinter import ttk
import tkinter
import random
from tkinter import messagebox
import pymysql
import csv
from datetime import datetime
import numpy as np

class JStockManager:

    def __init__(self):
        # Config
        WIDTH_WINDOW = 720
        HEIGHT_WINDOW = 640
        # Window
        self.window = Tk()
        style = ttk.Style()

        root = self.window
        root.title('jStock - Manager')
        tree = ttk.Treeview(root, show='headings', height=20)
        placeholderArr = ['', '', '', '', '']
        num = '1234567890'
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        def connectDb():
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='stock'
            )
            return conn

        conn = connectDb()
        cursor = conn.cursor()

        for i in range(0, 5):
            placeholderArr[i] = tkinter.StringVar()

        def readData():
            cursor.connection.ping()
            sql = "SELECT `id`, `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stock ORDER BY `id` DESC"
            cursor.execute(sql)
            results = cursor.fetchall()
            conn.commit()
            conn.close()
            return results

        # REFRESH TABLE FUNC
        def dataRefreshTable():
            for row in tree.get_children():
                tree.delete(row)
            for array in readData():
                tree.insert(parent='', index="end", iid=array, values=(array), tag="rfr")
                tree.tag_configure('rfr', background="#2c3e50")

        def genRandomId():
            randomId = ''.join(random.choice(num + alpha) for _ in range(5))
            print("Successfully generated ID " + randomId)
            return randomId

        def saveData():
            itemId = str(itemIdEntry.get())
            name = str(itemNameEntry.get())
            price = str(itemPriceEntry.get())
            quantity = str(itemQuantityEntry.get())
            category = str(itemCategoryEntry.get())
            valid = True
            if not (itemId[3] == '-'):
                valid = False
            for i in range(0, 3):
                if not (itemId[i] in num):
                    valid = False
                    break
            if not (itemId[4] in alpha):
                valid = False
            if not (valid):
                messagebox.showwarning("", "Invalid Item Id")
                return

        frame = tkinter.Frame(root, bg="#2c3e50")
        frame.pack()
        buttonColor = '#ecf0f1'
        frameManager = tkinter.LabelFrame(frame, text="Manage", borderwidth=5)
        frameManager.grid(row=0, column=0, sticky='w', padx=[10, 200], pady=[20], ipadx=[6])

        # Buttons
        buttonSave = Button(frameManager, text='Save', width=15, borderwidth=3, bg=buttonColor, fg='black', command=saveData)
        buttonSelect = Button(frameManager, text='Select', width=15, borderwidth=3, bg=buttonColor, fg='black')
        buttonDelete = Button(frameManager, text='Delete', width=15, borderwidth=3, bg=buttonColor, fg='black')
        buttonFind = Button(frameManager, text='Find', width=15, borderwidth=3, bg=buttonColor, fg='black')
        buttonClear = Button(frameManager, text='Clear', width=15, borderwidth=3, bg=buttonColor, fg='black')
        buttonExport = Button(frameManager, text='Export to Excel', width=15, borderwidth=3, bg=buttonColor, fg='black')
        buttonUpdate = Button(frameManager, text='Update', width=15, borderwidth=3, bg=buttonColor, fg='black')

        buttonSave.grid(row=0, column=0, padx=5, pady=5)
        buttonSelect.grid(row=0, column=1, padx=5, pady=5)
        buttonDelete.grid(row=0, column=2, padx=5, pady=5)
        buttonFind.grid(row=0, column=3, padx=5, pady=5)
        buttonClear.grid(row=0, column=4, padx=5, pady=5)
        buttonExport.grid(row=0, column=5, padx=5, pady=5)
        buttonUpdate.grid(row=0, column=6, padx=5, pady=5)

        entriesManager = tkinter.LabelFrame(frame, text="Form", borderwidth=5)
        entriesManager.grid(row=1, column=0, sticky='w', padx=[10, 200], pady=[0, 20], ipadx=[6])

        itemNameLabel = Label(entriesManager, text='Item Name', anchor="e", width=10)
        itemIdLabel = Label(entriesManager, text='Item Id', anchor="e", width=10)
        itemPriceLabel = Label(entriesManager, text='Price', anchor="e", width=10)
        itemQuantityLabel = Label(entriesManager, text='Quantity', anchor="e", width=10)
        itemCategoryLabel = Label(entriesManager, text='Item Category', anchor="e", width=11)

        itemNameLabel.grid(row=0, column=0, padx=10)
        itemIdLabel.grid(row=1, column=0, padx=10)
        itemPriceLabel.grid(row=2, column=0, padx=10)
        itemQuantityLabel.grid(row=3, column=0, padx=10)
        itemCategoryLabel.grid(row=4, column=0, padx=10)

        categoryArray = ['Souvenirs', 'Bijoux', 'Bougies', 'Cartes postales', 'Divers']

        itemNameEntry = Entry(entriesManager, width=50, textvariable=placeholderArr[0])
        itemIdEntry = Entry(entriesManager, width=50, textvariable=placeholderArr[1])
        itemPriceEntry = Entry(entriesManager, width=50, textvariable=placeholderArr[2])
        itemQuantityEntry = Entry(entriesManager, width=50, textvariable=placeholderArr[3])
        itemCategoryEntry = ttk.Combobox(entriesManager, width=50, textvariable=placeholderArr[4], values=categoryArray)

        itemNameEntry.grid(row=0, column=1, padx=5, pady=5)
        itemIdEntry.grid(row=1, column=1, padx=5, pady=5)
        itemPriceEntry.grid(row=2, column=1, padx=5, pady=5)
        itemQuantityEntry.grid(row=3, column=1, padx=5, pady=5)
        itemCategoryEntry.grid(row=4, column=1, padx=5, pady=5)

        buttonIdGen = Button(entriesManager, text="Generate ID for the product", borderwidth="3", bg=buttonColor,
                             fg='black', command=lambda: [placeholderArr[1].set(genRandomId())])
        buttonIdGen.grid(row=0, column=2, padx=5, pady=5)

        style.configure(root)

        tree['columns'] = ("Item Name", "Item Id", "Item Price", "Item Quantity", "Item Category", "Date")
        for col in tree['columns']:
            tree.column(col, anchor=W, width=90)
            tree.heading(col, text=col, anchor=W)

        tree.tag_configure('arrow', background="#2c3e50")
        tree.pack()

        dataRefreshTable()

        root.geometry(f'{WIDTH_WINDOW}x{HEIGHT_WINDOW}')
        root.resizable(width=False, height=False)
        root.mainloop()

# Lancer l'application
JStockManager()
