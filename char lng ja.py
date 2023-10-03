import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

def connection():
    conn=pymysql.connect(host="localhost", user="root", password="", database="libtraq_db")
    return conn

def refreshTable():
    for date in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag='orow')

    my_tree.tag_configure('orow', background='', font=("Arial", 12))
    my_tree.place(x=10, y=200)

root = Tk()
root.title("List of Student")
root.geometry("1380x720")
my_tree = ttk.Treeview(root)

def read():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM library_attendance")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10))
my_tree['columns']=("ID Number","First Name","Middle Name","Last Name","Course","Purpose","Date & Time")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID Number", anchor=W, width=160)
my_tree.column("First Name", anchor=W, width=160)
my_tree.column("Middle Name",anchor=W,  width=160)
my_tree.column("Last Name",anchor=W,  width=160)
my_tree.column("Course", anchor=W, width=160)
my_tree.column("Purpose",anchor=W,  width=180)
my_tree.column("Date & Time", anchor=W, width=165)

my_tree.heading("ID Number", text="ID Number", anchor=W,)
my_tree.heading("First Name", text="First Name", anchor=W,)
my_tree.heading("Middle Name", text="Middle Name", anchor=W,)
my_tree.heading("Last Name", text="Last Name", anchor=W,)
my_tree.heading("Course", text="Course", anchor=W,)
my_tree.heading("Purpose", text="Purpose", anchor=W,)
my_tree.heading("Date & Time", text="Date & Time", anchor=W,)

refreshTable()

root.mainloop()
