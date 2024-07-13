import os.path
from tkinter import *
from tkinter import messagebox
import random
import tempfile

def clear():
    timeEntry.delete(0, END)
    dateEntry.delete(0, END)
    nameEntry.delete(0, END)
    categoryEntry.delete(0, END)
    billEntry.delete(0, END)

    textArea.delete(1.0, END)

def print_bill():
    if textArea.get(1.0, END) == '\n':
        messagebox.showerror('Error', 'Bill is empty')
    else:
        file = tempfile.mktemp('.txt')
        open(file, 'w').write(textArea.get(1.0, END))
        os.startfile(file, 'print')

def search_bill():
    for i in os.listdir('bills/'):
        if i.split('.')[0] == billEntry.get():
            f = open(f'bills/{i}', 'r')
            textArea.delete(1.0, END)
            for data in f:
                textArea.insert(END, data)
            f.close()
            break
    else:
        messagebox.showerror('Error', 'Invalid Bill Number')

if not os.path.exists('bills'):
    os.mkdir('bills')

def save_bill():
    global billNumber
    result = messagebox.askyesno('Confirm', 'Save the bill?')
    if result:
        bill_content = textArea.get(1.0, END)
        file = open(f'bills/{billNumber}.txt', 'w')
        file.write(bill_content)
        file.close()
        messagebox.showinfo('Success', f'Bill No. {billNumber} is saved.')
        billNumber = random.randint(500, 1000)

billNumber = random.randint(500, 1000)
def enter_area():
    if timeEntry.get() == '' or dateEntry.get() == '' or nameEntry.get() == '' or categoryEntry == '':
        messagebox.showerror('Error', 'Customers Detail Required.')
    else:
        textArea.insert(END, '*******************************************************\n\n')
        textArea.insert(END, '\t\t**Panchakanya Driving Center**\n')
        textArea.insert(END, '\n*******************************************************\n\n')
        textArea.insert(END, f'Bill Number : {billNumber}\n')
        textArea.insert(END, f'Customer Name : {nameEntry.get()}\n')
        textArea.insert(END, f'Category : {categoryEntry.get()}\n')
        textArea.insert(END, f'Time : {timeEntry.get()}\n')
        textArea.insert(END, f'Date : {dateEntry.get()}')
        save_bill()

def format_date(event):
    date = dateEntry.get().replace('/', '')  # Remove any existing slashes
    if len(date) > 8:
        date = date[:8]  # Limit to 8 characters (DDMMYYYY)

    if len(date) > 2:
        date = date[:2] + '/' + date[2:]
    if len(date) > 5:
        date = date[:5] + '/' + date[5:]

    # Update the entry with the formatted date
    dateEntry.delete(0, END)
    dateEntry.insert(0, date)

root = Tk()
root.title('Panchakanya Driving Center')
root.geometry('1278x685')

headingLabel = Label(root, text='Panchakanya Driving Center', font=('times new roman', 30, 'bold'),
                     bg='gray20', fg='gold', bd=12, relief=GROOVE)
headingLabel.pack(fill=X, pady=10)

customer_detail_frame = LabelFrame(root, text='Customer Details', font=('times new roman', 15, 'bold'),
                                   fg='gold', bd=8, relief=GROOVE, bg='gray20')
customer_detail_frame.pack(fill=X, padx=10, pady=10)

# Configure grid columns for customer_detail_frame
customer_detail_frame.grid_columnconfigure(0, weight=1)
customer_detail_frame.grid_columnconfigure(1, weight=1)
customer_detail_frame.grid_columnconfigure(2, weight=1)
customer_detail_frame.grid_columnconfigure(3, weight=1)

nameLabel = Label(customer_detail_frame, text='Name:-', font=('times new roman', 15, 'bold'), bg='gray20', fg='white')
nameLabel.grid(row=0, column=0, pady=10, sticky=E)
nameEntry = Entry(customer_detail_frame, font=('arial', 15), bd=7, width=18)
nameEntry.grid(row=0, column=1, padx=8, pady=10, sticky=W)

timeLabel = Label(customer_detail_frame, text='Time:-', font=('times new roman', 15, 'bold'), bg='gray20', fg='white')
timeLabel.grid(row=1, column=0, pady=10, sticky=E)
timeEntry = Entry(customer_detail_frame, font=('arial', 15), bd=7, width=18)
timeEntry.grid(row=1, column=1, padx=8, pady=10, sticky=W)

dateLabel = Label(customer_detail_frame, text='Date:-', font=('times new roman', 15, 'bold'), bg='gray20', fg='white')
dateLabel.grid(row=0, column=2, pady=10, sticky=E)
dateEntry = Entry(customer_detail_frame, font=('arial', 15), bd=7, width=18)
dateEntry.grid(row=0, column=3, padx=8, pady=10, sticky=W)
dateEntry.bind('<KeyRelease>', format_date)  # Bind the KeyRelease event

categoryLabel = Label(customer_detail_frame, text='Category:-', font=('times new roman', 15, 'bold'), bg='gray20', fg='white')
categoryLabel.grid(row=1, column=2, pady=10, sticky=E)
categoryEntry = Entry(customer_detail_frame, font=('arial', 15), bd=7, width=18)
categoryEntry.grid(row=1, column=3, padx=8, pady=10, sticky=W)

enterButton = Button(customer_detail_frame, text='ENTER', font=('arial', 12, 'bold'), bd=7, width=10, command=enter_area)
enterButton.grid(row=2, column=2, pady=10, sticky=W)

bill_area_frame = LabelFrame(customer_detail_frame, text='Billing Details', font=('times new roman', 15, 'bold'),
                             fg='gold', bd=8, relief=GROOVE, bg='gray20')
bill_area_frame.grid(row=0, column=4, rowspan=3, padx=10, pady=10, sticky='ns')

billframe = Frame(bill_area_frame, bd=8, relief=GROOVE)
billframe.pack(fill=BOTH, expand=True)

billareaLabel = Label(billframe, text='Bill Area', font=('times new roman', 15, 'bold'), bd=7, relief=GROOVE)
billareaLabel.pack(fill=X)

scrollBar = Scrollbar(billframe, orient=VERTICAL)
scrollBar.pack(side=RIGHT, fill=Y)

textArea = Text(billframe, height=20, width=55, yscrollcommand=scrollBar.set)
textArea.pack()
scrollBar.config(command=textArea.yview)

billmenuFrame = LabelFrame(root, text='Customer Details', font=('times new roman', 15, 'bold'),
                           fg='gold', bd=8, relief=GROOVE, bg='gray20')
billmenuFrame.pack()

billLabel = Label(billmenuFrame, text='Bill No:-', font=('times new roman', 15, 'bold'), bg='gray20', fg='white')
billLabel.grid(row=0, column=0, pady=10, sticky=E)

billEntry = Entry(billmenuFrame, font=('arial', 15), bd=7, width=18)
billEntry.grid(row=0, column=1, padx=8, pady=10, sticky=W)

searchButton = Button(billmenuFrame, text='SEARCH', font=('arial', 12, 'bold'), bd=7, width=10, command=search_bill)
searchButton.grid(row=0, column=2, pady=10, padx=11, sticky=W)

printButton = Button(billmenuFrame, text='PRINT', font=('arial', 12, 'bold'), bd=7, width=10, command=print_bill)
printButton.grid(row=0, column=3, pady=10, padx=11, sticky=W)

clearButton = Button(billmenuFrame, text='CLEAR', font=('arial', 12, 'bold'), bd=7, width=10, command=clear)
clearButton.grid(row=0, column=4, pady=10, padx=11, sticky=W)

root.mainloop()
