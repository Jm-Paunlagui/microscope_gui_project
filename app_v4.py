import time
import tkinter
import tkinter.messagebox
import customtkinter
import cv2
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # @description: Window configuration min size 1280x832 pixels (Macbook Air 13")
        self.title("App title")
        self.geometry(f"{1280}x{832}")

        # @description: Window background color gray
        self.configure(fg_color="#d1d5db")

        # @description: Frames of the app
        self.top_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=50)
        self.top_bar_frame.pack(fill=customtkinter.X, side=customtkinter.TOP)

        self.status_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=50)
        self.status_bar_frame.pack(fill=customtkinter.X, side=customtkinter.BOTTOM)

        self.left_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.left_side_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y)


if __name__ == "__main__":
    app = App()
    app.mainloop()
