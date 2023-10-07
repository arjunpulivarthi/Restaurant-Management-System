#---------------------------------------------------------------------------------------------------IMPORT FUNCTIONS START-----------------------------------------------------------------------------------------------------------
import mysql.connector
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tmsg
import os
import time
from datetime import date
import datetime
from PIL import ImageTk, Image
import subprocess
from twilio.rest import Client

#---------------------------------------------------------------------------------------------------IMPORT FUNCTIONS END-------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------DECALRING VARIABLES START----------------------------------------------------------------------------------------------------------

menu_category = ["Coffee / Tea","Beverages","Fast Food","South Indian","Starters","Main Course","Dessert"]
menu_category_dict = {"Coffee / Tea":"1 Tea & Coffee.txt",
                      "Beverages":"2 Beverages.txt",
                      "Fast Food":"3 Fast Food.txt",
                      "South Indian":"4 South Indian.txt",
                      "Starters":"5 Starters.txt",
                      "Main Course":"6 Main Course.txt",
                      "Dessert":"7 Dessert.txt"}
order_dict = {}
for i in menu_category:
    order_dict[i] = {}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
today_date = date.today()
t = time.localtime()
current_time = datetime.datetime.now().strftime("%H:%M:%S")
client = Client("AC355a10d8653806b242c250d8c1cbf6de", "97c596116b15e9766235738d77272073")

#--------------------------------------------------------------------------------------------------DECALRING VARIABLES END-----------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------DECLARING FUNCTIONS START----------------------------------------------------------------------------------------------------------

def load_menu():
    menuCategory.set("")
    menu_table.delete(*menu_table.get_children())
    menu_file_list = os.listdir("Menu")
    for file in menu_file_list:
        f = open("Menu\\" + file , "r")
        category=""
        while True:
            line = f.readline()
            if(line==""):
                menu_table.insert('',END,values=["","",""])
                break
            elif (line=="\n"):
                continue
            elif(line[0]=='#'):
                category = line[1:-1]
                name = "\t\t"+line[:-1]
                price = ""
            elif(line[0]=='*'):
                name = line[:-1]
                price = ""
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
            
            menu_table.insert('',END,values=[name,price,category])

def load_order():
    order_table.delete(*order_table.get_children())
    for category in order_dict.keys():
        if order_dict[category]:
            for lis in order_dict[category].values():
                order_table.insert('',END,values=lis)
    update_total_price()

def add_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if name in order_dict[category].keys():
        tmsg.showinfo("Error", "Item already exist in your order")
        return
    if not quantity.isdigit():
        tmsg.showinfo("Error", "Please Enter Valid Quantity")
        return
    lis = [name,rate,quantity,str(int(rate)*int(quantity)),category]
    order_dict[category][name] = lis
    load_order()
    
def load_item_from_menu(event):
    cursor_row = menu_table.focus()
    contents = menu_table.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemCategory.set(row[2])
    itemQuantity.set("1")

def load_item_from_order(event):
    cursor_row = order_table.focus()
    contents = order_table.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemQuantity.set(row[2])
    itemCategory.set(row[4])

def show_button_operation():
    category = menuCategory.get()
    if category not in menu_category:
        tmsg.showinfo("Error", "Please Select A Valid Choice")
    else:
        menu_table.delete(*menu_table.get_children())
        f = open("Menu\\" + menu_category_dict[category] , "r")
        while True:
            line = f.readline()
            if(line==""):
                break
            if (line[0]=='#' or line=="\n"):
                continueFUNCTION
            if(line[0]=='*'):
                name = "\t"+line[:-1]
                menu_table.insert('',END,values=[name,"",""])
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
                menu_table.insert('',END,values=[name,price,category])

def clear_button_operation():
    itemName.set("")
    itemRate.set("")
    itemQuantity.set("")
    itemCategory.set("")

def cancel_button_operation():
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    ans = tmsg.askquestion("Cancel Order", "Are You Sure to Cancel Order?")
    if ans=="no":
        return
    order_table.delete(*order_table.get_children())
    for i in menu_category:
        order_dict[i] = {}
    clear_button_operation()
    update_total_price()

def update_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if category=="":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    if order_dict[category][name][2]==quantity:
        tmsg.showinfo("Error", "No changes in Quantity")
        return
    order_dict[category][name][2] = quantity
    order_dict[category][name][3] = str(int(rate)*int(quantity))
    load_order()

def remove_button_operation():
    name = itemName.get()
    category = itemCategory.get()

    if category=="":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    del order_dict[category][name]
    load_order()

def update_total_price():
    price = 0
    for i in menu_category:
        for j in order_dict[i].keys():
            price += int(order_dict[i][j][3])
    if price == 0:
        totalPrice.set("")
    else:
        totalPrice.set("₹"+str(price)+"/-")

def bill_button_operation():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    customer_name = customerName.get()
    customer_contact = customerContact.get()
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    if customer_name=="" or customer_contact=="":
        tmsg.showinfo("Error", "Customer Details Required")
        return
    if not customerContact.get().isdigit():
        tmsg.showinfo("Error", "Invalid Customer Contact")
        return   
    ans = tmsg.askquestion("Generate Bill", "Are You Sure you want to Generate Bill?")
    ans = "yes"
    if ans=="yes":
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="arpulivarthi",
        database="finedine"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO customer_id(customer_name, contact_number, date_of_visit, time_of_visit) VALUES (%s, %s, %s, %s)"
        val = (customer_name, customer_contact, today_date, current_time)
        mycursor.execute(sql, val)

        mydb.commit()
        print(customer_contact)
        bill = Toplevel()
        bill.title("Bill")
        bill.geometry("420x900+300+100")
        bill.wm_iconbitmap("Coffee.ico")
        bill_text_area = Text(bill, font=("segoe ui", 12))
        st = "\t           FINE DINE RESTAURANT\n\t            BENGALURU-560002\n"
        st += "\t      GST.NO:- 27AHXPP3379HIZH\n\n"
        st += "-"*32 + "BILL" + "-"*32 + "\n\nDate:- "
        
#Declaration of Date and Time for the bill

        t = time.localtime(time.time())
        week_day_dict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",
                            6:"Sunday"}
        st += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
        st += " "*9 + f"Time:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

#Customer Name & Contact
        st += f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\n"
        st += " \n"
        st += "-"*69 + "\n" + "DESCRIPTION" + "      " + "RATE" + "         " + "QUANTITY" + "        " + "AMOUNT\n"
        st += "-"*69 + "\n"

        #List of Items
        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3]
                st += name + "\t" + rate + "                   " + quantity + "                     " + price + "\n\n"
        st += "-"*69

#Total Price
        st += f"                                                              Total price : {totalPrice.get()}\n"
        st += "-"*69
        st += "                         ""Thank You, Visit Again!!"

#Display bill in a new window
        bill_text_area.insert(1.0, st)

#Save the bills as a file
        folder = f"{t.tm_mday}-{t.tm_mon}-{t.tm_year}"
        if not os.path.exists(f"Bill Records\\{folder}"):
            os.makedirs(f"Bill Records\\{folder}")
        file = open(f"Bill Records\\{folder}\\{customer_name+customer_contact}.txt", "w")
        #file.write(st)
        file.close()

#Clear operaitons
        order_table.delete(*order_table.get_children())
        for i in menu_category:
            order_dict[i] = {}
        clear_button_operation()
        update_total_price()
        customerName.set("")
        customerContact.set("")

        bill_text_area.pack(expand=True, fill=BOTH)
        bill.focus_set()
        bill.protocol("WM_DELETE_WINDOW", close_window)
        print(price)
        contactn = "+91" + customer_contact
        dm = "Hello " + customer_name + ", Thanks for visiting Fine Dine Restaurant, Have a Good Day. Your Total Bill is ₹" + price + "/-"
        client.messages.create(to=contactn, from_="+19377779588", body=dm)

def close_window():
    tmsg.showinfo("Thanks", "Thanks for using our service")
    root.mainloop()

def clock():
   hh= time.strftime("%I")
   mm= time.strftime("%M")
   ss= time.strftime("%S")
   day=time.strftime("%A")
   ap=time.strftime("%p")
   my_lab.config(text= hh + ":" + mm +":" + ss + " " + ap)
   my_lab.after(1000,clock)
   my_lab1.config(text = day)
   present_time = my_lab.config(text= hh + ":" + mm +":" + ss + " " + ap)

def updateTime():
   my_lab.config(text= "New Text")

def open_calculator():
    os.system("calc")

def open_bills():
    path = r'C:\Users\arpul\OneDrive\Desktop\RESTAURANT\Bill Records'
    os.startfile(path)

def show_customers():
    path1 = r'C:\Users\arpul\OneDrive\Desktop\RESTAURANT\mysqltest.py'
    os.startfile(path1)

def logout_btn():
    root.destroy()
    path2 = r'C:\Users\arpul\OneDrive\Desktop\RESTAURANT\login.py'
    os.startfile(path2)

        
#---------------------------------------------------------------------------------------------------DECLARING FUNCTIONS END----------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------TKINTER GUI APPEARENCE START--------------------------------------------------------------------------------------------------------

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("AR GROUP")
root.wm_iconbitmap("Burger.ico")
root.state('zoomed')
canv = Canvas(master=root)
canv.place(x=0, y=0, width=1920, height=1080)
img = ImageTk.PhotoImage(Image.open("pic.jpg"))
canv.create_image(0, 0, image=img)

#-----------------------TITLE / NAME----------------------

style_button = ttk.Style()
style_button.configure(
            "TButton",
            font = ("segoe ui",10,"bold"), 
            background="#ffeead"
            )
title_frame = Frame(
            root, 
            bd=5, 
            bg="#4267B2", 
            relief=GROOVE
            )
title_frame.pack(
            side=TOP,
            fill="x"
            )
title_frame.place(
            x=20,
            y=10,
            height=160,
            width=1875
            )
title_label = Label(
            title_frame, 
            text="Fine Dine Restaurant",
            font=("segoe ui", 20, "bold"),
            bg = "#4267B2",
            fg="white",
            pady=5)
canv1 = Canvas(master=title_frame, highlightthickness=0)
canv1.place(x=660, y=10, width=540, height=125)
logo = ImageTk.PhotoImage(Image.open("logo.png"))
canv1.create_image(275, 62, image=logo)
title_label.pack()
canv2 = Canvas(master=title_frame, highlightthickness=0)
canv2.place(x=1660, y=10, width=200, height=130)
logo1 = ImageTk.PhotoImage(Image.open("elephantlogo.png"))
canv2.create_image(100, 65, image=logo1)
title_label.pack()
canv3 = Canvas(master=title_frame, highlightthickness=0)
canv3.place(x=1415, y=10, width=200, height=130)
logo2 = ImageTk.PhotoImage(Image.open("elephantlogo.png"))
canv3.create_image(100, 65, image=logo2)
title_label.pack()

canv4 = Canvas(master=title_frame, highlightthickness=0)
canv4.place(x=5, y=10, width=200, height=130)
logo3 = ImageTk.PhotoImage(Image.open("elephantlogoinv.png"))
canv4.create_image(100, 65, image=logo3)
title_label.pack()

canv5 = Canvas(master=title_frame, highlightthickness=0)
canv5.place(x=250, y=10, width=200, height=130)
logo4 = ImageTk.PhotoImage(Image.open("elephantlogoinv.png"))
canv5.create_image(100, 65, image=logo4)
title_label.pack()

canv6 = Canvas(master=title_frame, highlightthickness=0)
canv6.place(x=500, y=10, width=200, height=130)
logo5 = ImageTk.PhotoImage(Image.open("elephantlogoinv.png"))
canv6.create_image(100, 65, image=logo5)
title_label.pack()

canv7 = Canvas(master=title_frame, highlightthickness=0)
canv7.place(x=1170, y=10, width=200, height=130)
logo6 = ImageTk.PhotoImage(Image.open("elephantlogo.png"))
canv7.create_image(100, 65, image=logo6)
title_label.pack()

canv8 = Canvas(root, highlightthickness=0)
canv8.place(x=1706, y=227, width=186, height=201)
logo7 = ImageTk.PhotoImage(Image.open("download1.png"))
canv8.create_image(92, 100, image=logo7)
title_label.pack()


logout_button = tk.Button(
            root,
            bg = "#f1f1f0",
            bd = 0,
            fg = "red",
            text="Logout",
            font=("comic sans ms", 15, "bold"),
            width=15,
            command = logout_btn
            )

logout_button.place(
            x=1706,
            y=182,
            )

#---------------------CUSTOMER DETALLS--------------------

customer_frame = LabelFrame(
            root,text="Enter Customer Details",
            font=("segoe ui", 18, "bold"),
            bd=5, 
            bg="#1778F2",
            fg="#ffeead",
            relief="ridge"
            )
customer_frame.pack(
            side=TOP, 
            fill="x"
            )
customer_name_label = Label(
            customer_frame, 
            text="Name                    :", 
            font=("segoe ui", 19, "bold"),
            bg = "#1778F2", 
            fg="#ffeead", 
            bd=5
            )
customer_name_label.grid(
            row = 0,
            column = 0
            )
customerName = StringVar()
customerName.set("")
customer_name_entry = Entry(
            customer_frame,
            width=20,
            font=("segoe ui", 15),
            bd=5, 
            textvariable=customerName
            )
customer_name_entry.grid(
            row = 0, 
            column=1,
            padx=50
            )
customer_contact_label = Label(
            customer_frame, 
            text="Contact Number  :", 
            font=("segoe ui", 19, "bold"), 
            bg = "#1778F2", 
            fg="#ffeead", 
            bd = 5
            )
customer_contact_label.grid(
            row = 1, 
            column = 0
            )
customerContact = StringVar()
customerContact.set("")
customer_contact_entry = Entry(
            customer_frame,
            width=20,
            font=("segoe ui", 15),
            bd=5, 
            textvariable=customerContact
            )
customer_contact_entry.grid(
            row = 1, 
            column=1,
            padx=50
            )
customer_frame.place(
            x=20,
            y=180,
            height=150,
            width=920
            )
dummy_label= Label(
            customer_frame,
            text = "\t\t", 
            bg = "#1778F2", 
            fg = "#1778F2"
            )
dummy_label.grid(
            row = 0, 
            column = 2
            )
dummy_label2= Label(
            customer_frame,text= ""
            )
dummy_label2.grid(
            row = 0,
            column = 3
            )
my_lab= Label(
            customer_frame,
            text= "",
            font=("segoe ui", 25, "bold"),
            bg = "#1778F2", 
            fg= "#ffeead"
            )
my_lab.grid(
            row = 0, 
            column = 4
            )
my_lab1= Label(
            customer_frame,
            text= "",
            font=("segoe ui",22, "bold"),
            bg = "#1778F2", 
            fg= "#ffeead"
            )
my_lab1.grid(
            row = 1,
            column = 4
            )
clock()

#---------------------------MENU FRAME--------------------------

menu_frame = Frame(
            root, 
            bd=5, 
            bg="#1778F2", 
            relief=GROOVE
            )
menu_frame.place(
            x=20,
            y=350,
            height=650,
            width=920
            )
menu_label = Label(
            menu_frame,
            text="Menu",
            font=("segoe ui", 20, "bold"),
            bg = "#1778F2",
            fg="#ffeead",
            pady=0
            )
menu_label.pack(
            side=TOP,
            fill="x"
            )
menu_category_frame = Frame(
            menu_frame,
            bg="#1778F2",
            pady=10
            )
menu_category_frame.pack(
            fill="x"
            )
combo_lable = Label(
            menu_category_frame,
            text="Select Type",
            font=("segoe ui", 12, "bold"),
            bg = "#1778F2",
            fg="#ffeead"
            )
combo_lable.grid(
            row=0,
            column=0,
            padx=7
            )
menuCategory = StringVar()
combo_menu = ttk.Combobox(
            menu_category_frame,
            values=menu_category,
            textvariable=menuCategory
            )
combo_menu.grid(
            row=0,
            column=1,
            padx=5
            )
dummy_button = Label(
            menu_category_frame,
            text="",
            width = 50,
            bg = "#1778F2"
            )
dummy_button.grid(
            row = 0,
            column = 3
            )
    
show_button = ttk.Button(
            menu_category_frame,
            text="Show",
            width=10, 
            command=show_button_operation
            )
show_button.grid(
            row=0,
            column=4,
            padx=60
            )
show_all_button = ttk.Button(
            menu_category_frame,
            text="Show All",
            width=10,
            command=load_menu
            )
show_all_button.grid(
            row=0,
            column=5
            )

#-----------------------MENU TABLE------------------------

menu_table_frame = Frame(
            menu_frame
            )
menu_table_frame.pack(
            fill=BOTH,
            expand=1
            )
menu_table_frame.place(
            x=10,
            y=100,
            height=500,
            width=890
            )
scrollbar_menu_x = Scrollbar(
            menu_table_frame,
            orient=HORIZONTAL
            )
scrollbar_menu_y = Scrollbar(
            menu_table_frame,
            orient=VERTICAL
            )
style = ttk.Style()
style.configure(
            "Treeview.Heading",
            font=("segoe ui",13, "bold")
            )
style.configure(
            "Treeview",
            font=("segoe ui",12),
            rowheight=45
            )
menu_table = ttk.Treeview(
            menu_table_frame,
            style = "Treeview", 
            columns =("name","price","category"),
            xscrollcommand=scrollbar_menu_x.set, 
            yscrollcommand=scrollbar_menu_y.set
            )
menu_table.heading(
            "name",
            text="Name"
            )
menu_table.heading(
            "price",
            text="Price"
            )
menu_table["displaycolumns"]=(
            "name", 
            "price"
            )
menu_table["show"] = (
            "headings"
            )
menu_table.column(
            "price",
            width=50,
            anchor='center'
            )
scrollbar_menu_x.pack(
            side=BOTTOM,
            fill=X
            )
scrollbar_menu_y.pack(
            side=RIGHT,
            fill=Y
            )
scrollbar_menu_x.configure(
            command=menu_table.xview
            )
scrollbar_menu_y.configure(
            command=menu_table.yview
            )
menu_table.pack(
            fill=BOTH,
            expand=1
            )
load_menu()
menu_table.bind(
            "<ButtonRelease-1>",
            load_item_from_menu
            )

#-----------------------ITEM FRAME------------------------

item_frame = Frame(
            root,
            bd=5,
            bg="#1778F2",
            relief=GROOVE
            )
item_frame.place(
            x=980,
            y=180,
            height=250,
            width=690
            )
item_title_label = Label(
            item_frame,
            text="Item",
            font=("segoe ui", 20, "bold"),
            bg = "#1778F2", 
            fg="#ffeead"
            )
item_title_label.pack(
            side=TOP,
            fill="x"
            )
item_frame2 = Frame(
            item_frame,
            bg="#1778F2"
            )
item_frame2.pack(
            fill=X
            )
dummy_label5 = Label(
            item_frame2, 
            text="",
            bg = "#1778F2",
            fg="#1778F2"
            )
dummy_label5.grid(
            row=0,
            column=0
            )
item_name_label = Label(
            item_frame2,
            text="Name", 
            font=("segoe ui", 12, "bold"),
            bg = "#1778F2", 
            fg="#ffeead"
            )
item_name_label.grid(
            row=1,
            column=0
            )
itemCategory = StringVar()
itemCategory.set("")
itemName = StringVar()
itemName.set("")
item_name = Entry(
            item_frame2, 
            font=("segoe ui", 12),
            textvariable=itemName,
            state=DISABLED, 
            width=25
            )
item_name.grid(
            row=1,
            column=1,
            padx=10
            )
item_rate_label = Label(
            item_frame2, 
            text="Rate", 
            font=("segoe ui", 12, "bold"),
            bg = "#1778F2", 
            fg="#ffeead"
            )
item_rate_label.grid(
            row=1,
            column=3,
            padx=40
            )
itemRate = StringVar()
itemRate.set("")
item_rate = Entry(
            item_frame2,
            font=("segoe ui", 12),
            textvariable=itemRate,
            state=DISABLED, 
            width=14
            )
item_rate.grid(
            row=1,
            column=4,
            padx=10
            )
item_quantity_label = Label(
            item_frame2,
            text="Quantity",
            font=("segoe ui", 12, "bold"),
            bg = "#1778F2",
            fg="#ffeead"
            )
item_quantity_label.grid(
            row=2,
            column=0,
            padx=30,
            pady=15
            )
itemQuantity = StringVar()
itemQuantity.set("")
item_quantity = Entry(
            item_frame2, 
            font=("segoe ui", 12),
            textvariable=itemQuantity, 
            width=25
            )
item_quantity.grid(
            row=2,
            column=1
            )
item_frame3 = Frame(
            item_frame,
            bg="#1778F2"
            )
item_frame3.pack(
            fill=X
            )
add_button = ttk.Button(
            item_frame3, 
            text="Add Item", 
            command=add_button_operation
            )
add_button.grid(
            row=0,
            column=1,
            padx=40,
            pady=30
            )
remove_button = ttk.Button(
            item_frame3, 
            text="Remove Item", 
            command=remove_button_operation
            )
remove_button.grid(
            row=0,
            column=2,
            padx=40,
            pady=30
            )
update_button = ttk.Button(
            item_frame3, 
            text="Update Quantity", 
            command=update_button_operation
            )
update_button.grid(
            row=0,
            column=3,
            padx=40,
            pady=30
            )
clear_button = ttk.Button(
            item_frame3,
            text="Clear", 
            width=8,
            command=clear_button_operation
            )
clear_button.grid(
            row=0,
            column=4,
            padx=40,
            pady=30
            )
calc_button = ttk.Button(
            item_frame3,
            text="Open Calculator", 
            command=open_calculator
            )
calc_button.grid(
            row=0,
            column=5,
            padx=40,
            pady=30
            )

item_frame7 = Frame(
            root,
            bd=5,
            bg="#1778F2",
            relief=GROOVE
            )
item_frame7.place(
            x=1620,
            y=470,
            height=250,
            width=275
            )
item_title_label7 = Label(
            item_frame7,
            text="Options",
            font=("segoe ui", 20, "bold"),
            bg = "#1778F2", 
            fg="#ffeead"
            )
item_title_label7.grid(
            row = 0,
            column = 0
            )
calc_button = ttk.Button(
            item_frame7,
            text="Open Calculator", 
            command=open_calculator
            )
calc_button.grid(
            row=1,
            column=0,
            padx=76,
            pady=25
            )
show_bills_button = ttk.Button(
            item_frame7,
            text="Show Bills", 
            command=open_bills
            )
show_bills_button.grid(
            row=2,
            column=0,
            padx=0,
            pady=16
            )
show_customers_button = ttk.Button(
            item_frame7,
            text = "Customers Details",
            command=show_customers
            )
show_customers_button.grid(
            row=3,
            column=0,
            padx=0,
            pady=16
            )

#----------------------ORDER FRAME------------------------

order_frame = Frame(
            root,
            bd=5, 
            bg="#1778F2", 
            relief=GROOVE
            )
order_frame.place(
            x=980,
            y=470,
            height=530,
            width=600
            )
order_title_label = Label(
            order_frame, 
            text="Your Order", 
            font=("segoe ui", 20, "bold"),
            bg = "#1778F2", 
            fg="#ffeead"
            )
order_title_label.pack(
            side=TOP,
            fill="x"
            )

#----------------------ORDER TABLE------------------------

order_table_frame = Frame(
            order_frame
            )
order_table_frame.place(
            x=15,
            y=60,
            height=423,
            width=560
            )
scrollbar_order_x = Scrollbar(
            order_table_frame,
            orient=HORIZONTAL
            )
scrollbar_order_y = Scrollbar(
            order_table_frame,
            orient=VERTICAL
            )
order_table = ttk.Treeview(
            order_table_frame,
            columns =("name","rate","quantity","price","category"),
            xscrollcommand=scrollbar_order_x.set, 
            yscrollcommand=scrollbar_order_y.set
            )
order_table.heading(
            "name",
            text="Name"
            )
order_table.heading(
            "rate",
            text="Rate"
            )
order_table.heading(
            "quantity",
            text="Quantity"
            )
order_table.heading(
            "price",
            text="Price"
            )
order_table["displaycolumns"]=(
            "name", 
            "rate",
            "quantity",
            "price"
            )
order_table["show"] = (
            "headings"
            )
order_table.column(
            "rate",
            width=100,
            anchor='center', 
            stretch=NO
            )
order_table.column(
            "quantity",
            width=100,
            anchor='center', 
            stretch=NO
            )
order_table.column(
            "price",
            width=100,
            anchor='center',
            stretch=NO
            )
order_table.bind(
            "<ButtonRelease-1>",
            load_item_from_order
            )
scrollbar_order_x.pack(
            side=BOTTOM,
            fill=X
            )
scrollbar_order_y.pack(
            side=RIGHT,
            fill=Y
            )
scrollbar_order_x.configure(
            command=order_table.xview
            )
scrollbar_order_y.configure(
            command=order_table.yview
            )
order_table.pack(
            fill=BOTH,
            expand=1
            )

#----------------TOTAL PRICE FRAME--------------------

totalprice_frame = Frame(
            root,
            bd=5, 
            bg="#1778F2", 
            relief=GROOVE
            )
totalprice_frame.place(
            x=1620,
            y=750,
            height=250,
            width=275
            )
totalprice_title_label = Label(
            totalprice_frame, 
            text="Total Price", 
            font=("segoe ui", 20, "bold"),
            bg = "#1778F2", 
            fg="#ffeead"
            )
totalprice_title_label.pack(
            side=TOP,
            fill="x"
            )
totalPrice = StringVar()
totalPrice.set("")
total_price_entry = Label(
            totalprice_frame,
            bg = "#1778F2",
            fg = "white",
            font=("segoe ui", 70, "bold"),
            textvariable=totalPrice
            )
total_price_entry.pack(
            side=TOP,
            )
bill_button = ttk.Button(
            totalprice_frame, 
            text="Print Bill",
            width=10, 
            command=bill_button_operation
            )
bill_button.pack(
            side=LEFT,
            anchor=SW,
            padx=33,
            pady=10
            )
cancel_button = ttk.Button(
            totalprice_frame, 
            text="Clear Order",
            width=10,
            command=cancel_button_operation
            )
cancel_button.pack(
            side=LEFT,
            anchor=SW,
            padx=10,
            pady=10
            )

#------------------TOTAL PRICE LABEL----------------------
root.mainloop()
#---------------------------------------------------------------------------------------------------TKINTER GUI APPEARENCE END-------------------------------------------------------------------------------------------------------

