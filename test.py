def get_data():
    id_number = id_entry.get()
    first_name = first_name_entry.get()
    middle_name = middle_name_entry.get()
    last_name = last_name_entry.get()
    sex = sex_var.get()
    course = course_var.get()
    status = status_var.get()

    data = {
        "ID Number": id_number,
        "First Name": first_name,
        "Middle Name": middle_name,
        "Last Name": last_name,
        "Sex": sex,
        "Course": course,
        "Status": status
    }

    return data


def generate_qr_code():
    data = entry.get()

    data_string = "\n".join([f"{key}: {value}" for key, value in data.items()])

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_tk = ImageTk.PhotoImage(qr_img)

    qr_photo_box.img = qr_img_tk
    qr_photo_box.config(image=qr_img_tk)

    qr_photo_box = tk.Label(add_record_window, width=220, height=200, bg="white", relief="solid")
    qr_photo_box.place(x=260, y=200)

    generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code)
    generate_button.pack()