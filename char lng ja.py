import tkinter as tk
from PIL import Image, ImageTk

# Create a tkinter window
second_window = tk.Tk()
second_window.geometry("500x500")

# Load the image and resize it
icon_image = Image.open("images/admin_icon.png")
new_width = 120
new_height = 70
icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
icon_photo = ImageTk.PhotoImage(icon_image)

# Create a frame to hold the label
frame = tk.Frame(second_window)
frame.place(x=1210, y=117)  # Position the frame at (x=1210, y=117)

# Create a label to display the image and add it to the frame
image_label = tk.Label(frame, image=icon_photo)
image_label.pack()

# Start the tkinter main loop
second_window.mainloop()
