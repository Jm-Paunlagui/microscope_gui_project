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
        self.minsize(1280, 832)
        self.maxsize(1280, 832)

        # @description: Window background color gray
        self.configure(fg_color="#d1d5db")

        # @description: configure grid layout (4 rows, 2 columns) with 30% for sidebar and 70% for content camera
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # @description: Sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#d1d5db")
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")

        # @description: Rows Config for sidebar_frame
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # @description: Sidebar OptionMenu
        self.label_options = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_options.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_option_1 = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["Option 1", "Option 2", "Option 3"], command=test_event)
        self.sidebar_option_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_option_2 = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["Option 1", "Option 2", "Option 3"], command=test_event)
        self.sidebar_option_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_option_3 = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["Option 1", "Option 2", "Option 3"], command=test_event)
        self.sidebar_option_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_option_4 = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["Option 1", "Option 2", "Option 3"], command=test_event)
        self.sidebar_option_4.grid(row=4, column=0, padx=20, pady=10)

        # @description: 2 SegmentedButton for appearance mode
        self.label_options_1 = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter",
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_options_1.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_segmented_button_1 = customtkinter.CTkSegmentedButton(self.sidebar_frame,
                                                                           values=["Button 1", "Button 2"],
                                                                           command=test_event)
        self.sidebar_segmented_button_1.grid(row=6, column=0, padx=20, pady=10)
        self.sidebar_segmented_button_1.set("Button 1")

        # @description: SegmentedButton
        self.label_options_2 = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter",
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_options_2.grid(row=8, column=0, padx=20, pady=10)

        # @description: Combobox with values
        self.sidebar_combobox_1 = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["Option 1", "Option 2", "Option 3"], command=test_event)
        self.sidebar_combobox_1.grid(row=9, column=0, padx=20, pady=10)

        # @description: Main Frame for the camera with 4 buttons
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#f8fafc")
        self.main_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

        # @description: Canvas for the camera image
        self.camera_canvas = customtkinter.CTkCanvas(self.main_frame, width=1050, height=730, relief="flat")
        self.camera_canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # @description: Camera VideoCapture

        # @description: 4 Buttons for the camera in the main frame (bottom center and aligned to the bottom)
        self.camera_button_1 = customtkinter.CTkButton(self.main_frame, text="Button 1",
                                                       command=sidebar_button_event)
        self.camera_button_1.grid(row=1, column=0, padx=10, pady=10, sticky="s")
        self.camera_button_2 = customtkinter.CTkButton(self.main_frame, text="Button 2",
                                                       command=sidebar_button_event)
        self.camera_button_2.grid(row=1, column=1, padx=10, pady=10, sticky="s")
        self.camera_button_3 = customtkinter.CTkButton(self.main_frame, text="Button 3",
                                                       command=sidebar_button_event)
        self.camera_button_3.grid(row=1, column=2, padx=10, pady=10, sticky="s")
        self.camera_button_4 = customtkinter.CTkButton(self.main_frame, text="Button 4",
                                                       command=sidebar_button_event)
        self.camera_button_4.grid(row=1, column=3, padx=10, pady=10, sticky="s")


if __name__ == "__main__":
    app = App()
    app.mainloop()
