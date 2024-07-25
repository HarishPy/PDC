import os
import sqlite3
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import tempfile
from datetime import datetime
from nepali_datetime import date as nepali_date
import csv

# Database setup
def create_database():
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            bill_number INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            practice_time TEXT NOT NULL,
            payment_type TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS deleted_bills (
                bill_number INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                practice_time TEXT NOT NULL,
                payment_type TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                deleted_date TEXT NOT NULL,
                deleted_time TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()
create_database()

def on_enter(event):
    save_bill()

def gregorian_to_nepali(gregorian_date):
    return nepali_date.from_datetime(gregorian_date)

def reset_bill_number_if_needed():
    current_date = datetime.now()
    nepali_date = gregorian_to_nepali(current_date)
    nepali_month = nepali_date.month
    nepali_day = nepali_date.day

    if nepali_month == 4 and nepali_day == 1:
        save_last_bill_number(0)

# Function to save a bill to the database
def save_bill():
    global billNumber
    if nameEntry.get() == '' or categoryEntry.get() == '' or timeEntry.get()=='' or priceEntry.get()=='' or paymentEntry.get()=='' :
        messagebox.showerror('Error', 'Customers Detail Required.')
    else:
        textArea.delete(1.0, END)
        result = messagebox.askyesno('Confirm', 'Save the bill?')
        if result:
            conn = sqlite3.connect('bills.db')
            cursor = conn.cursor()

            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')

            cursor.execute('''
                INSERT INTO bills (name, category, price, practice_time, payment_type, date, time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nameEntry.get(), categoryEntry.get(), priceEntry.get(), timeEntry.get(),
                  paymentEntry.get(), current_date, current_time))

            conn.commit()
            conn.close()

            messagebox.showinfo('Success', f'Bill is saved.')
            billNumber = cursor.lastrowid
            save_last_bill_number(billNumber)
            display_bill()

def delete():
    bill_number = billEntry.get().strip()

    if not bill_number:
        messagebox.showerror('Error', 'Please specify a Bill Number.')
        return

    if textArea.get(1.0, END).strip() == '':
        messagebox.showerror('Error', 'Bill details are not displayed.')
        return

    result = messagebox.askyesno('Confirm', 'Are you sure you want to delete this bill?')
    if result:
        conn = sqlite3.connect('bills.db')
        cursor = conn.cursor()

        # Fetch the bill details
        cursor.execute('SELECT * FROM bills WHERE bill_number = ?', (bill_number,))
        bill_data = cursor.fetchone()

        if bill_data:
            # Insert into deleted_bills table
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')

            cursor.execute('''
                INSERT INTO deleted_bills (bill_number, name, category, price, practice_time, payment_type, date, time, deleted_date, deleted_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*bill_data, current_date, current_time))

            # Delete from the bills table
            cursor.execute('DELETE FROM bills WHERE bill_number = ?', (bill_number,))

            conn.commit()
            conn.close()

            messagebox.showinfo('Success', f'Bill No. {bill_number} has been deleted.')

            # Clear the displayed bill
            textArea.delete(1.0, END)
            billEntry.delete(0, END)
        else:
            conn.close()
            messagebox.showerror('Error', 'No such bill found.')


def display_bill():
    textArea.delete(1.0, END)
    textArea.insert(END, '\t**Panchakanya Driving Center**\n\n')
    textArea.insert(END, f'Bill Number : {billNumber}\n')
    textArea.insert(END, f'Name : {nameEntry.get()}\n')
    textArea.insert(END, f'Category : {categoryEntry.get()}\n')
    textArea.insert(END, f'Price : Rs. {priceEntry.get()}\n')
    textArea.insert(END, f'Practice Time : {timeEntry.get()}\n')
    textArea.insert(END, f'Payment Type : {paymentEntry.get()}\n')
    current_date = datetime.now().strftime('%d/%m/%Y')
    textArea.insert(END, f'Date : {current_date}\n')
    current_time = datetime.now().strftime('%H:%M:%S')
    textArea.insert(END, f'Time : {current_time}')


# Function to print the bill
def print_bill():
    if textArea.get(1.0, END).strip() == '':
        messagebox.showerror('Error', 'Bill is empty')
    else:
        file = tempfile.mktemp('.txt')
        with open(file, 'w') as f:
            f.write(textArea.get(1.0, END))
        os.startfile(file, 'print')


# Function to clear the entries
def clear():
    nameEntry.delete(0, END)
    categoryEntry.set('')
    timeEntry.delete(0, END)
    priceEntry.delete(0, END)
    paymentEntry.set('')
    textArea.delete(1.0, END)


# Function to search for a bill based on bill number
def search_bill():
    bill_number = billEntry.get()
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bills WHERE bill_number = ?', (bill_number,))
    row = cursor.fetchone()
    if row:
        textArea.delete(1.0, END)
        textArea.insert(END, f'Bill Number : {row[0]}\n')
        textArea.insert(END, f'Name : {row[1]}\n')
        textArea.insert(END, f'Category : {row[2]}\n')
        textArea.insert(END, f'Price : Rs. {row[3]}\n')
        textArea.insert(END, f'Practice Time : {row[4]}\n')
        textArea.insert(END, f'Payment Type : {row[5]}\n')
        textArea.insert(END, f'Date : {row[6]}\n')
        textArea.insert(END, f'Time : {row[7]}')
    else:
        messagebox.showerror('Error', 'Invalid Bill Number')
    conn.close()


# Function to load the last bill number
def load_last_bill_number():
    if os.path.exists('last_bill_number.txt'):
        with open('last_bill_number.txt', 'r') as file:
            return int(file.read().strip())
    else:
        return 0


# Function to save the last bill number
def save_last_bill_number(number):
    with open('last_bill_number.txt', 'w') as file:
        file.write(str(number))


# Initialize bill number
billNumber = load_last_bill_number()

def capitalize_entry(entry):
    text = entry.get()
    capitalized_text = text.capitalize()
    entry.delete(0, END)
    entry.insert(0, capitalized_text)

def download_transactions(data):
    # Prompt the user to select a file location and name
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        # Write the data to a CSV file
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["Bill Number", "Name", "Category", "Price", "Practice Time", "Payment Type", "Date", "Time", "Deleted Date", "Deleted Time"])
            # Write the data
            for row in data:
                writer.writerow(row)
        messagebox.showinfo("Download Complete", "Transactions have been downloaded successfully.")


def display_transactions():
    # Create a new Toplevel window
    transaction_window = Toplevel(root)
    transaction_window.title('Transactions')
    transaction_window.geometry('900x500')

    # Fetch records from the database for the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()

    # Fetch records from bills table
    cursor.execute('SELECT * FROM bills WHERE date = ?', (current_date,))
    bills = cursor.fetchall()

    # Fetch records from deleted_bills table
    cursor.execute('SELECT * FROM deleted_bills WHERE deleted_date = ?', (current_date,))
    deleted_bills = cursor.fetchall()

    conn.close()

    # Combine bills and deleted bills data
    all_data = bills + deleted_bills

    # Create a frame for the download button
    button_frame = Frame(transaction_window)
    button_frame.pack(fill=X)

    # Create the "Download" button
    download_button = Button(button_frame, text="Download", command=lambda: download_transactions(all_data))
    download_button.pack(pady=10)

    # Define columns
    columns = (
    "Bill Number", "Name", "Category", "Price", "Practice Time", "Payment Type", "Date", "Time", "Deleted Date",
    "Deleted Time")

    # Create Treeview widget within a frame
    tree_frame = Frame(transaction_window)
    tree_frame.pack(fill=BOTH, expand=True)

    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
    tree.heading("Bill Number", text="Bill Number")
    tree.heading("Name", text="Name")
    tree.heading("Category", text="Category")
    tree.heading("Price", text="Price")
    tree.heading("Practice Time", text="Practice Time")
    tree.heading("Payment Type", text="Payment Type")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Deleted Date", text="Deleted Date")
    tree.heading("Deleted Time", text="Deleted Time")

    # Set column widths
    for col in columns:
        tree.column(col, width=100, anchor=CENTER)

    # Insert bills into the Treeview
    for bill in bills:
        tree.insert("", "end", values=(bill[0], bill[1], bill[2], bill[3], bill[4], bill[5], bill[6], bill[7], '', ''))

    # Insert deleted bills into the Treeview
    for deleted_bill in deleted_bills:
        tree.insert("", "end", values=(deleted_bill[0], deleted_bill[1], deleted_bill[2], deleted_bill[3],
                                       deleted_bill[4], deleted_bill[5], deleted_bill[6], deleted_bill[7],
                                       deleted_bill[8], deleted_bill[9]))

    # Add a scrollbar to the Treeview
    scrollbar = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(fill=BOTH, expand=True)


# Tkinter GUI setup
root = Tk()
root.title('Panchakanya Driving Center')
root.geometry('1278x685')

# Define colors
bg_color = '#34495E'
fg_color = '#F1C40F'
label_bg = '#2C3E50'
entry_bg = '#ECF0F1'
entry_fg = '#2C3E50'
btn_bg = '#1ABC9C'
btn_fg = '#ECF0F1'
heading_fg = '#E74C3C'

# Heading
headingLabel = Label(root, text='Panchakanya Driving Center', font=('times new roman', 24, 'bold'),
                     bg=bg_color, fg=heading_fg, bd=11, relief=GROOVE)
headingLabel.pack(fill=X, pady=10)

# Customer Detail Frame
customer_detail_frame = LabelFrame(root, text='Customer Details', font=('times new roman', 14, 'bold'),
                                   bd=8, relief=GROOVE, fg=heading_fg, bg=bg_color)
customer_detail_frame.pack(fill=X, padx=10, pady=10)

customer_detail_frame.grid_columnconfigure(0, weight=1)
customer_detail_frame.grid_columnconfigure(1, weight=1)
customer_detail_frame.grid_columnconfigure(2, weight=1)
customer_detail_frame.grid_columnconfigure(3, weight=1)

# Input fields
nameLabel = Label(customer_detail_frame, text='Name:-', font=('Helvetica', 12, 'bold'), bg=label_bg, fg=fg_color)
nameLabel.grid(row=0, column=0, pady=10, sticky=E)
nameEntry = Entry(customer_detail_frame, font=('Helvetica', 12), bd=7, width=18, bg=entry_bg, fg=entry_fg)
nameEntry.grid(row=0, column=1, padx=8, pady=10, sticky=W)
nameEntry.bind('<FocusOut>', lambda event: capitalize_entry(nameEntry))

timeLabel = Label(customer_detail_frame, text='Time:-', font=('Helvetica', 12, 'bold'), bg=label_bg, fg=fg_color)
timeLabel.grid(row=1, column=0, pady=10, sticky=E)
timeEntry = Entry(customer_detail_frame, font=('Helvetica', 12), bd=7, width=18, bg=entry_bg, fg=entry_fg)
timeEntry.grid(row=1, column=1, padx=8, pady=10, sticky=W)

categoryLabel = Label(customer_detail_frame, text='Category:-', font=('Helvetica', 12, 'bold'), bg=label_bg,
                      fg=fg_color)
categoryLabel.grid(row=0, column=2, pady=10, sticky=E)
categoryEntry = ttk.Combobox(customer_detail_frame, font=('Helvetica', 12), width=18, state='readonly')
categoryEntry['values'] = ('Bike', 'Car', 'Scooter')
categoryEntry.grid(row=0, column=3, padx=8, pady=10, sticky=W)

priceLabel = Label(customer_detail_frame, text='Price:-', font=('Helvetica', 12, 'bold'), bg=label_bg, fg=fg_color)
priceLabel.grid(row=1, column=2, pady=10, sticky=E)
priceEntry = Entry(customer_detail_frame, font=('Helvetica', 12), bd=7, width=18, bg=entry_bg, fg=entry_fg)
priceEntry.grid(row=1, column=3, padx=8, pady=10, sticky=W)

paymentLabel = Label(customer_detail_frame, text='Payment Type:-', font=('Helvetica', 12, 'bold'), bg=label_bg,
                     fg=fg_color)
paymentLabel.grid(row=2, column=0, pady=10, sticky=E)
paymentEntry = ttk.Combobox(customer_detail_frame, font=('Helvetica', 12), width=18, state='readonly')
paymentEntry['values'] = ('Cash', 'QR')
paymentEntry.grid(row=2, column=1, padx=8, pady=10, sticky=W)

enterButton = Button(customer_detail_frame, text='ENTER', font=('arial', 11, 'bold'), bd=7, width=10, command=save_bill,
                     bg=btn_bg, fg=btn_fg)
enterButton.grid(row=2, column=3, pady=10, sticky=W)

# Bill Area Frame
bill_area_frame = LabelFrame(customer_detail_frame, text='Billing Details', font=('times new roman', 12, 'bold'),
                             fg=fg_color, bd=8, relief=GROOVE, bg=bg_color)
bill_area_frame.grid(row=0, column=4, rowspan=3, padx=10, pady=10, sticky='ns')

billframe = Frame(bill_area_frame, bd=8, relief=GROOVE)
billframe.pack(fill=BOTH, expand=True)

billareaLabel = Label(billframe, text='Bill Area', font=('Helvetica', 12, 'bold'), bd=7, relief=GROOVE)
billareaLabel.pack(fill=X)

scrollBar = Scrollbar(billframe, orient=VERTICAL)
scrollBar.pack(side=RIGHT, fill=Y)

textArea = Text(billframe, height=20, width=55, yscrollcommand=scrollBar.set)
textArea.pack()
scrollBar.config(command=textArea.yview)

# Bill Menu Frame
billmenuFrame = LabelFrame(root, text='Billing Menu', font=('Helvetica', 12, 'bold'),
                           bd=8, relief=GROOVE, fg=heading_fg, bg=bg_color)
billmenuFrame.pack()

billLabel = Label(billmenuFrame, text='Bill No:-', font=('Helvetica', 12, 'bold'), bg=label_bg, fg=fg_color)
billLabel.grid(row=0, column=0, pady=10, sticky=E)

billEntry = Entry(billmenuFrame, font=('Helvetica', 12), bd=7, width=10, bg=entry_bg, fg=entry_fg)
billEntry.grid(row=0, column=1, padx=8, pady=10, sticky=W)

searchButton = Button(billmenuFrame, text='SEARCH', font=('Helvetica', 11, 'bold'), bd=7, width=10, command=search_bill,
                      bg=btn_bg, fg=btn_fg)
searchButton.grid(row=0, column=2, padx=10)

printButton = Button(billmenuFrame, text='PRINT', font=('Helvetica', 11, 'bold'), bd=7, width=10, command=print_bill,
                     bg=btn_bg, fg=btn_fg)
printButton.grid(row=0, column=3, padx=10)

clearButton = Button(billmenuFrame, text='CLEAR', font=('Helvetica', 11, 'bold'), bd=7, width=10, command=clear,
                     bg=btn_bg, fg=btn_fg)
clearButton.grid(row=0, column=4, padx=10)

deleteButton = Button(billmenuFrame, text='DELETE', font=('Helvetica', 10, 'bold'), bd=7, width=10, command=delete, bg=btn_bg, fg=btn_fg)
deleteButton.grid(row=0,column=5, padx=10)

transactionButton = Button(billmenuFrame, text='TRANSACTION', font=('Helvetica', 10, 'bold'), bd=7, width=11, command=display_transactions, bg=btn_bg,fg=btn_fg)
transactionButton.grid(row=1,column=3,padx=10, pady=10)


root.bind('<Return>', on_enter)

root.mainloop()
