
from tkinter import ttk
import tkinter as tk
import mysql.connector
 
def show():
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="123", database="finedine")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT customer_name, contact_number, date_of_visit, time_of_visit FROM customer_id")
        records = mycursor.fetchall()
 
        for i, (customer_name, contact_number, date_of_visit, time_of_visit) in enumerate(records, start=1):
            listBox.insert("", "end", values=(customer_name, contact_number, date_of_visit, time_of_visit))
            mysqldb.close()
 
 
root = tk.Tk()
root.title("Customer Details")
root.geometry("800x285")
root.resizable(False, False)
label = tk.Label(
        root,
        text="                      Customer Details                       ",
        bg="#1778F2",
        fg="#ffeead",
        font=("segoe ui",30, "bold")).grid(row=0, columnspan=3),
 
cols = ("Customer Name", "Contact Number", "Date of Visit", "Time of Visit")
listBox = ttk.Treeview(
        root,
        columns=cols,
        show='headings',
        )
 
for col in cols:
    listBox.heading(col, text=col)    
    listBox.grid(row=1, column=0, columnspan=2)
show()
root.mainloop()
