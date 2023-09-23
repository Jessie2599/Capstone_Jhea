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
from tkinter import Frame
import sqlite3


PIN = "1234"

def verify_pin(event=None):
    pin = pin_entry.get()
    if pin == PIN:
            open_system()
    else:
        messagebox.showerror("Invalid PIN", "Your PIN is invalid.")

def open_system():
    window.destroy()
    second_window()

def second_window():
    try:
        conn = sqlite3.connect('libtraq_db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT `library_id`, `name`, `course`, `purpose`, `date_&_time` FROM `library attendance`")
        row = cursor.fetchall()
        for row in rows:
            researcher_table.insert("", "end", values=row)

    except sqlite3.Error as e:
        print("SQLite error:", e)
    except Exception as e:
        print("An error occurred:", e)

    global second_window
    second_window = tk.Tk()
    second_window.geometry("1366x768")
    second_window.resizable(height=False, width=False)
    second_window.title("LibTraQ: Library Tracker and Monitoring System using QR Code")

    title_label = tk.Label(second_window, text="Library Tracker and Monitoring System Using QR Code", bg="Silver", font=("Arial Rounded MT Bold", 30, "bold"), borderwidth=10, relief="ridge")
    title_label.place(x=0, y=0, relwidth=0.99, height=100)

    buttons_frame = tk.Frame(second_window)
    buttons_frame.place(x=1240, y=100)

    researcher_frame = tk.LabelFrame(second_window, text="Library Attendance", font=("Arial", 16))
    researcher_frame.place(x=0, y=110)

    researcher_table = ttk.Treeview(researcher_frame)
    researcher_table["columns"] = ("Library ID", "Name", "Course", "Purpose", "Date and Time")

    researcher_table.column("#0", width=0, stretch=tk.NO)
    researcher_table.column("Library ID", anchor=tk.W, width=246)
    researcher_table.column("Name", anchor=tk.W, width=246)
    researcher_table.column("Course", anchor=tk.W, width=246)
    researcher_table.column("Purpose", anchor=tk.W, width=246)
    researcher_table.column("Date and Time", anchor=tk.W, width=246)

    researcher_table.heading("#0", text="", anchor=tk.W)
    researcher_table.heading("Library ID", text="Library ID", anchor=tk.W)
    researcher_table.heading("Name", text="Name", anchor=tk.W)
    researcher_table.heading("Course", text="Course", anchor=tk.W)
    researcher_table.heading("Purpose", text="Purpose", anchor=tk.W)
    researcher_table.heading("Date and Time", text="Date and Time", anchor=tk.W)

    researcher_table.pack(fill=tk.BOTH, expand=True)

    def open_add_record_window():
        second_window.withdraw()

        def add_record_window_save_to_db():
            connect = pymysql.connect(host='localhost', user='root', password="", database='libtraq_db')
            cursor = connect.cursor()
            id_get = id_entry.get()
            fname_get = first_name_entry.get()
            mname_get = middle_name_entry.get()
            lname_get = last_name_entry.get()
            sex_get = sex_var.get()
            course_get = course_var.get()
            status_get = status_var.get()

            try:
                print(f"{id_get}, {fname_get}, {mname_get}, {lname_get}, {sex_get}, {course_get}, {status_get}")
                cursor.execute(f"INSERT INTO `student` (`id_no`, `first_name`, `middle_name`, `last_name`, `sex`, `course`, `status`) VALUES ('{id_get}', '{fname_get}', '{mname_get}', '{lname_get}', '{sex_get}', '{course_get}', '{status_get}')")
                connect.commit()
                connect.close()
                messagebox.showinfo("Save Successfeul!")

            except Exception as error:
                messagebox.showerror("Error", error)
                print(error)

        def open_file_dialog():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
            if file_path:
                display_selected_image(file_path)

        def display_selected_image(file_path):
            # Clear any existing content in the photo_box
            for widget in photo_box.winfo_children():
                widget.destroy()

            # Open the selected image using PIL
            image = Image.open(file_path)

            # Resize the image to fit the dimensions of the photo_box frame
            image = image.resize((210, 195), Image.LANCZOS)

            # Convert the PIL image to a Tkinter PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Create a label to display the image in the photo_box frame
            image_label = tk.Label(photo_box, image=photo)
            image_label.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected
            image_label.pack(fill="both", expand=True)

        def generate_qr_code():
            if len(student_records) > 0:
                id_number, first_name, middle_name, last_name, sex, course = student_records[-1]
                qr_data = f"ID: {id_number}\nName: {last_name}, {first_name} {middle_name}\nSex: {sex}\nCourse: {course}"
                messagebox.showinfo("QR Code", qr_data)

        add_record_window = tk.Toplevel(second_window)
        add_record_window.title("Add Record")
        add_record_window.geometry("1366x768")
        add_record_window.resizable(height=False, width=False)

        def go_back():
            add_record_window.destroy()
            second_window.deiconify()

        app_title_label = tk.Label(add_record_window, text="Library Tracker and Monitoring System Using QR Code", font=("Arial Rounded MT Bold", 30, "bold"))
        app_title_label.place(x=0, y=0, relwidth=0.99, height=100)

        title_label = tk.Label(add_record_window, text="Add Student Record", bg="gray", font=("Arial", 24, "bold"), borderwidth=1, relief="solid")
        title_label.place(x=0, y=102, relwidth=0.99, height=80)

        back_icon = ImageTk.PhotoImage(Image.open("images/back_icon.png"))
        back_button = tk.Button(add_record_window, image=back_icon, command=go_back, bd=0)
        back_button.place(x=10, y=123)

        id_label = tk.Label(add_record_window, text="ID Number:", font=("Arial", 18))
        id_label.place(x=520, y=200)

        id_entry = tk.Entry(add_record_window, width=50, bg="lightgray", font=("Arial", 18))
        id_entry.place(x=670, y=200)

        first_name_label = tk.Label(add_record_window, text="First Name:", font=("Arial", 18))
        first_name_label.place(x=520, y=240)

        first_name_entry = tk.Entry(add_record_window, width=50, bg="lightgray", font=("Arial", 18))
        first_name_entry.place(x=670, y=240)

        middle_name_label = tk.Label(add_record_window, text="Middle Name:", font=("Arial", 18))
        middle_name_label.place(x=520, y=280)

        middle_name_entry = tk.Entry(add_record_window, width=50, bg="lightgray", font=("Arial", 18))
        middle_name_entry.place(x=670, y=280)

        last_name_label = tk.Label(add_record_window, text="Last Name:", font=("Arial", 18))
        last_name_label.place(x=520, y=320)

        last_name_entry = tk.Entry(add_record_window, width=50, bg="lightgray", font=("Arial", 18))
        last_name_entry.place(x=670, y=320)

        sex_label = tk.Label(add_record_window, text="Sex:", font=("Arial", 18))
        sex_label.place(x=520, y=360)

        sex_var = tk.StringVar(add_record_window)
        sex_var.set("Male")

        male_radio = tk.Radiobutton(add_record_window, text="Male", variable=sex_var, value="Male", font=("Arial", 18))
        female_radio = tk.Radiobutton(add_record_window, text="Female", variable=sex_var, value="Female", font=("Arial", 18))

        male_radio.place(x=670, y=360)
        female_radio.place(x=770, y=360)

        course_label = tk.Label(add_record_window, text="Course:", font=("Arial", 18))
        course_label.place(x=520, y=400)

        course_var = tk.StringVar(add_record_window)
        course_var.set("BSA")

        bsa_radio = tk.Radiobutton(add_record_window, text="BSA", variable=course_var, value="BSA", font=("Arial", 18))
        bsed_radio = tk.Radiobutton(add_record_window, text="BSED", variable=course_var, value="BSED", font=("Arial", 18))
        beed_radio = tk.Radiobutton(add_record_window, text="BEED", variable=course_var, value="BEED", font=("Arial", 18))
        bshm_radio = tk.Radiobutton(add_record_window, text="BSHM", variable=course_var, value="BSHM", font=("Arial", 18))
        bsoa_radio = tk.Radiobutton(add_record_window, text="BSOA", variable=course_var, value="BSOA", font=("Arial", 18))
        bsit_radio = tk.Radiobutton(add_record_window, text="BSIT", variable=course_var, value="BSIT", font=("Arial", 18))

        bsa_radio.place(x=670, y=400)
        bsed_radio.place(x=770, y=400)
        beed_radio.place(x=870, y=400)
        bshm_radio.place(x=970, y=400)
        bsoa_radio.place(x=1070, y=400)
        bsit_radio.place(x=1170, y=400)

        status_label = tk.Label(add_record_window, text="Status:", font=("Arial", 18))
        status_label.place(x=520, y=440)

        status_var = tk.StringVar(add_record_window)
        status_var.set("Active")

        active_radio = tk.Radiobutton(add_record_window, text="Active", variable=status_var, value="Active", font=("Arial", 18))
        inactive_radio = tk.Radiobutton(add_record_window, text="Inactive", variable=status_var, value="Inactive", font=("Arial", 18))

        active_radio.place(x=670, y=440)
        inactive_radio.place(x=770, y=440)

        photo_box = Frame(add_record_window, width=220, height=200, bg="white", highlightbackground="black",highlightthickness=2)
        photo_box.place(x=10, y=200)

        qr_photo_box = Frame(add_record_window, width=220, height=200, bg="white", highlightbackground="black",
                          highlightthickness=2)
        qr_photo_box.place(x=260, y=200)

        upload_button = tk.Button(add_record_window, text="Upload Photo", font=("Arial", 18), command=open_file_dialog)
        upload_button.place(x=38, y=406)

        qr_code_button = tk.Button(add_record_window, text="Generate QR", font=("Arial", 18))
        qr_code_button.place(x=290, y=406)

        save_button = tk.Button(add_record_window, text="Save Record",bg="gray",font=("Arial", 18), command=add_record_window_save_to_db)
        save_button.place(x=670, y=490)

        add_record_window.mainloop()

    icon_image = Image.open("images/add_record.png")
    original_width, original_height = icon_image.size
    aspect_ratio = original_width / original_height
    new_width = 100
    new_height = 60
    icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    button_add_record = tk.Button(buttons_frame, image=icon_photo, command=open_add_record_window, height=new_height, width=new_width)
    button_add_record.image = icon_photo
    button_add_record.pack(pady=10)

    def open_list_of_students_window():
        # noinspection PyGlobalUndefined
        global edit_photo
        # noinspection PyGlobalUndefined
        global delete_photo
        # noinspection PyGlobalUndefined
        global search_photo
        second_window.withdraw()

        list_of_students_window = tk.Toplevel(second_window)
        list_of_students_window.title("List Of Students")
        list_of_students_window.geometry("1366x768")
        list_of_students_window.resizable(height=False, width=False)

        def go_back():
            list_of_students_window.destroy()
            second_window.deiconify()

        def edit_student():
            pass

        def update_student():
            pass

        def search_student():
            pass

        app_title_label = tk.Label(list_of_students_window, text="Library Tracker and Monitoring System Using QR Code", font=("Arial Rounded MT Bold", 30, "bold"))
        app_title_label.place(x=0, y=0, relwidth=0.99, height=100)

        title_label = tk.Label(list_of_students_window, text="List Of Students", bg="gray", font=("Arial", 24, "bold"), borderwidth=1, relief="solid")
        title_label.place(x=0, y=102, relwidth=0.99, height=80)

        back_icon = ImageTk.PhotoImage(Image.open("images/back_icon.png"))
        back_button = tk.Button(list_of_students_window, image=back_icon, command=go_back, bd=0)
        back_button.place(x=10, y=123)

        edit_image = Image.open("images/edit_icon.png")
        edit_photo = ImageTk.PhotoImage(edit_image)

        edit_button = tk.Button(list_of_students_window, image=edit_photo, command=edit_student)
        edit_button.place(x=80, y=200)

        update_image = Image.open("images/update_icon.png")
        update_photo = ImageTk.PhotoImage(update_image)

        update_button = tk.Button(list_of_students_window, image=update_photo, command=update_student)
        update_button.place(x=140, y=200)

        search_image = Image.open("images/search_icon.png")
        search_photo = ImageTk.PhotoImage(search_image)

        search_button = tk.Button(list_of_students_window, image=search_photo, command=search_student)
        search_button.place(x=200, y=200)

        search_entry = tk.Entry(list_of_students_window, font=("Arial", 30), width=40, bg="Light Grey")
        search_entry.place(x=280, y=220)

        table_frame = tk.Frame(list_of_students_window)
        table_frame.place(x=0, y=300, width=1600, height=4600)

        table_columns = ("ID Number", "First Name", "Middle Name", "Last Name", "Sex", "Course","Status", "Photo Path")

        table = ttk.Treeview(table_frame, columns=table_columns, show="headings")
        table.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        scrollbar.pack(side="right", fill="y")
        table.configure(yscrollcommand=scrollbar.set)

        for col in table_columns:
            table.heading(col, text=col)
            table.column(col, width=165)

        list_of_students_window.mainloop()

    icon_image = Image.open("images/list_of_student_icon.png")
    original_width, original_height = icon_image.size
    aspect_ratio = original_width / original_height
    new_width = 100
    new_height = 60
    icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    list_of_students = tk.Button(buttons_frame, image=icon_photo, command=open_list_of_students_window, height=new_height, width=new_width)
    list_of_students.image = icon_photo
    list_of_students.pack(pady=10)

    def open_generate_report_window():
        second_window.withdraw()

        generate_report_window = tk.Toplevel(second_window)
        generate_report_window.title("Generate Report")
        generate_report_window.geometry("1366x768")
        generate_report_window.resizable(height=False, width=False)

        def go_back():
            generate_report_window.destroy()
            second_window.deiconify()

        def generate_report():
            selected_courses = course_var.get()

        app_title_label = tk.Label(generate_report_window, text="Library Tracker and Monitoring System Using QR Code", font=("Arial Rounded MT Bold", 30, "bold"))
        app_title_label.place(x=0, y=0, relwidth=0.99, height=100)

        title_label = tk.Label(generate_report_window, text="Generate Report", bg="gray", font=("Arial", 24, "bold"), borderwidth=1, relief="solid")
        title_label.place(x=0, y=102, relwidth=0.99, height=80)

        title_label = tk.Label(generate_report_window, text="Generate Report", bg="gray", font=("Arial", 24, "bold"), borderwidth=1, relief="solid")
        title_label.place(x=0, y=102, relwidth=0.99, height=80)

        semester_label = tk.Label(generate_report_window, text="Select Semester:", font=("Arial", 18))
        semester_label.place(x=0, y=200)  # Adjust the y-coordinate as needed

        semester_var = tk.StringVar(generate_report_window)
        semester_choices = ["Individual Date","1st Semester", "2nd Semester", "Whole School Year"]
        semester_dropdown = tk.OptionMenu(generate_report_window, semester_var, *semester_choices)
        semester_dropdown.config(font=("Arial", 16), width=20)
        semester_dropdown.place(x=180, y=200)

        course_label = tk.Label(generate_report_window, text="Select Courses:", font=("Arial", 18))
        course_label.place(x=470, y=200)

        course_var = tk.StringVar(generate_report_window)
        course_choices = ["Bachelor of Science in Agriculture", "Bachelor of Secondary Education", "Bachelor of Elementary Education", "Bachelor of Science in Hospitaly Management", "Bachelor of Science in Office Administration", "Bachelor of Science in Information Technology", "All Courses"]
        course_dropdown = tk.OptionMenu(generate_report_window, course_var, *course_choices)
        course_dropdown.config(font=("Arial", 16), width=20)
        course_dropdown.place(x=640, y=200)

        graph_button = tk.Button(generate_report_window, bg="orange", text="Graph", font=("Arial", 16),command=generate_report)
        graph_button.place(x=935, y=200)

        print_preview_button = tk.Button(generate_report_window, bg="green", text="Print Preview", font=("Arial", 16), command=generate_report)
        print_preview_button.place(x=1020, y=200)

        print_button = tk.Button(generate_report_window, text="Print", bg="red" ,font=("Arial", 16),command=generate_report)
        print_button.place(x=1170, y=200)

        back_icon = ImageTk.PhotoImage(Image.open("images/back_icon.png"))
        back_button = tk.Button(generate_report_window, image=back_icon, command=go_back, bd=0)
        back_button.place(x=10, y=123)

        generate_report_window.mainloop()

    icon_image = Image.open("images/generate_report_icon.png")
    original_width, original_height = icon_image.size
    aspect_ratio = original_width / original_height
    new_width = 100
    new_height = 60
    icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    button_generate_report = tk.Button(buttons_frame, image=icon_photo, command=open_generate_report_window, height=new_height, width=new_width)
    button_generate_report.image = icon_photo
    button_generate_report.pack(pady=10)

    def open_generate_qr_window():
        second_window.withdraw()

        generate_qr_window = tk.Toplevel(second_window)
        generate_qr_window.title("Generate QR Code")
        generate_qr_window.geometry("1366x768")
        generate_qr_window.resizable(height=False, width=False)

        def go_back():
            generate_qr_window.destroy()
            second_window.deiconify()

        def generate_qr_code():
            qr_data = qr_text_entry.get()

            if qr_data:
                qr = qrcode.QRCode(version=1, box_size=8, border=2)
                qr.add_data(qr_data)
                qr.make(fit=True)
                qr_image = qr.make_image(fill="black", back_color="white")

                # Convert the QR code image to a PhotoImage to display in a Label
                qr_image_tk = ImageTk.PhotoImage(qr_image)

                # Create a Label to display the QR code image inside the qr_box
                qr_label = tk.Label(qr_box, image=qr_image_tk)
                qr_label.image = qr_image_tk  # To prevent the image from being garbage collected
                qr_label.pack()

        app_title_label = tk.Label(generate_qr_window, text="Library Tracker and Monitoring System Using QR Code", font=("Arial Rounded MT Bold", 30, "bold"))
        app_title_label.place(x=0, y=0, relwidth=0.99, height=100)

        title_label = tk.Label(generate_qr_window, text="Generate QR Code", bg="gray", font=("Arial", 24, "bold"), borderwidth=1, relief="solid")
        title_label.place(x=0, y=102, relwidth=0.99, height=80)

        search_label = tk.Label(generate_qr_window, text="Search ID Number:", font=("Arial", 24))
        search_label.place(x=540, y=200)

        qr_text_entry = tk.Entry(generate_qr_window, width=50, bg="lightgray", font=("Arial", 24), justify='center')
        qr_text_entry.place(x=240, y=240)
        qr_text_entry.focus()

        generate_button = tk.Button(generate_qr_window, text="Generate", bg="gray", font=("Arial", 16),
                                    command=generate_qr_code)
        generate_button.place(x=620, y=290)

        # Create the qr_box
        qr_box = tk.Frame(generate_qr_window, width=220, height=200, bg="white", highlightbackground="black",
                          highlightthickness=2)
        qr_box.place(x=370, y=390)

        print_button = tk.Button(generate_qr_window, text="Print", bg="gray", font=("Arial", 16))
        print_button.place(x=640, y=660)

        back_icon = ImageTk.PhotoImage(Image.open("images/back_icon.png"))
        back_button = tk.Button(generate_qr_window, image=back_icon, command=go_back, bd=0)
        back_button.place(x=10, y=123)

        generate_qr_window.mainloop()

    icon_image = Image.open("images/genarate_qr_icon.png")
    original_width, original_height = icon_image.size
    aspect_ratio = original_width / original_height
    new_width = 100
    new_height = 60
    icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    button_generate_qr_code = tk.Button(buttons_frame, image=icon_photo, command=open_generate_qr_window, height=new_height, width=new_width)
    button_generate_qr_code.image = icon_photo
    button_generate_qr_code.pack(pady=10)

    def open_library_utilization_window():
        second_window.withdraw()
        library_utilization_window = tk.Toplevel(second_window)
        library_utilization_window.title("Library Utilization")
        library_utilization_window.geometry("1366x768")
        library_utilization_window.resizable(height=False, width=False)

        def go_back():
            library_utilization_window.destroy()
            second_window.deiconify()

        app_title_label = tk.Label(library_utilization_window, text="Library Tracker and Monitoring System Using QR Code", font=("Arial Rounded MT Bold", 30, "bold"))
        app_title_label.place(x=0, y=0, relwidth=0.99, height=100)

        title_label = tk.Label(library_utilization_window, text="Library Utilization", bg="gray", font=("Arial", 24, "bold"), borderwidth=1, relief="solid")
        title_label.place(x=0, y=102, relwidth=0.99, height=80)

        back_icon = ImageTk.PhotoImage(Image.open("images/back_icon.png"))
        back_button = tk.Button(library_utilization_window, image=back_icon, command=go_back, bd=0)
        back_button.place(x=10, y=123)

        library_utilization_window.mainloop()

    icon_image = Image.open("images/library_utilization_icon.png")
    original_width, original_height = icon_image.size
    aspect_ratio = original_width / original_height
    new_width = 100
    new_height = 60
    icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    open_library_utilization_window = tk.Button(buttons_frame, image=icon_photo, command=open_library_utilization_window, height=new_height, width=new_width)
    open_library_utilization_window.image = icon_photo
    open_library_utilization_window.pack(pady=10)

    def open_change_pin_window():
        second_window.withdraw()

        change_pin_window = tk.Toplevel(second_window)
        change_pin_window.title("Change Pin")
        change_pin_window.geometry("1366x768")
        change_pin_window.resizable(height=False, width=False)

        def go_back():
            change_pin_window.destroy()
            second_window.deiconify()

        def change_pin():
            old_pin = old_pin_entry.get()
            new_pin = new_pin_entry.get()
            if not simulated and validate_pins(old_pin, new_pin):
                # noinspection PyGlobalUndefined

                global current_pin
                current_pin = new_pin
                messagebox.showinfo("Success", "PIN changed successfully!")
                go_back()

        def simulate_button_press(button):
            button.invoke()

        def validate_pins(old_pin, new_pin):
            return True

        def simulate_enter(event=None):
            # noinspection PyGlobalUndefined
            global simulated
            simulated = True

            change_pin()

        app_title_label = tk.Label(change_pin_window, text="Library Tracker and Monitoring System Using QR Code", font=("Arial Rounded MT Bold", 30, "bold"))
        app_title_label.place(x=0, y=0, relwidth=0.99, height=100)

        title_label = tk.Label(change_pin_window, text="Change Pin", bg="gray", font=("Arial", 24, "bold"), borderwidth=1, relief="solid")
        title_label.place(x=0, y=102, relwidth=0.99, height=80)

        back_icon = ImageTk.PhotoImage(Image.open("images/back_icon.png"))
        back_button = tk.Button(change_pin_window, image=back_icon, command=go_back, bd=0)
        back_button.place(x=10, y=123)

        old_pin_label = tk.Label(change_pin_window, text="Old Pin:", font=("Arial", 24))
        old_pin_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        old_pin_entry = tk.Entry(change_pin_window, show="*", font=("Arial", 24), justify='center')
        old_pin_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        old_pin_entry.focus_set()

        new_pin_label = tk.Label(change_pin_window, text="New Pin:", font=("Arial", 24))
        new_pin_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        new_pin_entry = tk.Entry(change_pin_window, show="*", font=("Arial", 24), justify='center')
        new_pin_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        change_pin_window.bind("<Return>", simulate_enter)
        change_pin_window.protocol("WM_DELETE_WINDOW", go_back)

        simulated = False

        change_pin_button = tk.Button(change_pin_window, text="Change Pin", command=change_pin, font=("Arial", 24))
        change_pin_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        current_pin = "1234"

        change_pin_window.mainloop()

    icon_image = Image.open("images/change_pin_icon.png")
    original_width, original_height = icon_image.size
    aspect_ratio = original_width / original_height
    new_width = 100
    new_height = 60
    icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    open_change_pin_window = tk.Button(buttons_frame, image=icon_photo, command=open_change_pin_window, height=new_height, width=new_width)
    open_change_pin_window.image = icon_photo
    open_change_pin_window.pack(pady=10)

    def open_about_us_window():
        second_window.withdraw()
        about_us_window = tk.Toplevel(second_window)
        about_us_window.title("About Us")
        about_us_window.geometry("1366x768")
        about_us_window.resizable(height=False, width=False)

        def go_back():
            about_us_window.destroy()
            second_window.deiconify()

        background_image = Image.open("images/about_us_background.png")  # Change to your image file path
        background_image = background_image.resize((1366, 768), Image.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_image)

        # Create a label to display the background image
        background_label = tk.Label(about_us_window, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        about_us_window.background = background_photo

        back_button = tk.Button(about_us_window, text="Back", command=go_back)
        back_button.place(relx=0, rely=0, anchor=tk.NW)

        about_us_window.mainloop()

    icon_image = Image.open("images/about_us_icon.png")
    original_width, original_height = icon_image.size
    aspect_ratio = original_width / original_height
    new_width = 100
    new_height = 60
    icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    open_about_us_window = tk.Button(buttons_frame, image=icon_photo, command=open_about_us_window, height=new_height,
                                     width=new_width)
    open_about_us_window.image = icon_photo
    open_about_us_window.pack(pady=10)

if __name__ == "__main__":

    def on_entry_click(event):
        if pin_entry.get() == hint_text:
            pin_entry.delete(0, "end")
            pin_entry.config(fg='black')

    def on_focus_out(event):
        if not pin_entry.get():
            pin_entry.insert(0, hint_text)
            pin_entry.config(fg='grey')

    window = tk.Tk()
    window.title("LibTraQ: Library Tracker and Monitoring System using QR Code")
    window.geometry("1366x768")
    window.resizable(height=False, width=False)

    hint_text = "Enter PIN"

    background_image = tk.PhotoImage(file="images/admin_background.png")

    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    pin_label = tk.Label(window, text="Enter PIN:", font=("Arial", 26), justify='center')
    pin_label.pack(pady=(540, 10))

    pin_entry = tk.Entry(window, show="*", font=("Arial", 30), fg='grey', justify='center')
    pin_entry.insert(0, hint_text)
    pin_entry.bind("<FocusIn>", on_entry_click)
    pin_entry.bind("<FocusOut>", on_focus_out)
    pin_entry.pack(pady=10)
    pin_entry.bind("<Return>", verify_pin)
    pin_entry.focus()

    login_button = tk.Button(window, text="Login", font=("Arial", 24), command=verify_pin)
    login_button.pack(pady=0)

    window.mainloop()