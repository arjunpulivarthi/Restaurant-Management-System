from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import os

p = '123'
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            
class EntryWithPlaceholderpass(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', show="*"):
        super().__init__(master)
        show="*"

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        show="*"

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            show="*"

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            show="*"

def login():
    global window
    window = Tk()
    window.geometry("1200x600")
    window.configure(bg = "#dfe3ee")
    style_button = ttk.Style()
    window.resizable(False, False)
    style_button.configure(
            "TButton",
            font = ("tahoma",10,"bold"), 
            background="#3b5998"
            )
    title_label = Label(
            window, 
            text="Fine Dine Restaurant",
            font=("segoe ui", 33, "bold"),
            bg = "#dfe3ee",
            fg="#1778F2",
            pady=10)
    title_byline = Label(
            window, 
            text="Enjoy the Taste of Heaven",
            font=("segoe ui", 17),
            bg = "#dfe3ee",
            fg="black",
            )
    title_label.place(
            x = 100,
            y = 150
            )
    title_byline.place(
            x = 100,
            y = 230
            )
    body_frame = Frame(
            window, 
            bd=0, 
            bg="white", 
            relief=GROOVE
            )
    body_frame.place(
            x=620,
            y=120,
            height=360,
            width=440
            )
    dummy_label= Label(
            body_frame,
            text= "                              ", 
            bg = "white", 
            fg = "#ffc425",
            pady = 40
            )
    dummy_label.grid(
            row = 0, 
            column = 1
            )

    usern = EntryWithPlaceholder(
        body_frame,
        "Enter Username"
        )
    usern.grid(
        row = 0,
        column = 1
        )
    usern.configure(width = 20,
                    font = ("calibri", 17),
                    bd = 2,
                    relief = "groove")

    passw = EntryWithPlaceholderpass(
        body_frame,
        "Enter Password"
        )
    passw.grid(
         row = 1,
         column = 1
         )
    passw.config(bd=2,
                 width = 20,
                 font = ("calibri", 18),
                 relief = "groove")
    dummy_label= Label(
            body_frame,
            text= "                              ", 
            bg = "white", 
            fg = "#dfe3ee",
            pady = 30
            )
    dummy_label.grid(
            row = 3, 
            column = 0
            )
    login_button = Button(
        body_frame,
        text="Log In",
        width = 20,
        height  = 2,
        bg = "#1778F2",
        fg = "white",
        bd = 0,
        font=("segoe ui", 13, "bold"),
        command=lambda:loginok(usern.get(),passw.get())
        )
    login_button.grid(
        row = 4,
        column = 1
        )
    forgot_button = Button(
        body_frame,
        text="Forgotten Password?",
        width = 15,
        height  = 2,
        bg = "white",
        fg = "#3b5998",
        bd = 0,
        font=("segoe ui", 13),
        command=cpass
        )
    forgot_button.grid(
        row = 5,
        column = 1
        )
    copyright_label = Label(
        window,
        text = "Programmed by Arjun Pulivarthi and Gurunandhan",
        font = ("segoe ui", 10),
        bg = "#dfe3ee"
        )
    copyright_label.place(x = 100,
                          y = 460)
    window.mainloop()

def loginok(username,password):
    global p
    if username == "admin":
        if password == p:
            os.system(r"C:\Users\arpul\OneDrive\Desktop\RESTAURANT\main.py")
            window.destroy()
        else:
            messagebox.showerror("Login Failed!","Wrong Password")
    else:
        messagebox.showerror("Login Failed!","Wrong Username")

def cpass():
    global window
    window.destroy()
    window = Tk()
    Label(window,text="Enter new password:").pack()
    passn = Entry(window,width=15)
    passn.pack()
    Button(window,text="OK",command=lambda:chgpass(passn.get())).pack()
    window.mainloop()

def chgpass(newpass):
    global window
    global p
    p = newpass
    window.destroy()
    login()

login()
