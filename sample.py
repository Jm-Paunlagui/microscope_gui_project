import time
from typing import Union, Callable
from tkinter import messagebox
import customtkinter
import cv2
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"]


def clear_textbox_event():
    """
    :description: Clear the text box.
    :return:
    """
    app.text_box.delete(0.0, customtkinter.END)


def clear_combined_event():
    """
    :description: Clear the text box.
    :return:
    """
    app.combined_text.delete(0.0, customtkinter.END)


def clear_last_inserted_event():
    """
    :description: Clear the last inserted text.
    :return:
    """
    # Check if the text box is empty
    if app.combined_text.get("1.0", "end-1c") == "":
        messagebox.showwarning("Warning", "The text box is empty.")
    else:
        # Get the last inserted text
        last_inserted_text = app.combined_text.get("end-2c", "end-1c")
        # Get the index of the last whitespace character before the last inserted text
        last_whitespace_index = app.combined_text.search(r'\s\S*', "end-1c", backwards=True, regexp=True)
        if last_whitespace_index:
            # Delete the last word (i.e., text between last whitespace and end of text)
            app.combined_text.delete(last_whitespace_index, "end")
        else:
            # If no whitespace found, delete the last character
            app.combined_text.delete("end-1c")


def put_text_in_textbox_event():
    """
    :description: Puts the text in the combined_text textbox in the text box.
    :return:
    """
    # Check if the text box is empty
    if app.text_box.get("1.0", "end-1c") == "":
        messagebox.showwarning("Warning", "The text box is empty.")
    else:
        # Put the text in the combined_text textbox in the text box
        app.combined_text.insert(customtkinter.END, app.text_box.get("1.0", "end-1c") + " ")


class App(customtkinter.CTk):
    """
    :description: Main application class for the application window and all widgets inside.

    :param customtkinter.CTk: The base class for the application window.
    :type customtkinter.CTk: customtkinter.CTk
    """

    def __init__(self):
        """
        :description: Initialize the application window and all widgets inside the window.
        init is called when the class is instantiated and is the first method to be called.
        super().init() calls the init method of the parent class (customtkinter.CTk).
        """
        super().__init__()

        # @description: Auto detect the screen resolution
        self.title("App title")
        self.geometry(f"{1280}x{832}")
        self.configure(fg_color="#d1d5db")

        # @description: Left side bar starts here
        self.left_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.left_side_bar_frame.pack(side=customtkinter.BOTTOM, fill=customtkinter.Y)
        self.left_side_bar_frame.grid_rowconfigure(15, weight=1)

        self.text_box = customtkinter.CTkTextbox(self.left_side_bar_frame, corner_radius=0, fg_color="white",
                                                 font=("Helvetica", 20, "bold"),
                                                 width=640
                                                 )
        self.text_box.grid(row=0, column=0, sticky=customtkinter.NSEW)
        self.combined_text = customtkinter.CTkTextbox(self.left_side_bar_frame, corner_radius=0, fg_color="white",
                                                      font=("Helvetica", 20, "bold"),
                                                      width=640
                                                      )
        self.combined_text.grid(row=0, column=1, sticky=customtkinter.NSEW)
        self.text_box.insert(customtkinter.END, "Hello World")

        self.clear_button = customtkinter.CTkButton(self.left_side_bar_frame, text="Clear", corner_radius=4,
                                                    text_color="white", command=clear_textbox_event)
        self.clear_button.grid(row=1, column=0, sticky=customtkinter.NSEW, pady=10, padx=10)

        self.enter_button = customtkinter.CTkButton(self.left_side_bar_frame, text="Enter", corner_radius=4,
                                                    text_color="white", command=put_text_in_textbox_event)
        self.enter_button.grid(row=1, column=1, sticky=customtkinter.NSEW, pady=10, padx=10)
        self.clear_last_inserted_button = customtkinter.CTkButton(self.left_side_bar_frame, text="Clear last inserted",
                                                                  corner_radius=4,
                                                                  text_color="white", command=clear_last_inserted_event)
        self.clear_last_inserted_button.grid(row=2, column=0, sticky=customtkinter.NSEW, pady=10, padx=10)
        self.clear_combined_text_button = customtkinter.CTkButton(self.left_side_bar_frame, text="Clear combined text",
                                                                  corner_radius=4,
                                                                  text_color="white", command=clear_combined_event)
        self.clear_combined_text_button.grid(row=2, column=1, sticky=customtkinter.NSEW, pady=10, padx=10)

        # @description: Left side bar ends here

        # @description: Main frame starts here
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="black")
        self.main_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.camera_canvas = customtkinter.CTkCanvas(self.main_frame, width=self.main_frame.winfo_width(),
                                                     height=self.main_frame.winfo_height())
        self.camera_canvas.pack(fill="both", expand=True)

        self.cap = cv2.VideoCapture(0)

        def update_image():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                width = self.camera_canvas.winfo_width()
                height = self.camera_canvas.winfo_height()
                if width > 1 and height > 1:
                    frame = cv2.resize(frame, (width, height))
                    frame = cv2.flip(frame, 1)
                    frame = Image.fromarray(frame)
                    frame = ImageTk.PhotoImage(frame)
                    self.camera_canvas.create_image(0, 0, image=frame, anchor="nw")
                    self.camera_canvas.image = frame
            else:
                inactive_camera()
            self.camera_canvas.after(1, update_image)

        def inactive_camera():
            self.cap.release()
            self.camera_canvas.destroy()
            self.camera_canvas = customtkinter.CTkCanvas(self.main_frame, width=self.main_frame.winfo_width(),
                                                         height=self.main_frame.winfo_height(), closeenough=1)
            self.camera_canvas.pack(fill="both", expand=True)
            self.inactive_camera_label = customtkinter.CTkLabel(self.camera_canvas, text="Camera not in use",
                                                                font=customtkinter.CTkFont(size=20, weight="bold"))
            self.inactive_camera_label.place(relx=0.5, rely=0.5, anchor="center")

        # @description: Update the image
        # update_image()
        # inactive_camera()

        # @description: Main frame ends here


if __name__ == "__main__":
    app = App()
    app.mainloop()
