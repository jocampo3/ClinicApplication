import mysql.connector
from mysql.connector import errorcode
import tkinter as tk
from tkinter import font, ttk, messagebox
from tkinter import *

class PatientApp:
    def __init__(self, root):
        self.root = root
        self.create_gui_layout()

        self.connect_to_database()

        self.populate_gui_grid()

    def connect_to_database(self):
        try:
            self.connect = mysql.connector.connect(
                user='root',
                password='Samford99',
                host='localhost',
                database='clinic',
                port='3306'
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Invalid credentials')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database not found')
            else:
                print('Cannot connect to database:', err)

    def create_gui_layout(self):
        self.tree = ttk.Treeview(self.root)
        self.tree['show'] = 'headings'

        self.tree['columns'] = ('PatientID', 'PatientName', 'BirthDate')

        # Create: Columns
        self.tree.column('PatientID', width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column('PatientName', width=100, minwidth=100, anchor=tk.W)
        self.tree.column('BirthDate', width=100, minwidth=100, anchor=tk.W)

        # Create: Headings
        self.tree.heading('PatientID', text='PatientID', anchor=tk.CENTER)
        self.tree.heading('PatientName', text='PatientName', anchor=tk.CENTER)
        self.tree.heading('BirthDate', text='BirthDate', anchor=tk.CENTER)

        self.hsb = ttk.Scrollbar(self.root, orient='horizontal')
        self.hsb.configure(command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.hsb.set)
        self.hsb.pack(fill=tk.X, side=tk.BOTTOM)

        self.vsb = ttk.Scrollbar(self.root, orient='vertical')
        self.vsb.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)

        self.tree.pack()

        # Create and pack the buttons inside the frame
        self.insert_button = tk.Button(self.root, text='Insert', command=self.add_data)
        self.insert_button.configure(font=('calibri', 14, 'bold'), bg='green', fg='white')
        self.insert_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.root, text='Delete', command=self.delete_data)
        self.delete_button.configure(font=('calibri', 14, 'bold'), bg='red', fg='white')
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(self.root, text='Update', command=self.select_data)
        self.update_button.configure(font=('calibri', 14, 'bold'), bg='blue', fg='white')
        self.update_button.pack(side=tk.LEFT, padx=5)

        # Pack the frame at the bottom of the window
        self.root.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def populate_gui_grid(self):
        conn = self.connect.cursor()
        conn.execute("select * from Patient")

        for i, Row in enumerate(conn):
            self.tree.insert('', i, text="", values=(Row[0], Row[1], Row[2]))

    def add_data(self):
        f = Frame(self.root, width=400, height=400, background='grey')
        f.place(x=100, y=250)

        PatientID = StringVar()
        PatientName = StringVar()
        BirthDate = StringVar()

        l1 = Label(f, text='PatientID', width=8, font=('Times', 11, 'bold'))
        e1 = Entry(f, textvariable=PatientID, width=25)
        l1.place(x=50, y=30)
        e1.place(x=170, y=30)

        l2 = Label(f, text='PatientName', width=8, font=('Times', 11, 'bold'))
        e2 = Entry(f, textvariable=PatientName, width=25)
        l2.place(x=50, y=70)
        e2.place(x=170, y=70)

        l3 = Label(f, text='BirthDate', width=8, font=('Times', 11, 'bold'))
        e3 = Entry(f, textvariable=BirthDate, width=25)
        l3.place(x=50, y=110)
        e3.place(x=170, y=110)

        def insert_data():
            a_PatientID = PatientID.get()
            a_patientName = PatientName.get()
            a_BirthDate = BirthDate.get()

            conn = self.connect.cursor()
            conn.execute('INSERT INTO Patient(PatientID, PatientName, BirthDate) VALUES(%s,%s,%s)',
                         (a_PatientID, a_patientName, a_BirthDate))
            self.connect.commit()
            self.tree.insert('', 'end', text="", values=(a_PatientID, a_patientName, a_BirthDate))
            messagebox.showinfo("Success", "Patient Created")
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)

            f.destroy()

        submitbutton = tk.Button(f, text="submit", command=insert_data)
        submitbutton.configure(font=('Times', 11, 'bold'), bg='green', fg='white')
        submitbutton.place(x=100, y=360)
        cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
        cancelbutton.configure(font=('Times', 11, 'bold'), bg='red', fg='white')
        cancelbutton.place(x=240, y=360)

    def delete_data(self):
        selected_item = self.tree.selection()[0]
        uid = self.tree.item(selected_item)['values'][0]
        del_query = 'DELETE from Patient where PatientID = %s'
        sel_data = (uid,)
        conn = self.connect.cursor()
        conn.execute(del_query, sel_data)
        self.connect.commit()
        self.tree.delete(selected_item)
        messagebox.showinfo("SUCCESS", 'Patient data deleted')

    def select_data(self):
        curItem = self.tree.focus()
        values = self.tree.item(curItem, 'values')

        f = Frame(self.root, width=400, height=400, background='grey')
        f.place(x=100, y=250)

        patientID = StringVar()
        PatientName = StringVar()
        BirthDate = StringVar()

        l1 = Label(f, text='PatientID', width=8, font=('Times', 11, 'bold'))
        e1 = Entry(f, textvariable=patientID, width=25)
        l1.place(x=50, y=30)
        e1.place(x=170, y=30)

        l2 = Label(f, text='PatientName', width=8, font=('Times', 11, 'bold'))
        e2 = Entry(f, textvariable=PatientName, width=25)
        l2.place(x=50, y=70)
        e2.place(x=170, y=70)

        l3 = Label(f, text='BirthDate', width=8, font=('Times', 11, 'bold'))
        e3 = Entry(f, textvariable=BirthDate, width=25)
        l3.place(x=50, y=110)
        e3.place(x=170, y=110)

        e1.insert(0, values[0])
        e2.insert(0, values[1])
        e3.insert(0, values[2])

        def update_data():
            a_PatientID = patientID.get()
            a_patientName = PatientName.get()
            a_Birthdate = BirthDate.get()

            self.tree.item(curItem, values=(values[0], a_PatientID, a_patientName, a_Birthdate))

            conn = self.connect.cursor()
            conn.execute(
                'UPDATE Patient SET PatientID=%s, PatientName=%s, BirthDate=%s WHERE PatientID=%s',
                (a_PatientID, a_patientName, a_Birthdate, values[0]))

            self.connect.commit()
            messagebox.showinfo('SUCCESS', 'Patient data updated')
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)

            f.destroy()

        savebutton = tk.Button(f, text="submit", command=update_data)
        savebutton.configure(font=('Times', 11, 'bold'), bg='green', fg='white')
        savebutton.place(x=100, y=360)
        cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
        cancelbutton.configure(font=('Times', 11, 'bold'), bg='red', fg='white')
        cancelbutton.place(x=200, y=360)