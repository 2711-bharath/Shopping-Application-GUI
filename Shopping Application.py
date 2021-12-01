import time
import sqlite3
import pandas as pd
from tkinter import *
from tkinter import ttk
from numpy import random
from tkinter import messagebox
from datetime import datetime, timedelta, date


# =======================================DATABASE AND TABLES=======================================

def Database():
    global conn, cursor
    conn = sqlite3.connect ("Online Shopping.db")
    cursor = conn.cursor ()

    # Customer table

    conn.execute ('''
        create table if not exists users(
        username varchar2(15) not null,
        fname varchar2(10) not null,
        lname varchar2(10) not null,
        phoneno varchar2(10),
        email varchar2(20) primary key not null,
        password varchar2(10) not null,
        address varchar2(10) not null
        );
        ''')

    # Product table

    conn.execute ('''
    create table if not exists products(
    pid varchar2(15) primary key not NULL,
  	cartid varchar2(15) not NULL,
    price varchar2(5) not NULL,
    name varchar2(15) not NULL,
    quantity varchar2(3) NOT NULL
    );
    ''')

    # Cart List

    conn.execute ('''
    create table if not exists cart(
    cartid varchar2(6) primary key not null,
    amount varchar2(5) not null,
  	shipmentime varchar2(10) Not null,
  	delivertime vachar2(10) NOT null,
  	address varchar2(20) Not NULL,
  	paytype varchar2(4) check(paytype='Cash' or paytype='Card')
    );
    ''')

    # Payment Lists

    conn.execute ('''
    create table if not exists payment(
    payid varchar2(10) primary key not null,
    amount varchar2(5) not null,
    paytype varchar2(4) check(paytype='Cash' or paytype='Debited' or paytype='Credited'),
    paytime varchar2(10) Not null
    );
    ''')


# =======================================REGISTRATION=======================================

def registration():
    Register = Tk ()
    Register.title ("Online Shopping Application")

    ws = Register.winfo_screenwidth ()
    hs = Register.winfo_screenheight ()
    x = (ws / 2) - (600 / 2)
    y = (hs / 2) - (500 / 2)
    Register.geometry ('%dx%d+%d+%d' % (600, 500, x, y))
    Database ()

    def checkRegistration(event = None):
        try:
            x = int (PHONE.get ())
        except:
            messagebox.showerror (title = 'ERROR', message = "Enter valid phone number")
            PHONE.set("")
        if len(x)!=10:
            messagebox.showerror (title = 'ERROR', message = "Enter valid phone number")
            PHONE.set("")

        if USERNAME.get () == "" or FNAME.get () == "" or PHONE.get () == "" or PASSWORD.get () == "" or ADDRESS.get () == "" or EMAIL.get () == "":

            Label (Register, text = "Please complete the required field!", fg = "red").grid (row = 8, column = 1)
        else:

            cursor.execute ("SELECT email FROM users WHERE email = ? or username = ?", [EMAIL.get (),USERNAME.get()])
            if cursor.fetchone () is None:
                Label (Register, text = "", fg = "red").grid (row = 8, column = 1)
                try:
                    cursor.execute ("Insert into users values(?,?,?,?,?,?,?)", (
                        USERNAME.get (), FNAME.get (), LNAME.get (), PHONE.get (), EMAIL.get (), PASSWORD.get (),
                        ADDRESS.get ()))
                    conn.commit ()
                    messagebox.showinfo (title = 'Registration', message = 'Account Created')
                    Register.destroy ()
                    HomeWindow (USERNAME.get ())
                except Exception as e:
                    messagebox.showerror (title = "ERROR", message = e)
            else:
                messagebox.showerror (title = 'ERROR', message = "Already account exists with this email or username")
                Label (Register, text = "Already account exists with this email", fg = "red").grid (row = 8, column = 1)

    # ==============================VARIABLES======================================

    USERNAME = StringVar ()
    PASSWORD = StringVar ()
    FNAME = StringVar ()
    LNAME = StringVar ()
    PHONE = StringVar ()
    EMAIL = StringVar ()
    ADDRESS = StringVar ()

    # ==============================LABELS=================================

    Label (Register, text = "Registraion Form", font = ('arial', 25), bd = 15, fg = "SlateBlue").grid (
        padx = 20, row = 0,
        column = 1,columnspan=2)
    Label (Register, text = "Username:", font = ('arial', 14)).grid (pady = 10, padx = 20, row = 1,
                                                                                    column = 0)
    Label (Register, text = "First Name:", font = ('arial', 14)).grid (pady = 10, padx = 20, row = 2,
                                                                                   column = 0)
    Label (Register, text = "Last Name:", font = ('arial', 14)).grid (pady = 10, padx = 20, row = 3,
                                                                                  column = 0)
    Label (Register, text = "Contact Number:", font = ('arial', 14)).grid (pady = 10, padx = 20, row = 4,
                                                                                       column = 0)
    Label (Register, text = "Email Id:", font = ('arial', 14)).grid (pady = 10, padx = 20, row = 5,
                                                                                 column = 0)
    Label (Register, text = "Password:", font = ('arial', 14)).grid (pady = 10, padx = 20, row = 6,
                                                                                    column = 0)
    Label (Register, text = "Address:", font = ('arial', 14)).grid (pady = 10, padx = 20, row = 7,
                                                                                  column = 0)

    # ==============================ENTRY=================================

    Entry (Register, textvariable = USERNAME, font = (14), width = "25").grid (row = 1, column = 1)
    Entry (Register, textvariable = FNAME, font = (14), width = "25").grid (row = 2, column = 1)
    Entry (Register, textvariable = LNAME, font = (14), width = "25").grid (row = 3, column = 1)
    Entry (Register, textvariable = PHONE, font = (14), width = "25").grid (row = 4, column = 1)
    Entry (Register, textvariable = EMAIL, font = (14), width = "25").grid (row = 5, column = 1)
    Entry (Register, textvariable = PASSWORD, show = "*", font = (14), width = "25").grid (row = 6, column = 1)
    Entry (Register, textvariable = ADDRESS, font = (14), width = "25").grid (row = 7, column = 1)

    def back():
        Register.destroy ()
        Login ()

    # ==============================BUTTON WIDGETS=================================

    btn_submit = Button (Register, text = 'Submit', width = 25, command = checkRegistration,activebackground="spring green")
    btn_submit.grid (row = 13, column = 1)
    Button (Register, text = 'Login', width = 25, command = back,activebackground="tomato",activeforeground="snow").grid (pady = 10, row = 14, column = 1)
    Register.mainloop ()

# =======================================HOME WINDOW=======================================

# =======================================Variables For Product Count=======================================

c_laptop = 0
c_phone = 0
c_tablet = 0
c_tv = 0
c_earphones = 0
c_camera = 0
c_watch = 0
c_apple = 0
c_onion = 0
c_banana = 0
c_orange = 0
c_tomato = 0
c_promogranate = 0
c_potato = 0
c_purifiers = 0
c_mixer = 0
c_bottle = 0
c_bulb = 0
c_pans = 0
c_oven = 0
c_washingmachine = 0
tempc = 0

def HomeWindow(Username):
    Database ()

    # =======================================Cart=======================================
    '''
    Shows the products we choose
    '''

    def Cart():

        shop.iconify ()
        cart = Tk ()
        cart.title ("Online Shopping Application")

        ws = cart.winfo_screenwidth ()
        hs = cart.winfo_screenheight ()
        x = (ws / 2) - (560 / 2)
        y = (hs / 2) - (600 / 2)
        cart.geometry ('%dx%d+%d+%d' % (560, 600, x, y))
        cart.resizable (0, 0)

        # =======================================Payment=======================================
        '''
        Displays payment screen
        '''

        def Payment():

            cart.destroy ()
            # print(Address1.get())
            def back1():
                payment.destroy ()
                shop.deiconify ()

            payment = Tk ()
            payment.title ("Online Shopping Application")

            ws = payment.winfo_screenwidth ()
            hs = payment.winfo_screenheight ()
            x = (ws / 2) - (500 / 2)
            y = (hs / 2) - (400 / 2)
            payment.geometry ('%dx%d+%d+%d' % (500, 400, x, y))
            payment.resizable (0, 0)

            var = StringVar (payment, "1")
            cardno = StringVar (payment)
            cvv = StringVar (payment)
            carduser = StringVar (payment)

            Label (payment, text = "Payment ", font = ('arial', 15), fg = "light slate blue").place (x = 250, y = 20,
                                                                                                     anchor = CENTER)

            Radiobutton (payment, text = "Online Payment", variable = var, value = 1, font = ('arial', 12),
                         fg = "RoyalBlue1").place (
                x = 50, y = 50)

            Label (payment, text = "Card no", font = ('arial', 11)).place (x = 70, y = 100)
            Label (payment, text = "CVV", font = ('arial', 11)).place (x = 70, y = 130)
            Label (payment, text = "Card Holder Name", font = ('arial', 11)).place (x = 70, y = 160)
            Label (payment, text = "Amount", font = ('arial', 11)).place (x = 70, y = 190)

            Entry (payment, textvariable = cardno, font = ('arial', 11), width = 25).place (x = 200, y = 100)
            Entry (payment, textvariable = cvv, show = "*", font = ('arial', 11), width = 25).place (x = 200, y = 130)
            Entry (payment, textvariable = carduser, font = ('arial', 11), width = 25).place (x = 200, y = 160)
            Label (payment, text = Amount.get (), font = ('arial', 11)).place (x = 200, y = 190)

            Radiobutton (payment, text = "Payment After Delivery", variable = var, value = 2, fg = "RoyalBlue1",
                         font = ('arial', 12)).place (x = 50, y = 250)

            # =======================================Data inserted to Cart=======================================

            def enter_in_cart(method):

                global c_apple, c_banana, c_orange, c_promogranate, c_tomato, c_potato, c_onion
                global c_phone, c_earphones, c_laptop, c_camera, c_watch, c_tv, c_tablet
                global c_purifiers, c_mixer, c_bottle, c_bulb, c_oven, c_washingmachine, c_pans
                now = datetime.now ()
                cdate = (now.strftime ("%d-%m-%Y %H:%M:%S"))
                today = date.today ()
                d1 = today.strftime ("%d-%m-%Y")
                ddate = (datetime.strptime (d1, '%d-%m-%Y') + timedelta (days = 3)).strftime ('%d-%m-%Y')

                # print(cdate)
                # print(ddate)
                # print(Amount.get())

                c = 1
                list1 = cursor.execute ("SELECT cartid FROM cart").fetchall ()
                if list1 is None:
                    cartid = str (Username + str (c))
                else:
                    cartid = str (Username + str (c))
                    for cartid in list1:
                        c += 1
                        cartid = str (Username + str (c))

                c = 1
                list1 = cursor.execute ("SELECT payid FROM payment").fetchall ()
                if list1 is None:
                    pid = str (Username + str (c))
                else:
                    pid = str (Username + str (c))
                    for pid in list1:
                        c += 1
                        pid = str (Username + str (c))
                pid = str(pid+cartid)
                # print(pid)
                if method == 'Cash':
                    cursor.execute ("Insert into cart values(?,?,?,?,?,?)",(cartid, Amount.get (), cdate, ddate, Address1.get (),"Cash"))
                    cursor.execute ("Insert into payment values(?,?,?,?)", (pid, Amount.get (), method, ddate))
                else:

                    cursor.execute ("Insert into cart values(?,?,?,?,?,?)",(cartid, Amount.get (), cdate, ddate, Address1.get (),"Card"))
                    cursor.execute ("Insert into payment values(?,?,?,?)", (pid, Amount.get (), method, cdate))
                conn.commit ()
                count.set (0)

                c = 1;
                if c_apple != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_apple * 50), 'Apple', str (c_apple)))
                    c_apple = 0
                    conn.commit ()

                if c_banana != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_banana * 30), 'Banana', str (c_banana)))
                    conn.commit ()
                    c_banana = 0

                if c_orange != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_orange * 45), 'Orange', str (c_orange)))
                    conn.commit ()
                    c_orange = 0

                if c_promogranate != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_promogranate * 90), 'Promagranate', str (c_promogranate)))
                    conn.commit ()
                    c_promogranate = 0

                if c_tomato != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_tomato * 40), 'Tomato', str (c_tomato)))
                    conn.commit ()
                    c_tomato = 0

                if c_potato != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_potato * 53), 'Potato', str (c_potato)))
                    conn.commit ()
                    c_potato = 0

                if c_onion != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_onion * 89), 'Banana', str (c_onion)))
                    conn.commit ()
                    c_onion = 0

                if c_phone != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_phone * 32000), 'Phone', str (c_phone)))
                    conn.commit ()
                    c_phone = 0

                if c_laptop != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_laptop * 56000), 'Laptop', str (c_laptop)))
                    conn.commit ()
                    c_laptop = 0

                if c_earphones != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_earphones * 2499), 'Earphones', str (c_earphones)))
                    conn.commit ()
                    c_earphones = 0

                if c_camera != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_camera * 29000), 'Camera', str (c_camera)))
                    conn.commit ()
                    c_camera = 0

                if c_watch != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_watch * 2500), 'Fitness Band', str (c_watch)))
                    conn.commit ()
                    c_watch = 0

                if c_tv != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_tv * 70000), 'LED TV', str (c_tv)))
                    conn.commit ()
                    c_tv = 0

                if c_tablet != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_tablet * 45000), 'iPad', str (c_tablet)))
                    conn.commit ()
                    c_tablet = 0

                if c_purifiers != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_purifiers * 9000), 'Water Purifiers', str (c_purifiers)))
                    conn.commit ()
                    c_purifiers = 0

                if c_mixer != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_mixer * 3500), 'Mixer', str (c_mixer)))
                    conn.commit ()
                    c_mixer = 0

                if c_bottle != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_bottle * 700), 'Copper Bottle', str (c_bottle)))
                    conn.commit ()
                    c_bottle = 0

                if c_bulb != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_bulb * 600), 'LED Bulb', str (c_bulb)))
                    conn.commit ()
                    c_bulb = 0

                if c_oven != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_oven * 8000), 'Microoven', str (c_oven)))
                    conn.commit ()
                    c_oven = 0

                if c_pans != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_pans * 3700), 'Kitchen Sets', str (c_pans)))
                    conn.commit ()
                    c_pans = 0

                if c_washingmachine != 0:
                    pid = cartid + '00' + str (c)
                    c += 1
                    cursor.execute ("Insert into products values(?,?,?,?,?)",
                                    (pid, cartid, str (c_washingmachine * 42000), 'Washing Machine',
                                     str (c_washingmachine)))
                    conn.commit ()
                    c_washingmachine = 0
                Amount.set (0)
                payment.destroy ()

            '''
            Shows the payment method you choosed
            '''

            def showChoise():

                if var.get () == '1':

                    # print(cardno.get(),cvv.get(),carduser.get())
                    if cardno.get () == "" or cvv.get () == "" or carduser.get () == "" or Amount.get () == 0:
                        Label (payment, text = "Please complete the required field!", fg = "red",
                               font = ('arial', 11)).place (x = 250, y = 230, anchor = CENTER)
                    else:

                        enter_in_cart ("Debited")
                        messagebox.showinfo ("Payment", "Your order is successful placed!!!")
                        shop.deiconify ()

                else:
                    if Amount.get () != 0:
                        enter_in_cart ("Cash")
                        messagebox.showinfo ("Payment", "Your order is successful placed!!!")
                        shop.deiconify ()

                    else:
                        messagebox.showinfo ("Payment", "Pick minimum a Single Item")

            Button (payment, text = 'Proceed', command = showChoise, width = 25, font = ('arial', 10), bg = "tomato",
                    fg = "snow").place (x = 250,
                                        y = 300,
                                        anchor = CENTER)
            Button (payment, text = 'Back to home', command = back1, width = 25, font = ('arial', 10), bg = "gray54",
                    fg = "snow").place (x = 250,
                                        y = 350,
                                        anchor = CENTER)

            payment.mainloop ()
            return

        main_frame = Frame (cart)
        main_frame.pack (fill = BOTH, expand = 1)

        my_Canvas = Canvas (main_frame)
        my_Canvas.pack (side = LEFT, fill = BOTH, expand = 1)

        my_scrollbar = ttk.Scrollbar (main_frame, orient = VERTICAL, command = my_Canvas.yview)
        my_scrollbar.pack (side = RIGHT, fill = Y)

        my_Canvas.configure (yscrollcommand = my_scrollbar.set)
        my_Canvas.bind ('<Configure>', lambda e:my_Canvas.configure (scrollregion = my_Canvas.bbox ("all")))

        second_frame = Frame (my_Canvas)

        my_Canvas.create_window ((0, 0), window = second_frame, anchor = "nw")

        Label (second_frame, text = 'CART Items', font = "Verdana 15 underline", fg = "SlateBlue1").grid (row = 0,
                                                                                                          column = 1,
                                                                                                          padx = 5,
                                                                                                          pady = 5,columnspan=3)
        Label (second_frame, text = "Product Id", font = ('arial', 11), fg = "RoyalBlue1").grid (row = 1, column = 0,
                                                                                                 padx = 5, pady = 5)
        Label (second_frame, text = "Product Name", font = ('arial', 11), fg = "RoyalBlue1").grid (row = 1, column = 1,
                                                                                                   padx = 5, pady = 5)
        Label (second_frame, text = "Quantity", font = ('arial', 11), fg = "RoyalBlue1").grid (row = 1, column = 2,
                                                                                               padx = 5, pady = 5)
        Label (second_frame, text = "Cost", font = ('arial', 11), fg = "RoyalBlue1").grid (row = 1, column = 3,
                                                                                           padx = 5, pady = 5)
        c = 2
        nc = 0

        def remove1():
            global c_apple
            if c_apple != 0:
                c_apple -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 50)
            cart.destroy ()
            Cart ()

        if c_apple != 0:
            Label (second_frame, text = "fruits1", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Apple", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_apple), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                   pady = 5)
            Label (second_frame, text = str (c_apple * 50), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                        pady = 5)
            Button (second_frame, text = 'Remove', command = remove1).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove2():
            global c_banana
            if c_banana != 0:
                c_banana -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 30)
            cart.destroy ()
            Cart ()

        if c_banana != 0:
            Label (second_frame, text = "fruits2", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Banana", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_banana), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_banana * 30), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                         pady = 5)
            Button (second_frame, text = 'Remove', command = remove2).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove3():
            global c_orange
            if c_orange != 0:
                c_orange -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 45)
            cart.destroy ()
            Cart ()

        if c_orange != 0:
            Label (second_frame, text = "fruits3", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Orange", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_orange), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_orange * 45), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                         pady = 5)
            Button (second_frame, text = 'Remove', command = remove3).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove4():
            global c_promogranate
            if c_promogranate != 0:
                c_promogranate -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 90)
            cart.destroy ()
            Cart ()

        if c_promogranate != 0:
            Label (second_frame, text = "fruits4", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Promogranate", font = ('arial', 10)).grid (row = c, column = 1, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_promogranate), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                          pady = 5)
            Label (second_frame, text = str (c_promogranate * 90), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                               padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove4).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove5():
            global c_tomato
            if c_tomato != 0:
                c_tomato -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 40)
            cart.destroy ()
            Cart ()

        if c_tomato != 0:
            Label (second_frame, text = "Vegetable1", font = ('arial', 10)).grid (row = c, column = 0, padx = 5,
                                                                                  pady = 5)
            Label (second_frame, text = "Tomato", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_tomato), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_tomato * 40), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                         pady = 5)
            Button (second_frame, text = 'Remove', command = remove5).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove6():
            global c_potato
            if c_potato != 0:
                c_potato -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 53)
            cart.destroy ()
            Cart ()

        if c_potato != 0:
            Label (second_frame, text = "Vegetable", font = ('arial', 10)).grid (row = c, column = 0, padx = 5,
                                                                                 pady = 5)
            Label (second_frame, text = "Potato", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_potato), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_potato * 53), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                         pady = 5)
            Button (second_frame, text = 'Remove', command = remove6).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove7():
            global c_onion
            if c_onion != 0:
                c_onion -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 89)
            cart.destroy ()
            Cart ()

        if c_onion != 0:
            Label (second_frame, text = "Vegetable3", font = ('arial', 10)).grid (row = c, column = 0, padx = 5,
                                                                                  pady = 5)
            Label (second_frame, text = "Onion", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_onion), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                   pady = 5)
            Label (second_frame, text = str (c_onion * 89), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                        pady = 5)
            Button (second_frame, text = 'Remove', command = remove7).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove8():
            global c_phone
            if c_phone != 0:
                c_phone -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 32000)
            cart.destroy ()
            Cart ()

        if c_phone != 0:
            Label (second_frame, text = "Device1", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Phone", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_phone), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                   pady = 5)
            Label (second_frame, text = str (c_phone * 32000), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                           padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove8).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove9():
            global c_laptop
            if c_laptop != 0:
                c_laptop -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 56000)
            cart.destroy ()
            Cart ()

        if c_laptop != 0:
            Label (second_frame, text = "Device2", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Laptop", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_laptop), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_laptop * 56000), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                            padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove9).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove10():
            global c_earphones
            if c_earphones != 0:
                c_earphones -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 2499)
            cart.destroy ()
            Cart ()

        if c_earphones != 0:
            Label (second_frame, text = "Device3", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Earphones", font = ('arial', 10)).grid (row = c, column = 1, padx = 5,
                                                                                 pady = 5)
            Label (second_frame, text = str (c_earphones), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                       pady = 5)
            Label (second_frame, text = str (c_earphones * 2499), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                              padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove10).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove11():
            global c_camera
            if c_camera != 0:
                c_camera -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 29000)
            cart.destroy ()
            Cart ()

        if c_camera != 0:
            Label (second_frame, text = "Device4", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Camera", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_camera), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_camera * 29000), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                            padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove11).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove12():
            global c_watch
            if c_watch != 0:
                c_watch -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 21490)
            cart.destroy ()
            Cart ()

        if c_watch != 0:
            Label (second_frame, text = "Device5", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Fitness Band", font = ('arial', 10)).grid (row = c, column = 1, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_watch), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                   pady = 5)
            Label (second_frame, text = str (c_watch * 21490), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                           padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove12).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove13():
            global c_tv
            if c_tv != 0:
                c_tv -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 70000)
            cart.destroy ()
            Cart ()

        if c_tv != 0:
            Label (second_frame, text = "Device6", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "LED TV", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_tv), font = ('arial', 10)).grid (row = c, column = 2, padx = 5, pady = 5)
            Label (second_frame, text = str (c_tv * 70000), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                        pady = 5)
            Button (second_frame, text = 'Remove', command = remove13).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove14():
            global c_tablet
            if c_tablet != 0:
                c_tablet -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 45000)
            cart.destroy ()
            Cart ()

        if c_tablet != 0:
            Label (second_frame, text = "Device7", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Tables", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_tablet), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_tablet * 45000), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                            padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove14).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove15():
            global c_purifiers
            if c_purifiers != 0:
                c_purifiers -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 9000)
            cart.destroy ()
            Cart ()

        if c_purifiers != 0:
            Label (second_frame, text = "House1", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Water Purifier", font = ('arial', 10)).grid (row = c, column = 1, padx = 5,
                                                                                      pady = 5)
            Label (second_frame, text = str (c_purifiers), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                       pady = 5)
            Label (second_frame, text = str (c_purifiers * 9000), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                              padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove15).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove16():
            global c_mixer
            if c_mixer != 0:
                c_mixer -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 3500)
            cart.destroy ()
            Cart ()

        if c_mixer != 0:
            Label (second_frame, text = "House2", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Mixer", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_mixer), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                   pady = 5)
            Label (second_frame, text = str (c_mixer * 3500), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                          pady = 5)
            Button (second_frame, text = 'Remove', command = remove16).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove17():
            global c_bottle
            if c_bottle != 0:
                c_bottle -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 700)
            cart.destroy ()
            Cart ()

        if c_bottle != 0:
            Label (second_frame, text = "House3", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Bottle", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_bottle), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                    pady = 5)
            Label (second_frame, text = str (c_bottle * 700), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                          pady = 5)
            Button (second_frame, text = 'Remove', command = remove17).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove18():
            global c_bulb
            if c_bulb != 0:
                c_bulb -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 600)
            cart.destroy ()
            Cart ()

        if c_bulb != 0:
            Label (second_frame, text = "House4", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "LED Bulb", font = ('arial', 10)).grid (row = c, column = 1, padx = 5, pady = 5)
            Label (second_frame, text = str (c_bulb), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                  pady = 5)
            Label (second_frame, text = str (c_bulb * 600), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                        pady = 5)
            Button (second_frame, text = 'Remove', command = remove18).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove19():
            global c_oven
            if c_oven != 0:
                c_oven -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 8000)
            cart.destroy ()
            Cart ()

        if c_oven != 0:
            Label (second_frame, text = "House5", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Microwave Oven", font = ('arial', 10)).grid (row = c, column = 1, padx = 5,
                                                                                      pady = 5)
            Label (second_frame, text = str (c_oven), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                  pady = 5)
            Label (second_frame, text = str (c_oven * 8000), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                         pady = 5)
            Button (second_frame, text = 'Remove', command = remove19).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove20():
            global c_pans
            if c_pans != 0:
                c_pans -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 3700)
            cart.destroy ()
            Cart ()

        if c_pans != 0:
            Label (second_frame, text = "House6", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Kitchen Set", font = ('arial', 10)).grid (row = c, column = 1, padx = 5,
                                                                                   pady = 5)
            Label (second_frame, text = str (c_pans), font = ('arial', 10)).grid (row = c, column = 2, padx = 5,
                                                                                  pady = 5)
            Label (second_frame, text = str (c_pans * 3700), font = ('arial', 10)).grid (row = c, column = 3, padx = 5,
                                                                                         pady = 5)
            Button (second_frame, text = 'Remove', command = remove20).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def remove21():

            global c_washingmachine
            if c_washingmachine != 0:
                c_washingmachine -= 1
                count.set (count.get () - 1)
                Amount.set (Amount.get () - 42000)
            cart.destroy ()
            Cart ()

        if c_washingmachine != 0:

            Label (second_frame, text = "House7", font = ('arial', 10)).grid (row = c, column = 0, padx = 5, pady = 5)
            Label (second_frame, text = "Washing Machine", font = ('arial', 10)).grid (row = c, column = 1, padx = 5,
                                                                                       pady = 5)
            Label (second_frame, text = str (c_washingmachine), font = ('arial', 10)).grid (row = c, column = 2,
                                                                                            padx = 5, pady = 5)
            Label (second_frame, text = str (c_washingmachine * 42000), font = ('arial', 10)).grid (row = c, column = 3,
                                                                                                    padx = 5, pady = 5)
            Button (second_frame, text = 'Remove', command = remove21).grid (row = c, column = 4, padx = 5, pady = 5)
            c += 1
            nc += 1

        def back():
            cart.destroy ()
            shop.deiconify ()

        Label (second_frame, text = "Total Bill -", font = ('arial', 10)).grid (row = c, column = 3, padx = 5, pady = 5)
        Label (second_frame, text = Amount.get (), font = ('arial', 10)).grid (row = c, column = 4, padx = 5, pady = 5)
        c+=1
        Label (second_frame, text = "Address", font = ('arial', 11)).grid (row = c, column = 0, padx = 5, pady = 5)
        Address1 = StringVar(cart)
        Entry (second_frame, text = Address1, font = ('arial', 12),width=40).grid (row = c, column = 1, padx = 5, pady = 5,columnspan=4)

        def checkAddress():
            # print(Address1.get(),Amount.get())
            if Address1.get()=="":
                messagebox.showerror("Warning", "Please fill the Address feild!!!")
            elif Amount.get()==0:
                messagebox.showerror("Warning", "Please select minimum 1 product to buy!!!")
            else:
                Payment()

        c += 1
        Button (second_frame, text = "Proceed to Buy", width = 20, font = ('arial', 10), command = checkAddress,
                bg = "tomato", fg = "snow").grid (row = c, column = 2, padx = 5, pady = 5)
        c+=1
        Button (second_frame, text = 'Back', width = 20, font = ('arial', 10), command = back, bg = "gray54",
                fg = "snow").grid (row = c, column = 2, padx = 5, pady = 5)

        cart.mainloop ()

    def userDetails():
        Database ()
        shop.iconify ()
        users = Tk ()
        users.title ('Online Shopping Application')
        users.resizable (0, 0)

        ws = users.winfo_screenwidth ()
        hs = users.winfo_screenheight ()
        x = (ws / 2) - (500 / 2)
        y = (hs / 2) - (550 / 2)
        users.geometry ('%dx%d+%d+%d' % (500, 550, x, y))

        def displayCart():
            try:
                users.destroy ()
            except:
                pass
            list = cursor.execute ("SELECT * FROM cart where cartid Like ? ", (Username + '%',)).fetchall ()
            # print(list)

            Orders = Tk ()
            Orders.title ('Orders')
            cartno = StringVar (Orders)
            flag = StringVar (Orders)

            ws = Orders.winfo_screenwidth ()
            hs = Orders.winfo_screenheight ()
            x = (ws / 2) - (550 / 2)
            y = (hs / 2) - (400 / 2)

            Orders.geometry ('%dx%d+%d+%d' % (550, 400, x, y))
            Orders.resizable (0, 0)

            main_frame = Frame (Orders)
            main_frame.pack (fill = BOTH, expand = 1)

            my_Canvas = Canvas (main_frame)
            my_Canvas.pack (side = LEFT, fill = BOTH, expand = 1)

            my_scrollbar = ttk.Scrollbar (main_frame, orient = VERTICAL, command = my_Canvas.yview)
            my_scrollbar.pack (side = RIGHT, fill = Y)

            my_Canvas.configure (yscrollcommand = my_scrollbar.set)
            my_Canvas.bind ('<Configure>', lambda e:my_Canvas.configure (scrollregion = my_Canvas.bbox ("all")))

            second_frame = Frame (my_Canvas)
            cartno.set ("")
            flag.set (0)

            my_Canvas.create_window ((0, 0), window = second_frame, anchor = "nw")

            def displayProducts():

                cartid = Username + str (cartno.get ())
                # print(cartid)
                list1 = cursor.execute ("SELECT * FROM products where cartid = ? ", (cartid,)).fetchall ()
                # print(list1)
                if cartno.get () == "":
                    messagebox.showerror ("Error", "Enter Cart No")
                elif list1 == []:
                    cartno.set ("")
                    messagebox.showerror ("Error", "Enter Valid Cart No")

                else:
                    # print(flag.get())
                    if (flag.get () == '0'):
                        Orders.destroy ()

                        Products = Tk ()

                        ws = Products.winfo_screenwidth ()
                        hs = Products.winfo_screenheight ()
                        x = (ws / 2) - (420 / 2)
                        y = (hs / 2) - (400 / 2)
                        Products.geometry ('%dx%d+%d+%d' % (420, 400, x, y))
                        Products.resizable (0, 0)

                        main_frame = Frame (Products)
                        main_frame.pack (fill = BOTH, expand = 1)

                        my_Canvas = Canvas (main_frame)
                        my_Canvas.pack (side = LEFT, fill = BOTH, expand = 1)

                        my_scrollbar = ttk.Scrollbar (main_frame, orient = VERTICAL, command = my_Canvas.yview)
                        my_scrollbar.pack (side = RIGHT, fill = Y)

                        my_Canvas.configure (yscrollcommand = my_scrollbar.set)
                        my_Canvas.bind ('<Configure>',
                                        lambda e:my_Canvas.configure (scrollregion = my_Canvas.bbox ("all")))

                        second_frame = Frame (my_Canvas)

                        my_Canvas.create_window ((0, 0), window = second_frame, anchor = "nw")

                        Label (second_frame, text = "Products in cart " + cartno.get (), font = ('arial', 12),
                               fg = "SlateBlue1").grid (row = 1, column = 1, pady = 5, padx = 8)
                        Label (second_frame, text = 'Product Name', font = ('arial', 10), fg = "RoyalBlue1").grid (
                            row = 3, column = 0, pady = 5, padx = 8)
                        Label (second_frame, text = 'Quantity', font = ('arial', 10), fg = "RoyalBlue1").grid (row = 3,
                                                                                                               column = 1,
                                                                                                               pady = 5,
                                                                                                               padx = 8)
                        Label (second_frame, text = 'Price', font = ('arial', 10), fg = "RoyalBlue1").grid (row = 3,
                                                                                                            column = 2,
                                                                                                            pady = 5,
                                                                                                            padx = 8)
                        c = 4
                        for values in list1:
                            Label (second_frame, text = values[3], font = ('arial', 10)).grid (row = c, column = 0,
                                                                                               pady = 5, padx = 8)
                            Label (second_frame, text = values[4], font = ('arial', 10)).grid (row = c, column = 1,
                                                                                               pady = 5, padx = 8)
                            Label (second_frame, text = values[2], font = ('arial', 10)).grid (row = c, column = 2,
                                                                                               pady = 5, padx = 8)
                            c += 1

                        def back():
                            Products.destroy ()
                            displayCart ()
                        address = cursor.execute ("SELECT address FROM cart where cartid = ? ", (cartid,)).fetchone()
                        # print(address)
                        address = address[0]
                        Label (second_frame, text = "Address", font = ('arial', 11),fg="blue").grid (row = c, column = 0,
                                                                                           pady = 5, padx = 8)
                        c+=1
                        first = 0
                        end = len(address)
                        while first<end:
                            try:
                                Label (second_frame, text =address[first:50], font = ('arial', 10)).grid (row = c, column = 0,
                                                                                               pady = 5, padx = 8,columnspan=3)
                            except:
                                Label (second_frame, text =address[first:], font = ('arial', 10)).grid (row = c, column = 0,
                                                                                         pady = 5, padx = 8,
                                                                                         columnspan = 3)
                            c+=1
                            first+=50

                        Button (second_frame, text = "Back", command = back, width = 25, bg = "gray54",
                                fg = "snow").grid (row = c, column = 1, pady = 5, padx = 8)
                        Products.mainloop ()
                    else:
                        # print(cartid)
                        list1 = cursor.execute ("SELECT * FROM cart where cartid = ? ", (cartid,)).fetchall ()
                        # print(list1)
                        if list1 is []:
                            messagebox ("Error", "No cart exists")
                        else:
                            # print(list)
                            date1 = date.today ()
                            date2 = pd.to_datetime (list1[0][3], dayfirst = True)

                            if date1 < date2:
                                # print ("hello")

                                cursor.execute ("DELETE FROM cart where cartid = ? ", (cartid,))
                                cursor.execute ("DELETE FROM products where cartid = ? ", (cartid,))
                                messagebox.showinfo("message","Your order is cancelled")
                                conn.commit ()
                                if(list1[0][5]=="Card"):
                                    c = 1
                                    list2 = cursor.execute ("SELECT payid FROM payment").fetchall ()
                                    if list2 is None:
                                        pid = str (Username + str (c))
                                    else:
                                        pid = str (Username + str (c))
                                        for pid in list2:
                                            c += 1
                                            pid = str (Username + str (c))
                                    pid+=cartid
                                    cursor.execute ("Insert into payment values(?,?,?,?)",
                                                    (pid, list1[0][1], "Credited", list1[0][3]))
                                    conn.commit ()
                                    messagebox.showinfo ("Message", "Cancelled your order . Your amount will be credited in 3 to 4 days.")
                                else:
                                    # print(cursor.execute ("SELECT payid FROM payment where payid Like ?", (Username +'%'+list1[0][0],)).fetchall ())
                                    cursor.execute ("DELETE from payment where payid Like ?", (Username +'%'+list1[0][0],))
                                    conn.commit()

                            else:
                                messagebox.showerror ("Error", "Your order is already delivered")

                            Orders.destroy ()
                            displayCart ()

                            flag.set (0)

            Label (second_frame, text = 'My Orders', font = "Verdana 15 underline", fg = "SlateBlue1").grid (row = 0,
                                                                                                             column = 2)

            Label (second_frame, text = 'Enter Cart No:', font = ('arial', 10)).grid (row = 1, column = 0, pady = 5,
                                                                                      padx = 8)
            Entry (second_frame, textvariable = cartno, font = ('arial', 12), width = 12).grid (row = 1, column = 1,columnspan=1)
            Button (second_frame, text = "Show", command = displayProducts, font = ('arial', 8), fg = "snow",
                    bg = 'tomato', width = 8).grid (row = 1, column = 2,columnspan=1)

            def changeFlag():

                flag.set (1)
                try:
                    displayProducts ()
                except:
                    pass

            Button (second_frame, text = "Cancel Order", command = changeFlag, font = ('arial', 8), fg = "snow",
                    bg = 'tomato', width = 10).grid (row = 2, column = 0, columnspan=3,pady=5)

            Label (second_frame, text = 'Cart.No', font = ('arial', 11), fg = "RoyalBlue1").grid (row = 3, column = 0,
                                                                                                  pady = 5, padx = 8)
            Label (second_frame, text = 'Ordered Date', font = ('arial', 11), fg = "RoyalBlue1").grid (row = 3,
                                                                                                       column = 1,
                                                                                                       pady = 5,
                                                                                                       padx = 8)
            Label (second_frame, text = 'Delivery Date', font = ('arial', 11), fg = "RoyalBlue1").grid (row = 3,
                                                                                                        column = 2,
                                                                                                        pady = 5,
                                                                                                        padx = 8)
            Label (second_frame, text = 'Bill(in Rs)', font = ('arial', 11), fg = "RoyalBlue1").grid (row = 3,
                                                                                                      column = 3,
                                                                                                      pady = 5,
                                                                                                      padx = 8)
            Label (second_frame, text = 'Status', font = ('arial', 11), fg = "RoyalBlue1").grid (row = 3, column = 4,
                                                                                                 pady = 8)

            c = 4
            for x in list:

                Label (second_frame, text = x[0][len (Username):], font = ('arial', 12)).grid (row = c, column = 0,
                                                                                               pady = 5, padx = 8)
                Label (second_frame, text = x[2][:11], font = ('arial', 11)).grid (row = c, column = 1, pady = 5,
                                                                                   padx = 8)
                Label (second_frame, text = x[3], font = ('arial', 11)).grid (row = c, column = 2, pady = 5, padx = 8)
                Label (second_frame, text = x[1], font = ('arial', 11)).grid (row = c, column = 3, pady = 5, padx = 8)

                date1 = date.today ()
                date2 = pd.to_datetime (x[3], dayfirst = True)

                # print(date1,date2)

                if date1 < date2:
                    Label (second_frame, text = 'Pending', font = ('arial', 11), foreground = "red").grid (row = c,
                                                                                                           column = 4,
                                                                                                           pady = 5)
                else:
                    Label (second_frame, text = 'Delivered', font = ('arial', 11), foreground = "green").grid (row = c,
                                                                                                               column = 4,
                                                                                                               pady = 5)
                c += 1

            def Back():
                Orders.destroy ()
                shop.deiconify ()

            Button (second_frame, text = "Back", command = Back, font = ('arial', 11), width = 10, bg = "gray54",
                    fg = "snow").grid (row = 0, column = 4, pady = 5)

            Orders.mainloop ()

        Label (users, text = 'Hello,', font = ('arial', 13)).place (x = 30, y = 20)
        Label (users, text = Username, font = ('arial', 13), fg = "RoyalBlue1").place (x = 75, y = 20)
        Label (users, text = 'First Name', font = ('arial', 13)).place (x = 30, y = 60)
        Label (users, text = 'Last Name', font = ('arial', 13)).place (x = 30, y = 130)
        Label (users, text = 'Phone Number', font = ('arial', 13)).place (x = 30, y = 200)
        Label (users, text = 'Email', font = ('arial', 13)).place (x = 30, y = 270)
        Label (users, text = 'Address', font = ('arial', 13)).place (x = 30, y = 340)
        Button (users, text = 'Your Orders', font = ('arial', 12), command = displayCart, bg = "SlateBlue1",
                fg = "snow").place (x = 30, y = 410)
        c = 95
        for i in cursor.execute ("SELECT fname,lname,phoneno,email,address FROM users where username=?",
                                 [(Username)]).fetchone ():
            Label (users, text = i, font = ('arial', 12), fg = "RoyalBlue1").place (x = 30, y = c, bordermode = OUTSIDE)
            c += 70

        def back():
            users.destroy ()
            shop.destroy ()
            userScreen (Username)

        Button (users, text = 'Back', width = 35, font = ('arial', 10), command = back, bg = "gray54",
                fg = "snow").place (x = 250, y = 480, anchor = CENTER)

        def Back():
            shop.destroy ()
            users.destroy ()
            openScreen ()

        Button (users, text = 'Logout', command = Back, width = 35, font = ('arial', 10), bg = "tomato",
                fg = "snow").place (x = 250, y = 520, anchor = CENTER)
        users.mainloop ()

    shop = Tk ()
    shop.title ('Online Shopping Application')
    ws = shop.winfo_screenwidth ()
    hs = shop.winfo_screenheight ()
    x = (ws / 2) - (820 / 2)
    y = (hs / 2) - (660 / 2)
    shop.geometry ('%dx%d+%d+%d' % (820, 620, x, y))
    shop.resizable (0, 0)
    shop.config (bg = 'white')
    count = IntVar ()
    Amount = IntVar ()

    def add1():
        global c_apple
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 50)
        c_apple += 1

    def add2():
        global c_banana
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 30)
        c_banana += 1

    def add3():
        global c_orange
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 45)
        c_orange += 1

    def add4():
        global c_promogranate
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 90)
        c_promogranate += 1

    def add5():
        global c_tomato
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 40)
        c_tomato += 1

    def add6():
        global c_potato
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 53)
        c_potato += 1

    def add7():
        global c_onion
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 89)
        c_onion += 1

    def add8():
        global c_phone
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 32000)
        c_phone += 1

    def add9():
        global c_laptop
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 56000)
        c_laptop += 1

    def add10():
        global c_earphones
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 2499)
        c_earphones += 1

    def add11():
        global c_camera
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 29000)
        c_camera += 1

    def add12():
        global c_watch
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 2500)
        c_watch += 1

    def add13():
        global c_tv
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 70000)
        c_tv += 1

    def add14():
        global c_tablet
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 45000)
        c_tablet += 1

    def add15():
        global c_purifiers
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 9000)
        c_purifiers += 1

    def add16():
        global c_mixer
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 3500)
        c_mixer += 1

    def add17():
        global c_bottle
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 700)
        c_bottle += 1

    def add18():
        global c_bulb
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 600)
        c_bulb += 1

    def add19():
        global c_oven
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 8000)
        c_oven += 1

    def add20():
        global c_pans
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 3700)
        c_pans += 1

    def add21():
        global c_washingmachine
        count.set (count.get () + 1)
        Amount.set (Amount.get () + 42000)
        c_washingmachine += 1

    Label (shop, text = "Welcome to Click To Buy", bg = 'white', fg = '#875FFF',
           font = ('arial', 30, 'underline')).place (x = 400,
                                                     y = 25,
                                                     anchor = CENTER)

    photo = PhotoImage (file = r"Images\cart.png")
    photo1 = PhotoImage (file = r"Images\profile.png")
    photo2 = PhotoImage (file = r"Images\fuits.png")
    photo3 = PhotoImage (file = r"Images\apple.png")
    photo4 = PhotoImage (file = r"Images\banana.png")
    photo5 = PhotoImage (file = r"Images\orange.png")
    photo6 = PhotoImage (file = r"Images\promogranate.png")
    photo7 = PhotoImage (file = r"Images\tomato.png")
    photo8 = PhotoImage (file = r"Images\potato.png")
    photo9 = PhotoImage (file = r"Images\onion.png")
    photo10 = PhotoImage (file = r"Images\Laptop.png")
    photo11 = PhotoImage (file = r"Images\earphones.png")
    photo12 = PhotoImage (file = r"Images\camera.png")
    photo13 = PhotoImage (file = r"Images\Tv.png")
    photo14 = PhotoImage (file = r"Images\watch.png")
    photo15 = PhotoImage (file = r"Images\phone.png")
    photo16 = PhotoImage (file = r"Images\Tablet.png")
    photo17 = PhotoImage (file = r"Images\Logo1.png")
    photo18 = PhotoImage (file = r"Images\Water Purifiers.png")
    photo19 = PhotoImage (file = r"Images\mixer.png")
    photo20 = PhotoImage (file = r"Images\bottle.png")
    photo21 = PhotoImage (file = r"Images\Led bulbs.png")
    photo22 = PhotoImage (file = r"Images\owen.png")
    photo23 = PhotoImage (file = r"Images\Kitchen Set.png")
    photo24 = PhotoImage (file = r"Images\Washing Machine.png")
    photo25 = PhotoImage (file = r"Images\Logo.png")

    Button (shop, text = "USER", width = 45, image = photo1, bg = 'white', command = userDetails).place (x = 30, y = 10)
    Button (shop, text = "Cart", width = 45, image = photo, bg = 'white', command = Cart).place (x = 790, y = 10,
                                                                                                 anchor = NE)
    Label (shop, text = "Cart Items:", bg = 'white', font = ('arial', 15)).place (x = 740, y = 50, anchor = NE)
    Label (shop, textvariable = count, bg = 'white', font = ('arial', 15)).place (x = 790, y = 50, anchor = NE)

    Label (shop, text = "Products Available", font = ('arial', 15), bg = 'white').place (x = 10, y = 70)
    Label (shop, text = "Vegetables", font = ('arial', 10), image = photo2, bg = 'white').place (x = 10, y = 100)
    Label (shop, text = "Vegetables", font = ('arial', 12), bg = 'white').place (x = 10, y = 170)
    Label (shop, text = "and", font = ('arial', 12), bg = 'white').place (x = 10, y = 200)
    Label (shop, text = "Friuts", font = ('arial', 12), bg = 'white').place (x = 40, y = 200)

    Label (shop, text = "Apple", font = ('arial', 10), image = photo3, bg = 'white').place (x = 110, y = 100)
    Label (shop, text = "Apple", font = ('arial', 10), bg = 'white').place (x = 110, y = 170)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 110, y = 200)
    Label (shop, text = "Rs:50/Kg", font = ('arial', 10), bg = 'white').place (x = 140, y = 200)

    Label (shop, text = "Banana", font = ('arial', 10), image = photo4, bg = 'white').place (x = 210, y = 100)
    Label (shop, text = "Banana", font = ('arial', 10), bg = 'white').place (x = 210, y = 170)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 210, y = 200)
    Label (shop, text = "Rs:30/Kg", font = ('arial', 10), bg = 'white').place (x = 240, y = 200)

    Label (shop, text = "Orange", font = ('arial', 10), image = photo5, bg = 'white').place (x = 310, y = 100)
    Label (shop, text = "Orange", font = ('arial', 10), bg = 'white').place (x = 310, y = 170)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 310, y = 200)
    Label (shop, text = "Rs:45/Kg", font = ('arial', 10), bg = 'white').place (x = 340, y = 200)

    Label (shop, text = "Promagranate", font = ('arial', 10), image = photo6, bg = 'white').place (x = 410, y = 100)
    Label (shop, text = "Promagranate", font = ('arial', 10), bg = 'white').place (x = 410, y = 170)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 410, y = 200)
    Label (shop, text = "Rs:90/Kg", font = ('arial', 10), bg = 'white').place (x = 440, y = 200)

    Label (shop, text = "Tomato", font = ('arial', 10), image = photo7, bg = 'white').place (x = 510, y = 100)
    Label (shop, text = "Tomato", font = ('arial', 10), bg = 'white').place (x = 510, y = 170)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 510, y = 200)
    Label (shop, text = "Rs:40/Kg", font = ('arial', 10), bg = 'white').place (x = 540, y = 200)

    Label (shop, text = "Potato", font = ('arial', 10), image = photo8, bg = 'white').place (x = 610, y = 100)
    Label (shop, text = "Potato", font = ('arial', 10), bg = 'white').place (x = 610, y = 170)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 610, y = 200)
    Label (shop, text = "Rs:53/Kg", font = ('arial', 10), bg = 'white').place (x = 640, y = 200)

    Label (shop, text = "Onion", font = ('arial', 10), image = photo9, bg = 'white').place (x = 710, y = 100)
    Label (shop, text = "Onion", font = ('arial', 10), bg = 'white').place (x = 710, y = 170)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 710, y = 200)
    Label (shop, text = "Rs:89/Kg", font = ('arial', 10), bg = 'white').place (x = 740, y = 200)

    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add1).place (x = 125, y = 230)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add2).place (x = 225, y = 230)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add3).place (x = 325, y = 230)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add4).place (x = 425, y = 230)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add5).place (x = 525, y = 230)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add6).place (x = 625, y = 230)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add7).place (x = 725, y = 230)

    Label (shop, text = "Electronics", font = ('arial', 10), image = photo17, bg = 'white').place (x = 10, y = 260)
    Label (shop, text = "Electronics", font = ('arial', 12), bg = 'white').place (x = 10, y = 330)
    Label (shop, text = "and", font = ('arial', 12), bg = 'white').place (x = 10, y = 360)
    Label (shop, text = "Devices", font = ('arial', 12), bg = 'white').place (x = 40, y = 360)

    Label (shop, text = "Google Pixel 4a", font = ('arial', 10), image = photo15, bg = 'white').place (x = 110, y = 260)
    Label (shop, text = "Phone", font = ('arial', 10), bg = 'white').place (x = 110, y = 330)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 110, y = 360)
    Label (shop, text = "Rs:32,000/-", font = ('arial', 10), bg = 'white').place (x = 140, y = 360)

    Label (shop, text = "Laptop", font = ('arial', 10), image = photo10, bg = 'white').place (x = 210, y = 260)
    Label (shop, text = "Laptop", font = ('arial', 10), bg = 'white').place (x = 210, y = 330)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 210, y = 360)
    Label (shop, text = "Rs:56,000/-", font = ('arial', 10), bg = 'white').place (x = 240, y = 360)

    Label (shop, text = "Earphones", font = ('arial', 10), image = photo11, bg = 'white').place (x = 310, y = 260)
    Label (shop, text = "Earphones", font = ('arial', 10), bg = 'white').place (x = 310, y = 330)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 310, y = 360)
    Label (shop, text = "Rs:2,499/-", font = ('arial', 10), bg = 'white').place (x = 340, y = 360)

    Label (shop, text = "Camera", font = ('arial', 10), image = photo12, bg = 'white').place (x = 410, y = 260)
    Label (shop, text = "Camera", font = ('arial', 10), bg = 'white').place (x = 410, y = 330)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 410, y = 360)
    Label (shop, text = "Rs:29,000/-", font = ('arial', 10), bg = 'white').place (x = 440, y = 360)

    Label (shop, text = "Watch", font = ('arial', 10), image = photo14, bg = 'white').place (x = 510, y = 260)
    Label (shop, text = "Fitness Band", font = ('arial', 10), bg = 'white').place (x = 500, y = 330)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 510, y = 360)
    Label (shop, text = "Rs:2,500/-", font = ('arial', 10), bg = 'white').place (x = 540, y = 360)

    Label (shop, text = "TV", font = ('arial', 10), image = photo13, bg = 'white').place (x = 610, y = 260)
    Label (shop, text = "LED TV", font = ('arial', 10), bg = 'white').place (x = 610, y = 330)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 610, y = 360)
    Label (shop, text = "Rs:70,000/-", font = ('arial', 10), bg = 'white').place (x = 640, y = 360)

    Label (shop, text = "Tablet", font = ('arial', 10), image = photo16, bg = 'white').place (x = 710, y = 260)
    Label (shop, text = "Ipad", font = ('arial', 10), bg = 'white').place (x = 710, y = 330)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 710, y = 360)
    Label (shop, text = "Rs:45,000/-", font = ('arial', 10), bg = 'white').place (x = 740, y = 360)

    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add8).place (x = 125,
                                                                                                        y = 390)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add9).place (x = 225,
                                                                                                        y = 390)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add10).place (x = 325,
                                                                                                        y = 390)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add11).place (x = 425,
                                                                                                        y = 390)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add12).place (x = 525,
                                                                                                        y = 390)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add13).place (x = 625,
                                                                                                        y = 390)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add14).place (x = 725,
                                                                                                        y = 390)

    Label (shop, text = "Home and Kitchen", font = ('arial', 10), image = photo25, bg = 'white').place (x = 10, y = 420)
    Label (shop, text = "House", font = ('arial', 12), bg = 'white').place (x = 10, y = 490)
    Label (shop, text = "and", font = ('arial', 12), bg = 'white').place (x = 10, y = 520)
    Label (shop, text = "Kitchen", font = ('arial', 12), bg = 'white').place (x = 40, y = 520)

    Label (shop, text = "Water Purifier", font = ('arial', 10), image = photo18, bg = 'white').place (x = 110, y = 420)
    Label (shop, text = "Water Purifier", font = ('arial', 10), bg = 'white').place (x = 110, y = 490)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 110, y = 520)
    Label (shop, text = "Rs:9000/-", font = ('arial', 10), bg = 'white').place (x = 140, y = 520)

    Label (shop, text = "Mixer", font = ('arial', 10), image = photo19, bg = 'white').place (x = 210, y = 420)
    Label (shop, text = "Mixer", font = ('arial', 10), bg = 'white').place (x = 210, y = 490)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 210, y = 520)
    Label (shop, text = "Rs:3500/-", font = ('arial', 10), bg = 'white').place (x = 240, y = 520)

    Label (shop, text = "Bottle", font = ('arial', 10), image = photo20, bg = 'white').place (x = 310, y = 420)
    Label (shop, text = "Copper Bottle", font = ('arial', 10), bg = 'white').place (x = 310, y = 490)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 310, y = 520)
    Label (shop, text = "Rs:700/-", font = ('arial', 10), bg = 'white').place (x = 340, y = 520)

    Label (shop, text = "Smart Led Bulbs", font = ('arial', 10), image = photo21, bg = 'white').place (x = 410, y = 420)
    Label (shop, text = "Led Bulbs", font = ('arial', 10), bg = 'white').place (x = 410, y = 490)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 410, y = 520)
    Label (shop, text = "Rs:600/-", font = ('arial', 10), bg = 'white').place (x = 440, y = 520)

    Label (shop, text = "Microwave Oven", font = ('arial', 10), image = photo22, bg = 'white').place (x = 510, y = 420)
    Label (shop, text = "Microwave Oven", font = ('arial', 10), bg = 'white').place (x = 510, y = 490)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 510, y = 520)
    Label (shop, text = "Rs:8,000/-", font = ('arial', 10), bg = 'white').place (x = 540, y = 520)

    Label (shop, text = "Kitchen Sets", font = ('arial', 10), image = photo23, bg = 'white').place (x = 610, y = 420)
    Label (shop, text = "Kitchen Sets", font = ('arial', 10), bg = 'white').place (x = 610, y = 490)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 610, y = 520)
    Label (shop, text = "Rs:3,700/-", font = ('arial', 10), bg = 'white').place (x = 630, y = 520)

    Label (shop, text = "Washing Machine", font = ('arial', 10), image = photo24, bg = 'white').place (x = 700, y = 420)
    Label (shop, text = "Washing Machine", font = ('arial', 10), bg = 'white').place (x = 710, y = 490)
    Label (shop, text = "Cost", font = ('arial', 10), bg = 'white').place (x = 710, y = 520)
    Label (shop, text = "Rs:42,000/-", font = ('arial', 10), bg = 'white').place (x = 740, y = 520)

    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add15).place (x = 125,
                                                                                                        y = 550)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add16).place (x = 225,
                                                                                                        y = 550)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add17).place (x = 325,
                                                                                                        y = 550)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add18).place (x = 425,
                                                                                                        y = 550)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add19).place (x = 525,
                                                                                                        y = 550)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add20).place (x = 625,
                                                                                                        y = 550)
    Button (shop, text = "ADD", font = ('arial', 9), bg = 'blue', fg = 'white', command = add21).place (x = 725,
                                                                                                        y = 550)

    Label (shop, text = "Total Amount", bg = 'white', font = ('arial', 13)).place (x = 700, y = 590, anchor = NE)
    Label (shop, textvariable = Amount, bg = 'white', font = ('arial', 13)).place (x = 780, y = 590, anchor = NE)

    shop.mainloop ()


# =======================================LOGIN=======================================

def Login():
    main = Tk ()
    main.title ("Online Shopping Application")
    width = 500
    height = 300
    screen_width = main.winfo_screenwidth ()
    screen_height = main.winfo_screenheight ()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    main.geometry ("%dx%d+%d+%d" % (width, height, x, y))
    main.resizable (0, 0)

    # ==============================VARIABLES======================================

    USERNAME = StringVar ()
    PASSWORD = StringVar ()

    def checkLogin():

        Database ()

        if USERNAME.get () == "" or PASSWORD.get () == "":
            lbl_text.config (text = "Please complete the required field!", fg = "red")
        else:
            cursor.execute ("SELECT * FROM users WHERE username = ? AND password = ?",
                            (USERNAME.get (), PASSWORD.get ()))
            if cursor.fetchone () is not None:
                lbl_text.config (text = "")
                main.destroy ()
                userScreen (USERNAME.get ())
                USERNAME.set ("")
                PASSWORD.set ("")

            else:
                lbl_text.config (text = "Invalid username or password", fg = "red")
                USERNAME.set ("")
                PASSWORD.set ("")

    def registration1():
        main.destroy ()
        registration ()

    if __name__ == '__main__':
        # ==============================FRAMES=========================================

        Top = Frame (main, bd = 2, relief = RIDGE)
        Top.pack (side = TOP, fill = X)
        Form = Frame (main, height = 200)
        Form.pack (side = TOP, pady = 20)

        # ==============================LABELS=========================================

        lbl_title = Label (Top, text = "Online Shopping Application", fg = "#875FFF", font = ('arial', 15))
        lbl_title.pack (fill = X)
        lbl_username = Label (Form, text = "Username:", font = "Verdana 15", bd = 15)
        lbl_username.grid (row = 0, sticky = "e")
        lbl_password = Label (Form, text = "Password:", font = "Verdana 15", bd = 15)
        lbl_password.grid (row = 1, sticky = "e")
        lbl_text = Label (Form)
        lbl_text.grid (row = 2, columnspan = 2)

        # ==============================ENTRY WIDGETS==================================

        username = Entry (Form, textvariable = USERNAME, font = "Verdana 15")
        username.grid (row = 0, column = 1)
        password = Entry (Form, textvariable = PASSWORD, show = "*", font = "Verdana 15")
        password.grid (row = 1, column = 1)

        # ==============================BUTTON WIDGETS=================================

        btn_login = Button (Form, text = "Login", width = 45, command = checkLogin, activebackground = "spring green")
        btn_login.grid (pady = 15, row = 3, columnspan = 2)

        btn_login = Button (Form, text = "Register", width = 45, command = registration1, activebackground = "tomato",
                            activeforeground = "snow")
        btn_login.grid (pady = 10, row = 4, columnspan = 2)

        main.mainloop ()


def adminPage():

    Database ()

    users = Tk ()
    users.title ("Online Shopping Application")
    width = 700
    height = 500
    screen_width = users.winfo_screenwidth ()
    screen_height = users.winfo_screenheight ()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    users.geometry ("%dx%d+%d+%d" % (width, height, x, y))
    users.resizable (0, 0)

    # Create a main frame
    main_frame = Frame (users)
    main_frame.pack (fill = BOTH, expand = 1)

    # Create a Canvas
    my_Canvas = Canvas (main_frame)
    my_Canvas.pack (side = LEFT, fill = BOTH, expand = 1)

    # Add a scrollbar to Canvas
    my_scrollbar = ttk.Scrollbar (main_frame, orient = VERTICAL, command = my_Canvas.yview)
    my_scrollbar.pack (side = RIGHT, fill = Y)

    # Configure the canvas
    my_Canvas.configure (yscrollcommand = my_scrollbar.set)
    my_Canvas.bind ('<Configure>', lambda e:my_Canvas.configure (scrollregion = my_Canvas.bbox ("all")))

    # Create another frame inside the Canvas
    second_frame = Frame (my_Canvas)

    # Add new frame to a window
    my_Canvas.create_window ((0, 0), window = second_frame, anchor = "nw")
    second_frame.config (bg = 'white')

    Label (second_frame, text = "User Details",font = "Verdana 15 bold underline", fg = 'slateblue1',
           bg = 'white').grid (row = 0, column = 2, pady = 5,columnspan=1)
    Label (second_frame, text = "Username", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 2, column = 0, padx = 15, pady = 5)
    Label (second_frame, text = "First Name", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 2, column = 1, padx = 15, pady = 5)
    Label (second_frame, text = "Phone Number", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 2, column = 2, padx = 15, pady = 5)
    Label (second_frame, text = "Email Address", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 2, column = 3, padx = 15, pady = 5)

    c = 3
    l = cursor.execute ('Select * from users').fetchall ()
    # print(l)
    for i in l:
        Label (second_frame, text = i[0], font = ('arial', 12), bg = 'white').grid (row = c, column = 0, padx = 15,
                                                                                    pady = 5)
        Label (second_frame, text = i[1], font = ('arial', 12), bg = 'white').grid (row = c, column = 1, padx = 15,
                                                                                    pady = 5)
        Label (second_frame, text = i[3], font = ('arial', 12), bg = 'white').grid (row = c, column = 2, padx = 15,
                                                                                    pady = 5)

        Label (second_frame, text = i[4], font = ('arial', 12), bg = 'white').grid (row = c, column = 3, padx = 15,
                                                                                    pady = 5)
        c += 1

    def back():
        users.destroy ()
        openScreen ()

    Button (second_frame, text = 'Logout', width = 15, command = back, bg = "tomato", fg = "snow").grid (row = c,
                                                                                                         column = 2,
                                                                                                         padx = 15,
                                                                                                         pady = 5,columnspan=1)
    users.mainloop ()


def openScreen():

    open = Tk ()
    open.title ("Online Shopping Application")
    width = 500
    height = 300
    screen_width = open.winfo_screenwidth ()
    screen_height = open.winfo_screenheight ()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    open.geometry ("%dx%d+%d+%d" % (width, height, x, y))
    open.resizable (0, 0)
    open.config (bg = 'Ivory1')

    def openLogin():
        open.destroy ()
        Login ()

    def openAdmin():
        open.destroy ()
        adminPage ()

    def onLeave(event):
        user_btn.config (bg = 'Lightblue1', fg = 'black')

    def onEnter(event):
        user_btn.config (bg = 'slateblue1', fg = 'white')

    def onLeave1(event):
        admin_btn.config (bg = 'Lightblue1', fg = 'black')

    def onEnter1(event):
        admin_btn.config (bg = 'slateblue1', fg = 'white')

    def logout():
        open.destroy()
        print("Thanks for using Click to Buy!!!")
        return

    photo = PhotoImage (file = r"Images\exit.PNG")

    Button(open,text="back", font = 'Verdana 8 ', image=photo,fg = 'black', command=logout).pack(side=TOP, anchor=NW)

    Label (open, text = "DBMS Project", font = 'Verdana 15 bold underline', fg = 'black').pack ()
    Label (open, text = "Online Shopping Application", font = 'Verdana 15 bold underline',
           fg = 'black').pack ()

    user_btn = Button (open, text = 'USER', command = openLogin, font = "Verdana 15 underline", bg = 'Lightblue1')
    user_btn.pack (side = LEFT, expand = True, fill = BOTH, pady = 60, padx = 30)
    user_btn.bind ('<Enter>', onEnter)
    user_btn.bind ('<Leave>', onLeave)

    admin_btn = Button (open, text = 'ADMIN', command = openAdmin, font = "Verdana 15 underline", bg = 'Lightblue1')
    admin_btn.pack (side = LEFT, expand = True, fill = BOTH, pady = 60, padx = 30)
    admin_btn.bind ('<Enter>', onEnter1)
    admin_btn.bind ('<Leave>', onLeave1)

    open.mainloop ()


def userScreen(username):

    user = Tk ()
    user.title ("Online Shopping Application")
    width = 600
    height = 400
    screen_width = user.winfo_screenwidth ()
    screen_height = user.winfo_screenheight ()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    user.geometry ("%dx%d+%d+%d" % (width, height, x, y))
    user.resizable (0, 0)

    def gotoHome():
        user.destroy ()
        HomeWindow (username)

    def editdetails():
        user.destroy ()
        editDetails (username)

    def paymentdetails():
        user.destroy ()
        paymentDetails (username)

    def onLeave(event):
        user_btn.config (bg = 'Lightblue1', fg = 'black')

    def onEnter(event):
        user_btn.config (bg = 'slateblue1', fg = 'white')

    def onLeave1(event):
        user1_btn.config (bg = 'Lightblue1', fg = 'black')

    def onEnter1(event):
        user1_btn.config (bg = 'slateblue1', fg = 'white')

    def onLeave2(event):
        user2_btn.config (bg = 'Lightblue1', fg = 'black')

    def onEnter2(event):
        user2_btn.config (bg = 'slateblue1', fg = 'white')

    Label (user, text = "Dashboard", font = 'Verdana 25 bold underline').pack ()

    user_btn = Button (user, text = 'Shopping Page', command = gotoHome, font = "Verdana 15 ", bg = 'Lightblue1')
    user_btn.pack (fill = X, pady = 20, padx = 50, ipady = 10)
    user_btn.bind ('<Enter>', onEnter)
    user_btn.bind ('<Leave>', onLeave)

    user1_btn = Button (user, text = 'Edit Details', command = editdetails, font = "Verdana 15 ", bg = 'Lightblue1')
    user1_btn.pack (fill = X, pady = 20, padx = 50, ipady = 10)
    user1_btn.bind ('<Enter>', onEnter1)
    user1_btn.bind ('<Leave>', onLeave1)

    user2_btn = Button (user, text = 'User Payment History', command = paymentdetails, font = "Verdana 15 ",
                        bg = 'Lightblue1')
    user2_btn.pack (fill = X, pady = 20, padx = 50, ipady = 10)
    user2_btn.bind ('<Enter>', onEnter2)
    user2_btn.bind ('<Leave>', onLeave2)

    user.mainloop ()


def editDetails(username):

    Database ()
    edit = Tk ()
    edit.title ("Online Sh0pping Application")
    width = 600
    height = 400
    screen_width = edit.winfo_screenwidth ()
    screen_height = edit.winfo_screenheight ()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    edit.geometry ("%dx%d+%d+%d" % (width, height, x, y))
    edit.resizable (0, 0)
    Label (edit, text = '', font = "Verdana 15 bold underline").grid (row = 0, column = 0, ipadx = 50)
    Label (edit, text = 'Edit Account', font = "Verdana 15 bold underline").grid (row = 0, column = 1, pady = 20,
                                                                                  columnspan = 2)

    USERNAME = StringVar (edit)
    PASSWORD = StringVar (edit)
    FNAME = StringVar (edit)
    LNAME = StringVar (edit)
    PHONE = StringVar (edit)
    EMAIL = StringVar (edit)
    ADDRESS = StringVar (edit)

    list1 = cursor.execute ("SELECT * FROM users where username=?", [(username)]).fetchone ()
    USERNAME.set (list1[0])
    FNAME.set (list1[1])
    LNAME.set (list1[2])
    PHONE.set (list1[3])
    EMAIL.set (list1[4])
    PASSWORD.set (list1[5])
    ADDRESS.set (list1[6])

    Label (edit, text = "First Name", font = "Verdana 13 ").grid (row = 3, column = 1, pady = 9)
    Label (edit, text = "Last Name", font = "Verdana 13 ").grid (row = 4, column = 1, pady = 9)
    Label (edit, text = "Phone Number", font = "Verdana 13 ").grid (row = 5, column = 1, pady = 9, padx = 5)
    Label (edit, text = "Password", font = "Verdana 13 ").grid (row = 6, column = 1, pady = 9)
    Label (edit, text = "Address", font = "Verdana 13 ").grid (row = 7, column = 1, pady = 9)

    Entry (edit, textvariable = FNAME, font = "Verdana 13").grid (row = 3, column = 2)
    Entry (edit, textvariable = LNAME, font = "Verdana 13").grid (row = 4, column = 2)
    Entry (edit, textvariable = PHONE, font = "Verdana 13").grid (row = 5, column = 2)
    Entry (edit, textvariable = PASSWORD, font = "Verdana 13").grid (row = 6, column = 2)
    Entry (edit, textvariable = ADDRESS, font = "Verdana 13").grid (row = 7, column = 2)

    def save():

        # print(USERNAME.get(),FNAME.get(),LNAME.get(),PHONE.get(),PASSWORD.get(),ADDRESS.get(),EMAIL.get())

        try:
             x = int (PHONE.get ())
        except:
            messagebox.showerror (title = 'ERROR', message = "Enter valid phone number")
            PHONE.set("")

        if USERNAME.get () == "" or FNAME.get () == "" or LNAME.get () == "" or PHONE.get () == "" or PASSWORD.get () == "" or ADDRESS.get () == "" or EMAIL.get () == "":
            Label (edit, text = "Fill the required deitlds", fg = "red").grid (row = 9, column = 1, columnspan = 2)

        else:
            cursor.execute ('''UPDATE users set
                username=?,fname=?,lname=?,phoneno=?,password=?,address=?
                where email=?;
            ''', [USERNAME.get (), FNAME.get (), LNAME.get (), PHONE.get (), PASSWORD.get (), ADDRESS.get (),
                  EMAIL.get ()])
            conn.commit ()
            messagebox.showinfo("message","Your details have been updated")
            edit.destroy ()
            userScreen (username)

    Button (edit, text = 'Save', command = save, width = 15, font = "Verdana 13").grid (row = 10, column = 1, pady = 10,
                                                                                        columnspan = 2)
    edit.mainloop ()


def paymentDetails(username):

    Database ()
    transactions = Tk ()
    transactions.title ("Online Shopping Application")
    width = 560
    height = 400
    screen_width = transactions.winfo_screenwidth ()
    screen_height = transactions.winfo_screenheight ()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    transactions.geometry ("%dx%d+%d+%d" % (width, height, x, y))
    transactions.resizable (0, 0)

    # Create a main frame
    main_frame = Frame (transactions)
    main_frame.pack (fill = BOTH, expand = 1)

    # Create a Canvas
    my_Canvas = Canvas (main_frame)
    my_Canvas.pack (side = LEFT, fill = BOTH, expand = 1)

    # Add a scrollbar to Canvas
    my_scrollbar = ttk.Scrollbar (main_frame, orient = VERTICAL, command = my_Canvas.yview)
    my_scrollbar.pack (side = RIGHT, fill = Y)

    # Configure the canvas
    my_Canvas.configure (yscrollcommand = my_scrollbar.set)
    my_Canvas.bind ('<Configure>', lambda e:my_Canvas.configure (scrollregion = my_Canvas.bbox ("all")))

    # Create another frame inside the Canvas
    second_frame = Frame (my_Canvas)

    # Add new frame to a window
    my_Canvas.create_window ((0, 0), window = second_frame, anchor = "nw")
    second_frame.config (bg = 'white')
    second_frame.config (bg = 'white')

    Label (second_frame, text = "Payment History", font = "Verdana 15 bold underline", fg = 'slateblue1',
           bg = 'white').grid (row = 0, column = 1, pady = 5, columnspan = 4)
    Label (second_frame, text = "S.no", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 1, column = 0, padx = 12, pady = 5)
    Label (second_frame, text = "Payment id", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 1, column = 1, padx = 15, pady = 5)
    Label (second_frame, text = "Amount", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 1, column = 2, padx = 15, pady = 5)
    Label (second_frame, text = "Date", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 1, column = 3, padx = 15, pady = 5)
    Label (second_frame, text = "Method", font = ('arial', 12, 'bold', 'underline'), fg = 'VioletRed1',
           bg = 'white').grid (row = 1, column = 4, padx = 15, pady = 5)

    l = cursor.execute ('Select * from payment where payid Like ?',(username + '%',)).fetchall ()

    # print(l)

    def createpid():

        x = '100'
        for i in random.randint (100, size = (8)):
            x += str (i)
            x += str (random.randint (10))
            if len (x) >= 12:
                return x

    c = 2
    for i in range (len (l)):
        c += 1
        Label (second_frame, text = str (i + 1), font = ('arial', 12),
               bg = 'white').grid (row = c, column = 0, padx = 12, pady = 5)
        x = createpid ()
        Label (second_frame, text = x, font = ('arial', 12),
               bg = 'white').grid (row = c, column = 1, padx = 18, pady = 5)
        Label (second_frame, text = l[i][1], font = ('arial', 12),
               bg = 'white').grid (row = c, column = 2, padx = 15, pady = 5)
        Label (second_frame, text = l[i][3], font = ('arial', 12),
               bg = 'white').grid (row = c, column = 3, padx = 15, pady = 5)
        Label (second_frame, text = l[i][2], font = ('arial', 12),
               bg = 'white').grid (row = c, column = 4, padx = 15, pady = 5)
    c += 1

    def back():
        transactions.destroy ()
        userScreen (username)

    Button (second_frame, text = 'Back', font = ('arial', 12), command = back, width = 15).grid (row = c, column = 1,
                                                                                                 columnspan = 3)

    transactions.mainloop ()

openScreen ()

# HomeWindow("2711bharath")