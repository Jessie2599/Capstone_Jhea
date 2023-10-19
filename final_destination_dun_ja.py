photo_box = tk.Frame(detail_window, width=250, height=250, bg="white", highlightbackground="black", highlightthickness=2)
        photo_box.place(x=75, y=20)

        qr_box = tk.Frame(detail_window, width=200, height=200, bg="white", highlightbackground="black", highlightthickness=2)
        qr_box.place(x=100, y=290)

        cursor.execute("SELECT photo FROM student WHERE id_no = %s", (details[0],))
        photo_data = cursor.fetchone()

        if photo_data:
            # Convert binary photo data to an ImageTk.PhotoImage
            photo = Image.open(io.BytesIO(photo_data[0]))
            photo = photo.resize((250, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(photo)

            # Create a label to display the photo in the photo_box
            photo_label = tk.Label(photo_box, image=photo)
            photo_label.image = photo  # Keep a reference to prevent it from being garbage collected
            photo_label.pack(fill="both", expand=True)

        # Fetch the student's QR code from the database
        cursor.execute("SELECT qr FROM student WHERE id_no = %s", (details[0],))
        qr_data = cursor.fetchone()

        if qr_data:
            # Convert binary QR data to an ImageTk.PhotoImage
            qr_code = Image.open(io.BytesIO(qr_data[0]))
            qr_code = qr_code.resize((200, 200), Image.LANCZOS)
            qr_code = ImageTk.PhotoImage(qr_code)

            # Create a label to display the QR code in the qr_box
            qr_label = tk.Label(qr_box, image=qr_code)
            qr_label.image = qr_code  # Keep a reference to prevent it from being garbage collected
            qr_label.pack(fill="both", expand=True)