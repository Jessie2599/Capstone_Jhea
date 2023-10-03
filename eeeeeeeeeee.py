import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import qrcode
from tkinter import filedialog
from tkcalendar import DateEntry
import keyboard
import pymysql



root = Tk()
root.title("List of Student")
root.geometry("1080x720")
my_tree = ttk.Treeview(root)

label = Label(window, text="List of Student", font=("Arial Bold", 20))
label.place(y=10, x=10)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial Bold", 20))
my_tree['column']=("ID Number","First Name","Middle Name","Last Name","Sex","Course","Status","QR Code","Photo")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID Number", width=147)
my_tree.column("First Name", width=147)
my_tree.column("Middle Name", width=147)
my_tree.column("Last Name", width=147)
my_tree.column("Sex", width=147)
my_tree.column("Course", width=147)
my_tree.column("Status", width=147)
my_tree.column("QR Code", width=147)
my_tree.column("Photo", width=147)

my_tree.heading("ID Number", text="ID Number")
my_tree.heading("First Name", text="First Name")
my_tree.heading("Middle Name", text="Middle Name")
my_tree.heading("Last Name", text="Last Name")
my_tree.heading("Sex", text="Sex")
my_tree.heading("Course", text="Course")
my_tree.heading("Status", text="Status")
my_tree.heading("QR Code", text="QR Code")
my_tree.heading("Photo", text="Photo")

        # Set column widths


root.mainloop()
