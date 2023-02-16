import tkinter
import tkinter.messagebox
import customtkinter
import cv2
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def open_input_dialog_event():
    dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
    print("CTkInputDialog:", dialog.get_input())


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)


def test_event(option: str):
    print(option)


def sidebar_button_event():
    print("sidebar_button click")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # @description: configure window by 1100x580 pixels with title "App title"
        self.title("App title")
        self.geometry(f"{1280}x{832}")

        # @description: min and max size of window
        # self.minsize(1280, 832)

        # @description: Window background color gray
        self.configure(fg_color="#d1d5db")

        # @description: Top Bar frame with widgets (hambuger menu, title, settings, ...)
        self.top_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=50)
        self.top_bar_frame.pack(fill=customtkinter.X, side=customtkinter.TOP)

        # @description: Menu icon
        bars = customtkinter.CTkImage(
            light_image=Image.open("assets/icons/bars.png"),
            dark_image=Image.open("assets/icons/bars.png"),
            size=(24, 24)
        )

        # # @description: Left Side Bar frame with widgets (hambuger menu, title...)
        # self.left_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="green")
        # self.left_side_bar_frame.pack(side=customtkinter.LEFT)
        #
        # # @description: Right Side Bar frame with widgets (hambuger menu only)
        # self.right_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="yellow")
        # self.right_side_bar_frame.pack(side=customtkinter.RIGHT)

        # @description: Content frame with widgets (camera, ...)
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.pack(fill=customtkinter.BOTH, expand=customtkinter.YES)

        # @description: Top Bar frame with widgets (hambuger menu, title, settings, ...)
        self.menu_button = customtkinter.CTkButton(self.top_bar_frame, width=18, image=bars, text="",
                                                   fg_color="white", corner_radius=8, hover_color="white",
                                                   text_color="white")
        self.menu_button.pack(side=customtkinter.LEFT, padx=14, pady=14)

        self.status_cam = customtkinter.CTkLabel(self.top_bar_frame, text="Status", fg_color="#bfdbfe",
                                                 font=("Helvetica", 20), corner_radius=8, text_color="#3b82f6")
        self.status_cam.pack(side=customtkinter.RIGHT, padx=14, pady=14)

        self.top_bar_title = customtkinter.CTkLabel(self.top_bar_frame, text="App title",
                                                    font=("Helvetica", 20, "bold"), text_color="black")
        self.top_bar_title.pack(side=customtkinter.LEFT, padx=0, pady=14)

        # @description: Main Frame for the camera with 4 buttons
        # self.main_frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#f8fafc")
        # self.main_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        #
        # # @description: Canvas for the camera image
        self.camera_canvas = customtkinter.CTkCanvas(self.content_frame, width=self.winfo_y(),
                                                     height=self.winfo_x(), relief="flat")
        self.camera_canvas.grid(row=0, column=0, columnspan=4, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
