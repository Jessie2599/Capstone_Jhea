import tkinter as tk
from tkinter import ttk, Entry, messagebox, END, scrolledtext
from datetime import datetime
import pymysql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import PhotoImage


# Global variables
recorded_data = []
date_time_label = None
id_entry = None
purpose_label = None
purposes_frame = None
entry_enabled = True
selected_purpose = None
db = None
cursor = None

def clear_entry():
    id_entry.delete(0, tk.END)

def update_datetime():
    global date_time_label
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day_of_week = datetime.now().strftime("%A")
    date_time_label.config(text=f"{day_of_week}, {current_datetime}")
    date_time_label.after(1000, update_datetime)

def clear_and_restart():
    global id_entry, purpose_label, purposes_frame, entry_enabled, selected_purpose
    id_entry.config(state=tk.NORMAL)
    id_entry.delete(0, tk.END)
    purpose_label.config(text="Purpose:")
    for widget in purposes_frame.winfo_children():
        widget.destroy()
    entry_enabled = True
    selected_purpose = None

def restart():
    clear_and_restart()
    display_purposes(None)


def show_record_confirmation(id_number, first_name, middle_name, last_name, course, current_datetime, purpose,
                             academic_year, semester):
    confirmation_window = tk.Toplevel()
    confirmation_window.title("Successfully Logged In!")

    confirmation_message = f"ID: {id_number}\nFirst Name: {first_name}\nMiddle Name: {middle_name}\nLast Name: {last_name}\nCourse: {course}\nDate and Time: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\nPurpose: {purpose}\nAcademic Year: {academic_year}\nSemester: {semester}"

    confirmation_label = tk.Label(confirmation_window, text=confirmation_message, padx=20, pady=20)
    confirmation_label.pack()

    # Optionally, you can add a button to close the confirmation window.
    close_button = tk.Button(confirmation_window, text="Close", command=confirmation_window.destroy)
    close_button.pack()


# ... (the rest of your code) ...

def save_and_confirm_purpose(purpose):
    global id_entry, entry_enabled, selected_purpose
    id_number = id_entry.get()

    if id_number:
        current_datetime = datetime.now()
        current_year = current_datetime.year
        current_month = current_datetime.month
        academic_year = current_year

        # Determine the semester based on the current month
        if 8 <= current_month <= 12:
            # If the current month is August to December, set the semester to "1st Semester"
            semester = "1st Semester"
        elif 1 <= current_month <= 6:
            # If the current month is January to June, set the semester to "2nd Semester"
            semester = "2nd Semester"
        else:
            # Handle cases where the month is not in the range (e.g., July)
            semester = "N/A"

        unique_id = f"{id_number}-{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        recorded_data.append([unique_id, current_datetime.strftime('%Y-%m-%d %H:M:%S'), purpose])
        connect = pymysql.connect(host='localhost', user='root', password="", database='libtraq_db')
        cursor = connect.cursor()

        try:
            cursor.execute("SELECT first_name, middle_name, last_name, course FROM student WHERE id_no = %s",
                           (id_number,))
            result = cursor.fetchone()

            if result:
                first_name, middle_name, last_name, course = result
                cursor.execute(
                    "INSERT INTO `library_attendance` (`id_no`, `first_name`, `middle_name`, `last_name`, `course`, `purpose`, `date_and_time`, `academic_year`, `semester`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (unique_id, first_name, middle_name, last_name, course, purpose,
                     current_datetime.strftime('%Y-%m-%d %H:%M:%S'), academic_year, semester))
                connect.commit()
                connect.close()

                show_record_confirmation(id_number, first_name, middle_name, last_name, course, current_datetime,
                                         purpose, academic_year, semester)
                clear_entry()
                clear_and_restart()
            else:
                messagebox.showerror("Error", "ID Number not found in the 'student' table.")
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

def check_id_number(id_number):
    connect = pymysql.connect(host='localhost', user='root', password="", database='libtraq_db')
    cursor = connect.cursor()
    cursor.execute("SELECT id_no FROM student WHERE id_no = %s", (id_number,))
    result = cursor.fetchone()
    connect.close()
    return result is not None

def display_purposes(event):
    global id_entry, entry_enabled, selected_purpose
    id_number = id_entry.get()

    if id_number and entry_enabled:
        if check_id_number(id_number):
            purposes = [
                "a. Read A Book",
                "b. Borrow and Return Book",
                "c. Connect to the Internet",
                "d. Research",
                "e. Appointment with the Librarian",
                "f. Others"
            ]

            for widget in purposes_frame.winfo_children():
                widget.destroy()

            for i, purpose in enumerate(purposes, start=1):
                purpose_button = tk.Button(purposes_frame, text=purpose, font=("Arial", 15), anchor="w", command=lambda purpose=purpose: save_and_confirm_purpose(purpose))
                purpose_button.pack(fill="x")

            id_entry.config(state=tk.DISABLED)
            entry_enabled = False
        else:
            messagebox.showerror("Error", "Invalid ID Number. Please try again.")

def handle_purpose_key(key, purpose):
    global selected_purpose
    selected_purpose = purpose
    save_and_confirm_purpose(purpose)

def fetch_data_and_create_graph():
    try:
        connect = pymysql.connect(host='localhost', user='root', password="", database='libtraq_db')
        cursor = connect.cursor()

        cursor.execute("SELECT course, COUNT(*) FROM library_attendance GROUP BY course")
        results = cursor.fetchall()
        connect.close()

        if not results:
            messagebox.showerror("Error", "No attendance data found.")
            return

        courses, counts = zip(*results)
        total_count = sum(counts)

        percentages = [count / total_count * 100 for count in counts]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(courses, counts, color='blue')

        ax.set_xlabel('Course')
        ax.set_ylabel('Attendance Count')
        ax.set_title('Attendance by Course')
        ax.tick_params(axis='x', rotation=45)

        for bar, percentage in zip(bars, percentages):
            height = bar.get_height()
            ax.annotate(f'{percentage:.2f}%', (bar.get_x() + bar.get_width() / 2, height),
                        ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=home)
        canvas.get_tk_widget().place(x=20, y=330)
        canvas.draw()
    except pymysql.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def generate_leaderboard():
    try:
        connect = pymysql.connect(host='localhost', user='root', password="", database='libtraq_db')
        cursor = connect.cursor()

        cursor.execute("SELECT first_name, middle_name, last_name, course, purpose, COUNT(*) as attendance_count FROM library_attendance GROUP BY first_name, middle_name, last_name, course, purpose ORDER BY attendance_count DESC LIMIT 10")
        results = cursor.fetchall()
        connect.close()

        if not results:
            messagebox.showerror("Error", "No attendance data found.")
            return

        leaderboard_label = tk.Label(home, text="Top Ten Visitors", font=("Arial", 15, "bold"))
        leaderboard_label.place(x=20, y=45)

        leaderboard_tree = ttk.Treeview(home, columns=("Name", "Course", "Purpose", "No. of Visits"), show="headings", height=10)
        leaderboard_tree.heading("Name", text="Name", anchor="center")
        leaderboard_tree.heading("Course", text="Course", anchor="center")
        leaderboard_tree.heading("Purpose", text="Purpose", anchor="center")
        leaderboard_tree.heading("No. of Visits", text="No. of Visits", anchor="center")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        leaderboard_tree.column("Name", width=150)
        leaderboard_tree.column("Course", width=120)
        leaderboard_tree.column("Purpose", width=190)
        leaderboard_tree.column("No. of Visits", width=130)

        leaderboard_tree.place(x=20, y=80)

        for index, (first_name, middle_name, last_name, course, purpose, attendance_count) in enumerate(results, start=1):
            name = f"{first_name} {middle_name} {last_name}"
            leaderboard_tree.insert("", "end", values=(name, course, purpose, attendance_count))

    except pymysql.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Create the main window
home = tk.Tk()
home.title("LibTraQ: Library Tracker and Monitoring System using QR Code")
home.geometry("1366x768")
home.resizable(height=False, width=False)


def open_book_window():
    book_window = tk.Toplevel(home)
    book_window.title("Book")
    book_window.geometry("420x345")

    def search_data():
        search_query = search_entry.get().strip().lower()

        for row in my_tree.get_children():
            my_tree.delete(row)

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book_info")
        rows = cursor.fetchall()

        for row in rows:
            if any(search_query in str(cell).strip().lower() for cell in row):
                my_tree.insert("", "end", values=row)

        conn.close()

    search_label = tk.Label(book_window, text="Search Book:", font=("Arial", 12))
    search_label.pack()

    search_entry = tk.Entry(book_window, font=("Arial", 12))
    search_entry.pack()

    search_button = tk.Button(book_window, text="Search", font=("Arial", 12), command=search_data)
    search_button.pack()

    def refreshTable():
        for date in my_tree.get_children():
            my_tree.delete(date)

        for array in read():
            my_tree.insert(parent='', index='end', iid=array, values=array, tag='orow')
            my_tree.place(x=10, y=100)

    def read():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book_info")
        results = cursor.fetchall()
        conn.close()
        return results

    def connection():
        conn = pymysql.connect(host="localhost", user="root", password="", database="libtraq_db")
        return conn

    my_tree = ttk.Treeview(book_window, height=10)

    my_tree['columns'] = ("ISBN", "Book Name", "Author", "Book Copies")

    my_tree.column("#0", width=0, stretch=tk.NO)
    my_tree.column("ISBN", anchor="center", width=100)
    my_tree.column("Book Name", anchor="center", width=100)
    my_tree.column("Author", anchor="center", width=100)
    my_tree.column("Book Copies", anchor="center", width=100)

    my_tree.heading("ISBN", text="ISBN", anchor="center")
    my_tree.heading("Book Name", text="Book Name", anchor="center")
    my_tree.heading("Author", text="Author", anchor="center")
    my_tree.heading("Book Copies", text="Book Copies", anchor="center")

    my_tree.pack()
    refreshTable()


def open_marquee_window():
    marquee_window = tk.Toplevel()
    marquee_window.title("Library Announcement")
    marquee_window.geometry("300x200")  # Set the size of the window (width x height)

    marquee_label = tk.Label(marquee_window, text="Enter Announcement:", font=("Arial", 16))
    marquee_label.pack()

    # Make the Entry widget multi-line with a smaller height
    marquee_entry = scrolledtext.ScrolledText(marquee_window, font=("Arial", 16), height=5)  # Adjust height as needed
    marquee_entry.pack()

    def display_marquee_message():
        message = marquee_entry.get("1.0", tk.END)
        marquee_message.config(text=message)
        marquee_window.destroy()

    submit_button = tk.Button(marquee_window, text="Submit", font=("Arial", 16), command=display_marquee_message)
    submit_button.pack()

# Create and update the date and time label
date_time_label = tk.Label(home, text="", font=("Arial", 18))
date_time_label.place(relx=0.03, rely=1.0, anchor=tk.SW)
update_datetime()

# Create a canvas for background
canvas = tk.Canvas(home, width=1600, height=1500)
canvas.pack()

# Create and populate the Treeview widget
my_tree = ttk.Treeview(home, height=20)
my_tree['columns'] = ("ID Number", "First Name", "Middle Name", "Last Name", "Course", "Purpose", "Date & Time")

my_tree.column("#0", width=0, stretch=tk.NO)
my_tree.column("ID Number", anchor="center", width=120)
my_tree.column("First Name", anchor="center", width=120)
my_tree.column("Middle Name", anchor="center", width=120)
my_tree.column("Last Name", anchor="center", width=120)
my_tree.column("Course", anchor="center", width=110)
my_tree.column("Purpose", anchor="center", width=150)
my_tree.column("Date & Time", anchor="center", width=150)

my_tree.heading("ID Number", text="ID Number", anchor="center")
my_tree.heading("First Name", text="First Name", anchor="center")
my_tree.heading("Middle Name", text="Middle Name", anchor="center")
my_tree.heading("Last Name", text="Last Name", anchor="center")
my_tree.heading("Course", text="Course", anchor="center")
my_tree.heading("Purpose", text="Purpose", anchor="center")
my_tree.heading("Date & Time", text="Date & Time", anchor="center")

my_tree.pack()

# Create a background image
background_image = tk.PhotoImage(file="images/student_background.png")
background_label = tk.Label(canvas, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

id_label = tk.Label(home, text="Library Number:", font=("Arial", 20))
id_label.place(x=730, y=250)

id_entry = Entry(home, font=("Arial", 20))
id_entry.place(x=946, y=250)
id_entry.focus()

id_entry.bind("<Return>", display_purposes)

purpose_label = tk.Label(home, text="Purpose:", font=("Arial", 20))
purpose_label.place(x=730, y=310)

purposes_frame = tk.Frame(home)
purposes_frame.place(x=945, y=310)

entry_enabled = True
selected_purpose = None

home.bind("<space>", lambda event: restart())

home.bind("a", lambda event: handle_purpose_key("a", "Read Book"))
home.bind("b", lambda event: handle_purpose_key("b", "Borrowed/Returned Books"))
home.bind("c", lambda event: handle_purpose_key("c", "Connect Internet"))
home.bind("d", lambda event: handle_purpose_key("d", "Research"))
home.bind("e", lambda event: handle_purpose_key("e", "Go to the Librarian"))
home.bind("f", lambda event: handle_purpose_key("f", "Others"))

# Create buttons to fetch data, create the graph, and generate the leaderboard
fetch_and_generate_button = tk.Button(home, bg="orange", text="Leaderboard", font=("Arial", 16), command=lambda: [fetch_data_and_create_graph(), generate_leaderboard()])
fetch_and_generate_button.place(x=195, y=15)

# Create a button to refresh the data, graph, and leaderboard
refresh_button = tk.Button(home, bg="orange", text="Refresh", font=("Arial", 16), command=lambda: [fetch_data_and_create_graph(), generate_leaderboard()])
refresh_button.place(x=335, y=15)

marquee_button = tk.Button(home, bg="orange", text="Announcement", font=("Arial", 16), command=open_marquee_window)
marquee_button.place(x=430, y=15)

# Create a label to display the marquee message
marquee_message = tk.Label(home, text="", font=("Arial", 16), fg="blue", wraplength=1000)
marquee_message.place(x=730, y=600)

book_button = tk.Button(home, bg="orange", text="Book", font=("Arial", 16), command=open_book_window)
book_button.place(x=590, y=15)

# Run the main loop
home.mainloop()
