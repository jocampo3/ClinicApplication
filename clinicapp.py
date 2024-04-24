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

class PatientContactApp:
    def __init__(self, root):
        self.root = root
        
        self.connect_to_database()
        
        self.create_gui_layout()

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

        self.tree['columns'] = ('PatientID', 'PhoneNumber', 'Email')

        # Create: Columns
        self.tree.column('PatientID', width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column('PhoneNumber', width=100, minwidth=100, anchor=tk.W)
        self.tree.column('Email', width=100, minwidth=100, anchor=tk.W)

        # Create: Headings
        self.tree.heading('PatientID', text='PatientID', anchor=tk.CENTER)
        self.tree.heading('PhoneNumber', text='PhoneNumber', anchor=tk.CENTER)
        self.tree.heading('Email', text='Email', anchor=tk.CENTER)

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
        conn.execute("select * from Patient_Contact")

        for i, Row in enumerate(conn):
            self.tree.insert('', i, text="", values=(Row[0], Row[1], Row[2]))

    def add_data(self):
        f = Frame(self.root, width=400, height=400, background='grey')
        f.place(x=100, y=250)

        PatientID = StringVar()
        PhoneNumber = StringVar()
        Email = StringVar()

        l1 = Label(f, text='PatientID', width=8, font=('Times', 11, 'bold'))
        e1 = Entry(f, textvariable=PatientID, width=25)
        l1.place(x=50, y=30)
        e1.place(x=170, y=30)

        l2 = Label(f, text='PhoneNumber', width=8, font=('Times', 11, 'bold'))
        e2 = Entry(f, textvariable=PhoneNumber, width=25)
        l2.place(x=50, y=70)
        e2.place(x=170, y=70)

        l3 = Label(f, text='Email', width=8, font=('Times', 11, 'bold'))
        e3 = Entry(f, textvariable=Email, width=25)
        l3.place(x=50, y=110)
        e3.place(x=170, y=110)

        def insert_data():
            a_PatientID = PatientID.get()
            a_PhoneNumber = PhoneNumber.get()
            a_Email = Email.get()

            conn = self.connect.cursor()
            conn.execute('INSERT INTO Patient_Contact(PatientID, PhoneNumber, Email) VALUES(%s,%s,%s)',
                         (a_PatientID, a_PhoneNumber, a_Email))
            self.connect.commit()
            self.tree.insert('', 'end', text="", values=(a_PatientID, a_PhoneNumber, a_Email))
            messagebox.showinfo("Success", "Patient Contact Created")
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
        del_query = 'DELETE from patient_contact where PatientID = %s'
        sel_data = (uid,)
        conn = self.connect.cursor()
        conn.execute(del_query, sel_data)
        self.connect.commit()
        self.tree.delete(selected_item)
        messagebox.showinfo("SUCCESS", 'Patient Contact data deleted')

    def select_data(self):
        curItem = self.tree.focus()
        values = self.tree.item(curItem, 'values')

        f = Frame(self.root, width=400, height=400, background='grey')
        f.place(x=100, y=250)

        patientID = StringVar()
        PhoneNumber = StringVar()
        Email = StringVar()

        l1 = Label(f, text='PatientID', width=8, font=('Times', 11, 'bold'))
        e1 = Entry(f, textvariable=patientID, width=25)
        l1.place(x=50, y=30)
        e1.place(x=170, y=30)

        l2 = Label(f, text='PhoneNumber', width=8, font=('Times', 11, 'bold'))
        e2 = Entry(f, textvariable=PhoneNumber, width=25)
        l2.place(x=50, y=70)
        e2.place(x=170, y=70)

        l3 = Label(f, text='Email', width=8, font=('Times', 11, 'bold'))
        e3 = Entry(f, textvariable=Email, width=25)
        l3.place(x=50, y=110)
        e3.place(x=170, y=110)

        e1.insert(0, values[0])
        e2.insert(0, values[1])
        e3.insert(0, values[2])

        def update_data():
            a_PatientID = patientID.get()
            a_PhoneNumber = PhoneNumber.get()
            a_Email = Email.get()

            self.tree.item(curItem, values=(values[0], a_PatientID, a_PhoneNumber, a_Email))

            conn = self.connect.cursor()
            conn.execute(
                'UPDATE patient_contact SET PatientID=%s, PhoneNumber=%s, Email=%s WHERE PatientID=%s',
                (a_PatientID, a_PhoneNumber, a_Email, values[0]))

            self.connect.commit()
            messagebox.showinfo('SUCCESS', 'Patient Contact data updated')
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


#create class appointment

class Appointment():
    def __init__(self, root):
        self.root = root
        
        self.connect_to_database()
        
        self.create_gui_layout()

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

        self.tree['columns'] = ('PatientID', 'AppointmentID', 'AppointmentDate', 'AppointmentTypeID')

        # Create: Columns
        self.tree.column('PatientID', width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column('AppointmentID', width=100, minwidth=100, anchor=tk.W)
        self.tree.column('AppointmentDate', width=100, minwidth=100, anchor=tk.W)
        self.tree.column('AppointmentTypeID', width=100, minwidth=100, anchor=tk.W)

        # Create: Headings
        self.tree.heading('PatientID', text='PatientID', anchor=tk.CENTER)
        self.tree.heading('AppointmentID', text='AppointmentID', anchor=tk.CENTER)
        self.tree.heading('AppointmentDate', text='AppointmentDate', anchor=tk.CENTER)
        self.tree.heading('AppointmentTypeID', text='AppointmentTypeID', anchor=tk.CENTER)

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
        conn.execute("select * from appointment")

        for i, Row in enumerate(conn):
            self.tree.insert('', i, text="", values=(Row[0], Row[1], Row[2], Row[3]))

    def add_data(self):
        f = Frame(self.root, width=400, height=400, background='black')
        f.place(x=100, y=250)

        PatientID = StringVar()
        AppointmentID = StringVar()
        AppointmentDate = StringVar()
        AppointmentTypeID = StringVar()

        l1 = Label(f, text='PatientID', width=8, font=('Times', 11, 'bold'))
        e1 = Entry(f, textvariable=PatientID, width=25)
        l1.place(x=50, y=30)
        e1.place(x=170, y=30)

        l2 = Label(f, text='AppointmentID', width=8, font=('Times', 11, 'bold'))
        e2 = Entry(f, textvariable=AppointmentID, width=25)
        l2.place(x=50, y=70)
        e2.place(x=170, y=70)

        l3 = Label(f, text='AppointmentDate', width=8, font=('Times', 11, 'bold'))
        e3 = Entry(f, textvariable=AppointmentDate, width=25)
        l3.place(x=50, y=110)
        e3.place(x=170, y=110)

        l4 = Label(f, text='AppointmentTypeID', width=8, font=('Times', 11, 'bold'))
        e4 = Entry(f, textvariable=AppointmentTypeID, width=25)
        l4.place(x = 50, y = 70)
        e4.place(x = 170, y= 110)

        def insert_data():
            a_PatientID = PatientID.get()
            a_appointmentID = AppointmentID.get()
            a_AppointmentDate = AppointmentDate.get()
            a_appointmentTypeID = AppointmentTypeID.get()

            conn = self.connect.cursor()
            conn.execute('INSERT INTO Appointment(PatientID, AppointmentID, AppointmentDate, AppointmentTypeID) VALUES(%s,%s,%s,%s)',
                         (a_PatientID, a_appointmentID, a_AppointmentDate, a_appointmentTypeID))
            self.connect.commit()
            self.tree.insert('', 'end', text="", values=(a_PatientID, a_appointmentID, a_AppointmentDate, a_appointmentTypeID))
            messagebox.showinfo("Success", "Appointment Created")
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)

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
        del_query = 'DELETE from appointment where PatientID = %s' #TODO: check if aptID also needs to be retrieved
        sel_data = (uid,)
        conn = self.connect.cursor()
        conn.execute(del_query, sel_data)
        self.connect.commit()
        self.tree.delete(selected_item)
        messagebox.showinfo("SUCCESS", 'Appointment data deleted')

    def select_data(self):
        curItem = self.tree.focus()
        values = self.tree.item(curItem, 'values')

        f = Frame(self.root, width=400, height=400, background='grey')
        f.place(x=100, y=250)

        patientID = StringVar()
        AppointmentID = StringVar()
        AppointmentDate = StringVar()
        AppointmentTypeID = StringVar()

        l1 = Label(f, text='PatientID', width=8, font=('Times', 11, 'bold'))
        e1 = Entry(f, textvariable=patientID, width=25)
        l1.place(x=50, y=30)
        e1.place(x=170, y=30)

        l2 = Label(f, text='AppointmentID', width=8, font=('Times', 11, 'bold'))
        e2 = Entry(f, textvariable=AppointmentID, width=25)
        l2.place(x=50, y=70)
        e2.place(x=170, y=70)

        l3 = Label(f, text='AppointmentDate', width=8, font=('Times', 11, 'bold'))
        e3 = Entry(f, textvariable=AppointmentDate, width=25)
        l3.place(x=50, y=110)
        e3.place(x=170, y=110)

        l4 = Label(f, text='AppointmentTypeID', width=8, font=('Times', 11, 'bold'))
        e4 = Entry(f, textvariable=AppointmentTypeID, width=25)
        l4.place(x=50, y=110)
        e4.place(x=170, y=110)

        e1.insert(0, values[0])
        e2.insert(0, values[1])
        e3.insert(0, values[2])
        e4.insert(0, values[3])

        def update_data():
            a_PatientID = patientID.get()
            a_appointmentID = AppointmentID.get()
            a_AppointmentDate = AppointmentDate.get()
            a_appointmentTypeID = AppointmentTypeID.get()

            self.tree.item(curItem, values=(values[0], a_PatientID, a_appointmentID, a_AppointmentDate, a_appointmentTypeID))

            conn = self.connect.cursor()
            conn.execute(
                'UPDATE appointment SET PatientID=%s, appointmentID=%s, AppointmentDate=%s, AppointmentTypeID = %s WHERE PatientID=%s',
                (a_PatientID, a_appointmentID, a_AppointmentDate, a_appointmentTypeID, values[0]))

            self.connect.commit()
            messagebox.showinfo('SUCCESS', 'Appointment data updated')
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)

            f.destroy()

        savebutton = tk.Button(f, text="submit", command=update_data)
        savebutton.configure(font=('Times', 11, 'bold'), bg='green', fg='white')
        savebutton.place(x=100, y=360)
        cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
        cancelbutton.configure(font=('Times', 11, 'bold'), bg='red', fg='white')
        cancelbutton.place(x=200, y=360)


#create class appointmentType

#create class contact

#create employee

#create employee_appointment

#create employee_contact

#patient_relationship

#create relationship

#create relationshiptype

if __name__ == "__main__":
    root = tk.Tk()

    notebook = ttk.Notebook(root)

    # Create instance of PatientApp
    patient_app_frame = tk.Frame(notebook)
    patient_app = PatientApp(patient_app_frame)
    notebook.add(patient_app_frame, text="Patient Details")

    # Create instance of PatientContactApp
    patient_contact_frame = tk.Frame(notebook)
    patient_contact_app = PatientContactApp(patient_contact_frame)
    notebook.add(patient_contact_frame, text="Patient Contact Details")

    appointment_frame = tk.Frame(notebook)
    appointment_app = Appointment(appointment_frame)
    notebook.add(appointment_frame, text = "Appointment")

    notebook.pack(expand=True, fill="both")

    root.title("Main Application")
    root.mainloop()
