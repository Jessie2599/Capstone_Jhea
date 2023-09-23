import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import *
import pymysql

# Initialize a list to store information
recorded_data = []

# Initialize date_time_label as a global variable
date_time_label = None

# Initialize id_entry as a global variable
id_entry = None

# Initialize purpose_label as a global variable
purpose_label = None

# Initialize purposes_frame as a global variable
purposes_frame = None

# Initialize a variable to keep track of whether the entry is enabled
entry_enabled = True

# Initialize a variable to store the selected purpose
selected_purpose = None

db = None
cursor = None

def clear_entry():
    id_entry.delete(0, END)

def update_datetime():
    global date_time_label
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day_of_week = datetime.now().strftime("%A")
    date_time_label.config(text=f"{day_of_week}, {current_datetime}")
    date_time_label.after(1000, update_datetime)

def clear_and_restart():
    global  id_entry, purpose_label, purposes_frame, entry_enabled, selected_purpose
    id_entry.config(state=tk.NORMAL)  # Enable the entry widget
    id_entry.delete(0, tk.END)  # Clear any remaining text in the entry
    purpose_label.config(text="Purpose:")  # Clear the purpose label

    # Clear the displayed purposes in the purposes_frame
    for widget in purposes_frame.winfo_children():
        widget.destroy()

    entry_enabled = True
    selected_purpose = None

def restart():
    clear_and_restart()
    display_purposes(None)

def save_and_confirm_purpose(purpose):
    global id_entry, entry_enabled, selected_purpose
    id_number = id_entry.get()

    if id_number:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        recorded_data.append([id_number, current_datetime, purpose])
        connect = pymysql.connect(host='localhost', user='root', password="", database='libtraq_db')
        cursor = connect.cursor()
        library_id_get = id_entry.get()


        try:
            cursor.execute(f"INSERT INTO `library attendance` (`library_id`, `purpose`, `date_&_time`) VALUES ('{library_id_get}', '{purpose}', '{current_datetime}')")
            connect.commit()
            connect.close()
            messagebox.showinfo("Save Successfeul!")

            confirmation_message = f"ID: {id_number}\nDate and Time: {current_datetime}\nPurpose: {purpose}"
            result = messagebox.showinfo("Successfully Login!", confirmation_message)

            clear_entry()
            clear_and_restart()
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

def display_purposes(event):
    global  id_entry, purpose_label, purposes_frame, entry_enabled, selected_purpose  # Declare id_var, id_entry, purpose_label, purposes_frame, entry_enabled, and selected_purpose as global variables
    id_number = id_entry.get()

    if id_number and entry_enabled:
        purposes = [
            "Purpose",
            "a. Read Book",
            "b. Borrowed/Returned Books",
            "c. Connect Internet",
            "d. Research",
            "e. Go to the Librarian",
            "f. Others"
        ]

        # Clear the displayed purposes in the purposes_frame
        for widget in purposes_frame.winfo_children():
            widget.destroy()

        for i, purpose in enumerate(purposes[1:], start=1):  # Start from index 1 to skip "Purpose"
            tk.Label(purposes_frame, text=purpose, font=("Arial", 18)).pack()

        # Disable the entry widget after processing the ID number
        id_entry.config(state=tk.DISABLED)
        entry_enabled = False

def handle_purpose_key(key, purpose):
    global selected_purpose
    selected_purpose = purpose
    save_and_confirm_purpose(purpose)

def home():
    global date_time_label, id_entry, purpose_label, purposes_frame, home, entry_enabled, selected_purpose  # Declare date_time_label, id_var, id_entry, purpose_label, purposes_frame, home, entry_enabled, and selected_purpose as global variables
    home = tk.Tk()
    home.title("LibTraQ: Library Tracker and Monitoring System using QR Code")
    home.geometry("1366x768")
    home.resizable(height=False, width=False)

    date_time_label = tk.Label(home, text="", font=("Arial", 18))
    date_time_label.place(relx=0.03, rely=1.0, anchor=tk.SW)
    update_datetime()

    canvas = tk.Canvas(home, width=1600, height=1500)
    canvas.pack()

    background_image = tk.PhotoImage(file="images/student_background.png")
    background_label = tk.Label(canvas, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    id_label = tk.Label(home, text="Library Number:", font=("Arial", 20))
    id_label.place(x=660, y=360)

    id_entry = Entry(home, font=("Arial", 20))
    id_entry.place(x=865, y=360)
    id_entry.focus()

    id_entry.bind("<Return>", display_purposes)  # Bind Enter key press to display_purposes function

    purpose_label = tk.Label(home, text="Purpose:", font=("Arial", 20))
    purpose_label.place(x=660, y=410)

    # Create a frame to hold the dynamic labels for purposes
    purposes_frame = tk.Frame(home)
    purposes_frame.place(x=860, y=410)

    entry_enabled = True
    selected_purpose = None

    # Bind spacebar key to restart
    home.bind("<space>", lambda event: restart())

    # Bind keys a-f to handle_purpose_key
    home.bind("a", lambda event: handle_purpose_key("a", "Read Book"))
    home.bind("b", lambda event: handle_purpose_key("b", "Borrowed/Returned Books"))
    home.bind("c", lambda event: handle_purpose_key("c", "Connect Internet"))
    home.bind("d", lambda event: handle_purpose_key("d", "Research"))
    home.bind("e", lambda event: handle_purpose_key("e", "Go to the Librarian"))
    home.bind("f", lambda event: handle_purpose_key("f", "Others"))

    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'db': 'libtraq_db',
    }
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    home.mainloop()

home()
