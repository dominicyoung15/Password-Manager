from tkinter import *
import tkinter as tk
from tkinter import messagebox
import time
import random
import sqlite3

global root
global registerScreen

root = tk.Tk()
root.geometry('500x350')
root.title("Login Form")

conn=sqlite3.connect('LoginDatabase.db')

nameVar=StringVar()
emailVar=StringVar()
passVar=StringVar()
confirmVar=StringVar()
genderVar = IntVar()
javaVar= IntVar()

def addNew():
    try:
        if passVar.get() != confirmVar.get():
            messagebox.showwarning(title="Error", message="Passwords do not match") 
            print('Signup Error')
    except:
            messagebox.showinfo(title='Success', message='Account Registration Successful')
            registerScreen.destroy()
            name=nameVar.get()
            email=emailVar.get()
            password=passVar.get()
            confirm=confirmVar.get()
            gender=genderVar.get()
            conn = sqlite3.connect('LoginDatabase.db')
            with conn:
                cursor=conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS detailsTable (Name TEXT,Email TEXT,Password TEXT,Confirm TEXT,Gender TEXT)')
            count=cursor.execute('INSERT INTO detailsTable (Name,Email,Password,Confirm,Gender) VALUES(?,?,?,?,?)',(name,email,password,confirm,gender))
            
            if(cursor.rowcount>0):
                print ("Signup Done")
            else:
                print ("Signup Error")
            
            conn.commit()
            registerScreen.destroy()

    name=nameVar.get()
    email=emailVar.get()
    password=passVar.get()
    confirm=confirmVar.get()
    gender=genderVar.get()
    conn = sqlite3.connect('LoginDatabase.db')
    with conn:
        cursor=conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS detailsTable (Name TEXT,Email TEXT,Password Text,Confirm TEXT, Gender TEXT)')
    count=cursor.execute('INSERT INTO detailsTable (Name,Email,Password,Confirm,Gender) VALUES(?,?,?,?,?)',(name,email,password,confirm,gender))
    
    if(cursor.rowcount>0):
        print ("Signup Done")
    else:
        print ("Signup Error")
    
    conn.commit()
    registerScreen.destroy()


def loginNow():
    email=emailVar.get()
    password=passVar.get()
    confirm=confirmVar.get()
    conn = sqlite3.connect('LoginDatabase.db')
    with conn:
        cursor=conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS detailsTable (Name TEXT,Email TEXT,Password Text,Gender TEXT)')
    cursor.execute('Select * from detailsTable Where Email=? AND Password=?',(email,password))

    if cursor.fetchone() is not None:
        print ("Welcome")
        messagebox.showinfo(title="Login Success", message="Login details are correct")
        time.sleep(1)
        root.destroy()
        mainframe = Tk()
        mainframe.title('Password Manager')
        mainframe.geometry('400x200')
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS passwords (
            webname text,
            username text,
            password text
            ) """)
        conn.commit()
        conn.close()

        # functions
        def edit_idselect():
            global chooser
            global delete_box
            chooser = Tk()
            chooser.title('Update Record')
            chooser.geometry('400x100')
            delete_label = Label(chooser, text=('Select ID'))
            delete_label.grid(row=0, column=0, padx=10, pady=10)
            delete_box = Entry(chooser, width=30)
            delete_box.grid(row=0, column=1)
            update_btn = Button(chooser, text=('Update Record'), command=updaterec)
            update_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

        def del_idselect():
            global chooser
            global delete_box
            chooser = Tk()
            chooser.title('Delete Record')
            chooser.geometry('400x100')
            delete_label = Label(chooser, text=('Select ID'))
            delete_label.grid(row=0, column=0, padx=10, pady=10)
            delete_box = Entry(chooser, width=30)
            delete_box.grid(row=0, column=1)
            update_btn = Button(chooser, text=('Delete Record'), command=deleterec)
            update_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

        def deleterec():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            c.execute('DELETE FROM passwords WHERE oid = ' + delete_box.get())
            conn.commit()
            conn.close()
            delete_box.delete(0, END)
            chooser.destroy()

        def saverec():
            record_id = delete_box.get()
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            c.execute("""UPDATE passwords SET
                    webname = :webname,
                    username = :username,
                    password = :password

                    WHERE oid = :oid""",
                    {
                    'webname': webname_box_edit.get(),
                    'username': username_box_edit.get(),
                    'password': password_box_edit.get(),
                    'oid': record_id
                    })
            conn.commit()
            conn.close()
            webname_box_edit.delete(0, END)
            username_box_edit.delete(0, END)
            password_box_edit.delete(0, END)
            delete_box.delete(0, END)
            chooser.destroy()
            updater.destroy()
            try:
                recspg.destroy()
            except: 
                return
            else: 
                return	


        def updaterec():
            global updater
            global delete_label
            global delete_box
            updater = Tk()
            updater.title('Update Record')
            global webname_box_edit
            global username_box_edit
            global password_box_edit
            webname_edit = Label(updater, text=('Website name: '))
            webname_edit.grid(row=1, column=0, pady=10)
            username_edit = Label(updater, text=('Please enter Username: '))
            username_edit.grid(row=2, column=0, pady=10)
            password_edit = Label(updater, text=('Please enter Password: '))
            password_edit.grid(row=3, column=0, pady=10)
            
            # text boxes
            webname_box_edit= Entry(updater, width=30)
            webname_box_edit.grid(row=1, column=1, padx=10, pady=10)
            username_box_edit = Entry(updater, width=30)
            username_box_edit.grid(row=2, column=1)
            password_box_edit = Entry(updater, width=30)
            password_box_edit.grid(row=3, column=1)
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            record_id = delete_box.get()
            c.execute('SELECT * FROM passwords WHERE oid= ' + delete_box.get())
            records = c.fetchall()
            for record in records:
                webname_box_edit.insert(0, record[0])
                username_box_edit.insert(0, record[1])
                password_box_edit.insert(0, record[2])
            save_btn = Button(updater, text=('Save Changes'), command=saverec)
            save_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            conn.commit()
            conn.close()

        def query():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            global query_frame
            query_frame = Tk()
            query_frame.title('Records')
            
            # buttons + functions
            all_btn = Button(query_frame, text=('Show All Records'), command=allrecs)
            all_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            delete_btn = Button(query_frame, text=('Delete Record'), command=del_idselect)
            delete_btn.grid(row=6, column=0, pady=10, padx=10, ipadx=110)
            update_btn = Button(query_frame, text=('Update Record'), command=edit_idselect)
            update_btn.grid(row=7, column=0, pady=10, padx=10, ipadx=110)
            close_btn = Button(query_frame, text=('Close Page'), command=closedb_)
            close_btn.grid(row=8, column=0, pady=10, padx=10, ipadx=120)
            search_btn = Button(query_frame, text=('Search Records'), command=search)
            search_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10, ipadx=105)
            
            conn.commit()
            conn.close()

        def closedb_():
            query_frame.destroy()

        def allrecs():
                conn = sqlite3.connect('password_manager.db')
                c = conn.cursor()
                global recspg
                recspg = Tk()
                recspg.title('All Records')
                c.execute('SELECT *, oid FROM passwords')
                records = c.fetchall()
                print_records = ''
                for record in records:
                    print_records += "Website: " + record[0] + "    Username: " + record[1] + "    Password: " + record[2] + "   ID: " + str(record[3]) + "\n" 
                query_label = Label(recspg, text=print_records)
                query_label.grid(row=4, column=0, columnspan=2)
                conn.commit()
                conn.close()

        def addnew():
            global add_new
            add_new = Tk()
            add_new.title('Add details to database')
            
            # labels
            global webname
            global username
            global password
            global webname_box
            global username_box
            global password_box
            webname = Label(add_new, text=('Website name: '))
            webname.grid(row=0, column=0, pady=10)
            username = Label(add_new, text=('Please enter Username: '))
            username.grid(row=1, column=0, pady=10)
            password = Label(add_new, text=('Please enter Password: '))
            password.grid(row=2, column=0, pady=10)
            
            # text boxes
            webname_box = Entry(add_new, width=30)
            webname_box.grid(row=0, column=1, padx=10, pady=10)
            username_box = Entry(add_new, width=30)
            username_box.grid(row=1, column=1)
            password_box = Entry(add_new, width=30)
            password_box.grid(row=2, column=1)
            
            # add button
            ad_btn = Button(add_new, text=('Add details to manager'), command=add_db)
            ad_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=135)

        def add_db():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            c.execute('INSERT INTO passwords VALUES (:webname, :username, :password)',
                {
                'webname': webname_box.get(),
                'username': username_box.get(),
                'password': password_box.get()
                })
            conn.commit()
            conn.close()	
            webname_box.delete(0, END)
            username_box.delete(0, END)
            password_box.delete(0, END)
            add_new.destroy()

        def close_db():
            add_new.destroy()
            add2db = Button(add_new, text=('Add details to database'), command=add_db)
            add2db.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            closedb = Button(add_new, text=('Close Page'), command=close_db)
            closedb.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipadx=135)

        def generate():
            global webname_box_gen
            global username_box_gen
            global password_box_gen
            global generate
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            generate = Tk()
            generate.title('Generate a password')
            
            # labels
            webname_gen = Label(generate, text=('Website name: '))
            webname_gen.grid(row=0, column=0, pady=10)
            username_gen = Label(generate, text=('Please enter Username: '))
            username_gen.grid(row=1, column=0, pady=10)
            password_gen = Label(generate, text=('Please enter Password: '))
            password_gen.grid(row=2, column=0, pady=10)
            
            # text boxes
            webname_box_gen = Entry(generate, width=30)
            webname_box_gen.grid(row=0, column=1, padx=10, pady=10)
            username_box_gen = Entry(generate, width=30)
            username_box_gen.grid(row=1, column=1)
            password_box_gen = Entry(generate, width=30)
            password_box_gen.grid(row=2, column=1)
            lower_case = 'abcdefghijklmnopqrstuvwxyz'
            upper_case = lower_case.upper()
            number = '0123456789'
            symbols = "@#$%*/\?|£'"
            use_for = lower_case + upper_case + symbols + number
            length_for_pass = 15
            password_generate = "".join(random.sample(use_for, length_for_pass))
            password_box_gen.insert(0, password_generate)
            
            # buttons
            add_btn = Button(generate, text=('Add details to manager'), command=adddb)
            add_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=135)
            conn.commit()
            conn.close()
            try:
                recspg.destroy()
            except: 
                return
            else:
                return

        def adddb():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            c.execute('INSERT INTO passwords VALUES (:webname, :username, :password)',
                {
                'webname': webname_box_gen.get(),
                'username': username_box_gen.get(),
                'password': password_box_gen.get()
                })
            conn.commit()
            conn.close()	
            webname_box_gen.delete(0, END)
            username_box_gen.delete(0, END)
            password_box_gen.delete(0, END)
            generate.destroy()

        def usersearch():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            global user_search
            global usersearch_label
            global usersearch_entry
            user_search = Tk()
            user_search.title('Search Database by Username')
            usersearch_label = Label(user_search, text=('Username'))
            usersearch_label.grid(row=0, column=0)
            usersearch_entry = Entry(user_search, width=30,)
            usersearch_entry.grid(row=0, column=1)
            search_btn = Button(user_search, text=('Search Records'), command=searchuser)
            search_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            conn.commit()
            conn.close()

        def searchuser():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            usersearch = c.execute('SELECT *, oid FROM passwords WHERE username= :username',
            {
                'username': usersearch_entry.get()
            } )
            records = c.fetchall()
            print_search = ''
            for record in records:
                print_search += "Website: " + record[0] + "    Username: " + record[1] + "    Password: " + record[2] + "   ID: " + str(record[3]) + "\n" 
            recs = Label(user_search, text=print_search)
            recs.grid(row=2, column=0, columnspan=4)
            conn.commit()
            conn.close()

        def websearch():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            global web_search
            global websearch_label
            global websearch_entry
            web_search = Tk()
            web_search.title('Search Database by Webname')
            websearch_label = Label(web_search, text=('Webname'))
            websearch_label.grid(row=0, column=0)
            websearch_entry = Entry(web_search, width=30,)
            websearch_entry.grid(row=0, column=1)
            search_btn = Button(web_search, text=('Search Records'), command=searchweb)
            search_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            conn.commit()
            conn.close()

        def searchweb():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            websearch = c.execute('SELECT *, oid FROM passwords WHERE webname= :webname', 
            {
                'webname': websearch_entry.get()
            })
            records = c.fetchall()
            print_search = ''
            for record in records:
                print_search += "Website: " + record[0] + "    Username: " + record[1] + "    Password: " + record[2] + "   ID: " + str(record[3]) + "\n" 
            recs = Label(web_search, text=print_search)
            recs.grid(row=2, column=0, columnspan=4)
            conn.commit()
            conn.close()

        def pass_search():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            global pass_search
            global passsearch_label
            global passsearch_entry
            pass_search = Tk()
            pass_search.title('Search Database by Password')
            passsearch_label = Label(pass_search, text=('Password'))
            passsearch_label.grid(row=0, column=0)
            passsearch_entry = Entry(pass_search, width=30,)
            passsearch_entry.grid(row=0, column=1)
            search_btn = Button(pass_search, text=('Search Records'), command=searchpass)
            search_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            conn.commit()
            conn.close()	

        def searchpass():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            passsearch = c.execute('SELECT *, oid FROM passwords WHERE password= :webname', 
            {
                'webname': passsearch_entry.get()
            })
            records = c.fetchall()
            print_search = ''
            for record in records:
                print_search += "Website: " + record[0] + "    Username: " + record[1] + "    Password: " + record[2] + "   ID: " + str(record[3]) + "\n" 
            recs = Label(pass_search, text=print_search)
            recs.grid(row=2, column=0, columnspan=4)
            conn.commit()
            conn.close()

        def oidsearch():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            global oid_search
            global oidsearch_label
            global oidsearch_entry
            oid_search = Tk()
            oid_search.title('Search Database by OID')
            oidsearch_label = Label(oid_search, text=('OID'))
            oidsearch_label.grid(row=0, column=0)
            oidsearch_entry = Entry(oid_search, width=30,)
            oidsearch_entry.grid(row=0, column=1)
            oid_btn = Button(oid_search, text=('Search Records'), command=searchoid)
            oid_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            conn.commit()
            conn.close()	

        def searchoid():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            oidsearch = c.execute('SELECT *, oid FROM passwords WHERE oid= :oid',
            {
                'oid': oidsearch_entry.get()
            })
            records = c.fetchall()
            print_search = ''
            for record in records:
                print_search += "Website: " + record[0] + "    Username: " + record[1] + "    Password: " + record[2] + "   ID: " + str(record[3]) + "\n" 
            recs = Label(oid_search, text=print_search)
            recs.grid(row=2, column=0, columnspan=4)
            conn.commit()
            conn.close()

        def search():
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            searchrecs = Tk()
            searchrecs.title('Search Records')

            # buttons
            web_btn = Button(searchrecs, text=('Search Site Name'), command=websearch)
            web_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            user_btn = Button(searchrecs, text=("Search Username"), command=usersearch)
            user_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            pass_btn = Button(searchrecs, text=('Search Password'), command=pass_search)
            pass_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=100)
            oid_btn = Button(searchrecs, text=('Search OID'), command=oidsearch)
            oid_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=110)

        def closepg():
            mainframe.destroy()
            
        # buttons
        adds_btn = Button(mainframe, text=('Add details to records'), command=addnew)
        adds_btn.grid(row=0, column=0, columnspan=1, padx=10, pady=10, ipadx=100)
        generate_btn = Button(mainframe, text=('Generate details for records'), command=generate)
        generate_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=80)
        query_btn = Button(mainframe, text=('Records'), command=query)
        query_btn.grid(row=2, column=0, columnspan=1, padx=10, pady=10, ipadx=140)
        close_btn = Button(mainframe, text=('Close'), command=closepg)
        close_btn.grid(row=3, column=0, columnspan=1, padx=10, pady=10, ipadx=150)

        mainframe = mainloop()
    else:
        print("Login failed")
        messagebox.showwarning(title="Login failed", message='Login details incorrect')

def registerWindow(): 
    
    global registerScreen
    global passEntry
    global confirmPasswordEntry
    registerScreen=Toplevel(root)
    
    registerScreen.title("Registration Here")
    
    registerScreen.geometry('500x500')
    
    label = Label(registerScreen, text="Registration Here",width=20,fg="white",font=("bold", 20))
    label.place(x=125,y=53)


    nameLabel = Label(registerScreen, text="FullName",width=20,font=("bold", 10))
    nameLabel.place(x=80,y=130)

    nameEntery = Entry(registerScreen,textvar=nameVar)
    nameEntery.place(x=240,y=130)

    emailLabel = Label(registerScreen, text="Email",width=20,font=("bold", 10))
    emailLabel.place(x=68,y=180)

    emailEntry = Entry(registerScreen,textvar=emailVar)
    emailEntry.place(x=240,y=180)

    passLabel = Label(registerScreen, text="Password",width=20,font=("bold", 10))
    passLabel.place(x=78,y=230)

    passEntry = Entry(registerScreen,textvar=passVar,show='*')
    passEntry.place(x=240,y=230)

    genderLabel = Label(registerScreen, text="Gender",width=20,font=("bold", 10))
    genderLabel.place(x=78,y=330)

    confirmPasswordEntry = Label(registerScreen, text="Confirm Password", width=20, font=("bold", 10))
    confirmPasswordEntry.place(x=78, y=280)

    confirmPasswordEntry = Entry(registerScreen, textvar=confirmVar, show='*')
    confirmPasswordEntry.place(x=240, y=280)

    Radiobutton(registerScreen, text="Male",padx = 5, variable=genderVar, value=1).place(x=235,y=330)
    Radiobutton(registerScreen, text="Female",padx = 20, variable=genderVar, value=2).place(x=295,y=330)

    Button(registerScreen, text='Submit',width=20,pady=5,command=addNew).place(x=150,y=380)



label = Label(root, text="Login Here",width=20,fg="white",font=("bold", 30))
label.place(x=68,y=53)


emailLabel = Label(root, text="Email",width=20,font=("bold", 10))
emailLabel.place(x=68,y=130)

emailEntry = Entry(root,textvar=emailVar)
emailEntry.place(x=240,y=130)

passwordLabel = Label(root, text="Password",width=20,font=("bold", 10))
passwordLabel.place(x=68,y=180)

passwordEntry = Entry(root,textvar=passVar,show='*')
passwordEntry.place(x=240,y=180)


Button(root, text='Login Now',width=20,pady=5,command=loginNow).place(x=150,y=230)

Button(root,text="Have no Account! Create one",width=20,command=registerWindow).place(x=150,y=280)

root.mainloop()