import locale
import platform
import time
from typing import Union, Callable
from tkinter import messagebox
import customtkinter
import cv2
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"]
all_width = 150


def test_event_status_objective_option(option):
    app.status_objective_option.configure(text=f"Objective: {option}")


def test_event_status_condenser_option(option):
    app.status_condenser_option.configure(text=f"Condenser: {option}")


def test_event_status_reflection_option(option):
    app.status_reflection_option.configure(text=f"Reflection: {option}")


def test_event_status_side_port_option(option):
    app.status_side_port_option.configure(text=f"Side Port: {option}")


def test_event_status_tube_lens_option(option):
    app.status_tube_lens_option.configure(text=f"Tube Lens: {option}")


def test_event_status_shutter_option(option):
    app.status_shutter_option.configure(text=f"Shutter: {option}")


# Initial state of the sidebars
left_side_bar_state = False
right_side_bar_state = False


def toggle_left_sidebar_event():
    """
    :description: Toggle left sidebar, which contains the microscope functions.
    :return:
    """
    global left_side_bar_state
    if left_side_bar_state is True:
        app.left_side_bar_frame.place(x=app.left_side_bar.get(), y=60,
                                      relwidth=app.relwidth_side_bar.get(), relheight=0.89)
        app.update()
        left_side_bar_state = False
    else:
        app.left_side_bar_frame.place(x=0, y=60, relwidth=app.relwidth_side_bar.get(), relheight=0.89)
        app.update()
        app.left_side_bar_frame.lift()
        left_side_bar_state = True


def toggle_right_sidebar_event():
    """
    :description: Toggle right sidebar, which contains the settings functions.
    :return:
    """
    global right_side_bar_state
    if right_side_bar_state is None or right_side_bar_state is True:
        app.right_side_bar_frame.place(x=app.left_side_bar.get(), y=60,
                                       relwidth=0.26, relheight=0.89)
        app.update()
        right_side_bar_state = False
    else:
        app.right_side_bar_frame.place(x=app.right_side_bar.get(), y=60,
                                       relwidth=app.relwidth_side_bar.get(), relheight=0.89)
        app.update()
        app.right_side_bar_frame.lift()
        right_side_bar_state = True


def awb_test_event():
    """
    :description: Change the text of the auto_white_balance button.
    :return:
    """
    if app.auto_white_balance.cget("text") == "OFF":
        app.auto_white_balance.configure(text="Auto")
    else:
        app.auto_white_balance.configure(text="OFF")


def live_capture_test_event():
    """
    :description: Change the text of the live_capture_button button.
    :return:
    """
    if app.live_capture_button.cget("text") == "OFF":
        app.live_capture_button.configure(text="Live")
    else:
        app.live_capture_button.configure(text="OFF")


def capture_test_event():
    """
    :description: Change the text of the capture_snapshot_button button and reset it after 3 seconds.
    :return:
    """
    if app.capture_snapshot_button.cget("text") == "Capture":
        app.capture_snapshot_button.configure(text="Captured")
        app.after(3000, capture_test_event)
    else:
        app.capture_snapshot_button.configure(text="Capture")


def message_box_test_event():
    """
    :description: Show a message box.
    :return: Message box

    Examples of message boxes:
        messagebox.showinfo("showinfo", "Information")

        messagebox.showwarning("showwarning", "Warning")

        messagebox.showerror("showerror", "Error")

        messagebox.askquestion("askquestion", "Are you sure?")

        messagebox.askokcancel("askokcancel", "Want to continue?")

        messagebox.askyesno("askyesno", "Find the value?")

        messagebox.askretrycancel("askretrycancel", "Try again?")
    """
    messagebox.showinfo("Sample", "This is a sample message box.")


def status_setter():
    app.z_drive_config.configure(text=f"{app.coarse_focus_options.get() + app.fine_focus_options.get():,}")
    if app.condenser_diaphragm_options.get() is not None:
        app.status_condenser_diaphragm_value.configure(
            text=f"Condenser Diaphragm: {app.condenser_diaphragm_options.get():,}")
    if app.coarse_focus_options.get() is not None:
        app.status_coarse_focus_value.configure(text=f"Coarse Focus: {app.coarse_focus_options.get():,}")
    if app.fine_focus_options.get() is not None:
        app.status_fine_focus_value.configure(text=f"Fine Focus: {app.fine_focus_options.get():,}")


class Spinbox(customtkinter.CTkFrame):
    """
    :description: A spinbox with float values.

    The spinbox is a combination of a Tkinter Entry and two Tkinter Buttons.
    The Entry is used to display the current value, and the Buttons are used to increase or decrease the value.

    To get the current value, use the get() method. To set the current value, use the set() method.

    The spinbox can be configured with the following parameters:
        width: The width of the spinbox in pixels.
        height: The height of the spinbox in pixels.
        step_size: The step size, which is used to increase or decrease the value.
        min_value: The minimum value, which can be set.
        max_value: The maximum value, which can be set.
        command: A function, which is called, when the value is changed.

    Example:
        spinbox = FloatSpinbox(root, width=100, height=30, step_size=0.1, min_value=0, max_value=10, command=print)
        spinbox.pack()

        print(spinbox.get())  # prints the current value
        spinbox.set(5)  # sets the current value to 5
    """

    def __init__(self, *args,
                 width: int = 150,
                 height: int = 30,
                 step_size: int = 1,
                 min_value: int = None,
                 max_value: int = None,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.min_value = min_value
        self.max_value = max_value
        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"), corner_radius=8)  # set frame color

        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height - 6, height=height - 6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0")

    def add_button_callback(self):
        """
        :description: Increase the value by the step size.

        If the value is greater than the maximum value, the value is set to the maximum value.
        :return:
        """
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get().replace(',', '')) + self.step_size
            if self.max_value is not None and value > self.max_value:
                value = self.max_value
            value_str = f"{value:,}"
            self.entry.delete(0, "end")
            self.entry.insert(0, value_str)
            status_setter()
        except ValueError:
            return

    def subtract_button_callback(self):
        """
        :description: Decrease the value by the step size.
        If the value is less than the minimum value, the value is set to the minimum value.

        :return: The current value as a float or None, if the value is not a float.
        """
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get().replace(',', '')) - self.step_size
            if self.min_value is not None and value < self.min_value:
                value = self.min_value
            value_str = f"{value:,}"
            self.entry.delete(0, "end")
            self.entry.insert(0, value_str)
            status_setter()
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        """
        :description: Get the current value.
        If the value is not a float, None is returned.

        :return: The current value.
        """
        try:
            return int(self.entry.get().replace(',', ''))
        except ValueError:
            return None

    def set(self, value: int):
        """
        :description: Set a new value with commas.
        :param value:
        :return:
        """
        value = f"{value:,}"
        self.entry.delete(0, "end")
        self.entry.insert(0, value)


class App(customtkinter.CTk):
    """
    :description: Main application class for the application window and all widgets inside.

    :param customtkinter.CTk: The base class for the application window.
    :type customtkinter.CTk: customtkinter.CTk
    """

    def __init__(self):
        """
        :description: Initialize the application window and all widgets inside the window.
        __init__ is called when the class is instantiated and is the first method to be called.
        super().__init__() calls the __init__ method of the parent class (customtkinter.CTk).
        """
        super().__init__()

        # @description: Auto detect the screen resolution
        self.title("App title")

        if platform.system() == "Windows":
            self.iconbitmap("assets/icons/sample_icon.ico")
        else:
            image = Image.open("assets/icons/sample_icon.png")
            photo = ImageTk.PhotoImage(image)
            self.iconphoto(True, photo)

        # x = (self.winfo_screenwidth() / 2) - (self.winfo_screenwidth() / 2)
        # y = (self.winfo_screenheight() / 2) - (self.winfo_screenheight() / 2)
        # self.attributes("-fullscreen", True)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight() - 80}+0+0")
        self.configure(fg_color="#d1d5db")

        self.minsize(self.winfo_screenwidth(), self.winfo_screenheight() - 80)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight() - 80)

        self.left_side_bar = customtkinter.IntVar()
        self.right_side_bar = customtkinter.IntVar()
        self.relwidth_side_bar = customtkinter.DoubleVar()

        match self.winfo_screenwidth():
            case 1280:
                self.left_side_bar.set(-500)
                self.right_side_bar.set(880)
                self.relwidth_side_bar.set(0.34)
            case 1366:
                self.left_side_bar.set(-500)
                self.right_side_bar.set(975)
                self.relwidth_side_bar.set(0.32)
            case 1440:
                self.left_side_bar.set(-500)
                self.right_side_bar.set(1000)
                self.relwidth_side_bar.set(0.32)
            case 1512:
                self.left_side_bar.set(-520)
                self.right_side_bar.set(1100)
                self.relwidth_side_bar.set(0.30)
            case 1600:
                self.left_side_bar.set(-520)
                self.right_side_bar.set(1200)
                self.relwidth_side_bar.set(0.28)
            case 1680:
                self.left_side_bar.set(-520)
                self.right_side_bar.set(1290)
                self.relwidth_side_bar.set(0.26)
            case 1728:
                self.left_side_bar.set(-520)
                self.right_side_bar.set(1325)
                self.relwidth_side_bar.set(0.28)
            case 1920:
                self.left_side_bar.set(-520)
                self.right_side_bar.set(1520)
                self.relwidth_side_bar.set(0.23)

        # @description: Menu icon
        bars = customtkinter.CTkImage(
            light_image=Image.open("assets/icons/bars.png"),
            size=(24, 24)
        )

        gear = customtkinter.CTkImage(
            light_image=Image.open("assets/icons/gear-solid.png"),
            size=(24, 24)
        )

        # @description: Top bar frame starts here
        self.top_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=54)
        self.top_bar_frame.pack(fill=customtkinter.X, side=customtkinter.TOP)
        self.menu_button = customtkinter.CTkButton(self.top_bar_frame, width=24, height=24, image=bars, text="",
                                                   fg_color="white", corner_radius=8, hover_color="white",
                                                   text_color="white", command=toggle_left_sidebar_event)
        self.menu_button.pack(side=customtkinter.LEFT, padx=8, pady=14)
        self.settings_button = customtkinter.CTkButton(self.top_bar_frame, width=24, height=24, image=gear, text="",
                                                       fg_color="white", corner_radius=8, hover_color="white",
                                                       text_color="white", command=toggle_right_sidebar_event)
        self.settings_button.pack(side=customtkinter.RIGHT, padx=8, pady=14)
        self.top_bar_title = customtkinter.CTkLabel(
            self.top_bar_frame, text="App title", font=("Helvetica", 20, "bold"), text_color="black",
            anchor=customtkinter.SW)
        self.top_bar_title.pack(side=customtkinter.LEFT, padx=0, pady=14)
        # @description: Top bar frame ends here

        # @description: Left sidebar frame starts here
        self.left_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.left_side_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y)
        self.left_side_bar_frame.place(x=-500, y=60, relwidth=0.34, relheight=0.89)
        self.left_side_bar_frame.grid_rowconfigure(15, weight=1)

        self.microscope_functions_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Microscope Functions",
                                                                 font=customtkinter.CTkFont("Helvetica", 20, "bold"))
        self.microscope_functions_label.grid(row=0, column=0, sticky=customtkinter.W, padx=14, pady=14)
        self.objective_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Objective",
                                                      font=customtkinter.CTkFont(size=20))
        self.objective_label.grid(row=1, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.condenser_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Condenser",
                                                      font=customtkinter.CTkFont(size=20))
        self.condenser_label.grid(row=2, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.reflector_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Reflector",
                                                      font=customtkinter.CTkFont(size=20))
        self.reflector_label.grid(row=3, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.side_port_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Side Port",
                                                      font=customtkinter.CTkFont(size=20))
        self.side_port_label.grid(row=4, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.tube_lens_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Tube Lens",
                                                      font=customtkinter.CTkFont(size=20))
        self.tube_lens_label.grid(row=5, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.shutter_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Shutter",
                                                    font=customtkinter.CTkFont(size=20))
        self.shutter_label.grid(row=6, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.condenser_diaphragm_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Condenser Diaphragm",
                                                                font=customtkinter.CTkFont(size=20))
        self.condenser_diaphragm_label.grid(row=7, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.z_drive_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Z Drive",
                                                    font=customtkinter.CTkFont(size=20))
        self.z_drive_label.grid(row=8, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.coarse_focus_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Coarse Focus",
                                                         font=customtkinter.CTkFont(size=20))
        self.coarse_focus_label.grid(row=9, column=0, padx=20, pady=0)
        self.fine_focus_label = customtkinter.CTkLabel(self.left_side_bar_frame, text="Fine Focus",
                                                       font=customtkinter.CTkFont(size=20))
        self.fine_focus_label.grid(row=10, column=0, padx=20, pady=0)

        objective_options_lists = [
            "Option 1.1", "Option 2.1", "Option 3.1", "Option 4.1", "Option 5.1", "Option 6.1"
        ]

        condenser_options_lists = [
            "Option 1.2", "Option 2.2", "Option 3.2", "Option 4.2", "Option 5.2", "Option 6.2"
        ]

        reflector_options_lists = [
            "Option 1.3", "Option 2.3", "Option 3.3", "Option 4.3", "Option 5.3"
        ]

        side_port_options_lists = [
            "Option 1.4", "Option 2.4", "Option 3.4"
        ]

        tube_lens_options_lists = [
            "Option 1.5", "Option 2.5", "Option 3.5"
        ]

        self.objective_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=objective_options_lists, command=test_event_status_objective_option,
            width=all_width, corner_radius=8)
        self.objective_options.grid(row=1, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.condenser_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=condenser_options_lists, command=test_event_status_condenser_option,
            width=all_width, corner_radius=8)
        self.condenser_options.grid(row=2, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.reflector_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=reflector_options_lists, command=test_event_status_reflection_option,
            width=all_width, corner_radius=8)
        self.reflector_options.grid(row=3, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.side_port = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=side_port_options_lists, command=test_event_status_side_port_option,
            width=all_width, corner_radius=8)
        self.side_port.grid(row=4, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.tube_lens_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=tube_lens_options_lists, command=test_event_status_tube_lens_option,
            width=all_width, corner_radius=8)
        self.tube_lens_options.grid(row=5, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.shutter_options = customtkinter.CTkSegmentedButton(
            self.left_side_bar_frame, values=["S-Button 1", "S-Button 2"], command=test_event_status_shutter_option,
            width=all_width, corner_radius=8)
        # default value for segmented button
        self.shutter_options.set("S-Button 2")
        self.shutter_options.grid(row=6, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.condenser_diaphragm_options = Spinbox(self.left_side_bar_frame, width=150, step_size=1, min_value=0,
                                                   max_value=1400)
        self.condenser_diaphragm_options.grid(row=7, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.condenser_diaphragm_options.set(700)
        self.coarse_focus_options = Spinbox(self.left_side_bar_frame, width=150, step_size=100, min_value=0,
                                            max_value=40000)
        self.coarse_focus_options.grid(row=9, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.coarse_focus_options.set(20000)
        self.fine_focus_options = Spinbox(self.left_side_bar_frame, width=150, step_size=1, min_value=0,
                                          max_value=99)
        self.fine_focus_options.grid(row=10, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.fine_focus_options.set(50)
        self.z_drive_config = customtkinter.CTkLabel(
            self.left_side_bar_frame, text=f"{self.coarse_focus_options.get() + self.fine_focus_options.get():,}",
            fg_color="#bfdbfe", font=("Helvetica", 20), corner_radius=8, width=150, anchor=customtkinter.SW,
            text_color="#3b82f6")
        self.z_drive_config.grid(row=8, column=1, padx=20, pady=10, sticky=customtkinter.W)
        # @description: Left sidebar frame ends here

        # @description: Right sidebar frame starts here
        self.right_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.right_side_bar_frame.place(x=1112, y=60, relwidth=0.34, relheight=0.89)
        self.right_side_bar_frame.grid_rowconfigure(15, weight=1)

        self.right_side_bar_frame.pack_forget()
        self.camera_settings_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Camera Settings",
                                                            font=customtkinter.CTkFont("Helvetica", 20, "bold"))
        self.camera_settings_label.grid(row=0, column=0, sticky=customtkinter.W, padx=14, pady=14)
        self.auto_white_balance_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Auto White Balance",
                                                               font=customtkinter.CTkFont(size=20))
        self.auto_white_balance_label.grid(row=1, column=0, sticky=customtkinter.W, padx=14, pady=14)
        self.sharpness_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Sharpness",
                                                      font=customtkinter.CTkFont(size=20))
        self.sharpness_label.grid(row=2, column=0, sticky=customtkinter.W, padx=14, pady=14)
        self.contrast_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Contrast",
                                                     font=customtkinter.CTkFont(size=20))
        self.contrast_label.grid(row=3, column=0, sticky=customtkinter.W, padx=14, pady=14)
        self.brightness_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Brightness",
                                                       font=customtkinter.CTkFont(size=20))
        self.brightness_label.grid(row=4, column=0, sticky=customtkinter.W, padx=14, pady=14)

        self.auto_white_balance = customtkinter.CTkButton(self.right_side_bar_frame, text="Auto",
                                                          font=("Helvetica", 14), corner_radius=8,
                                                          command=awb_test_event, width=all_width)
        self.auto_white_balance.grid(row=1, column=1, sticky=customtkinter.W, padx=14, pady=14)
        self.sharpness_level = Spinbox(self.right_side_bar_frame, step_size=1, min_value=0, max_value=9)
        self.sharpness_level.grid(row=2, column=1, sticky=customtkinter.W, padx=14, pady=14)
        self.contrast_level = Spinbox(self.right_side_bar_frame, step_size=1, min_value=0, max_value=100)
        self.contrast_level.grid(row=3, column=1, sticky=customtkinter.W, padx=14, pady=14)
        self.brightness_level = Spinbox(self.right_side_bar_frame, step_size=1, min_value=0, max_value=100)
        self.brightness_level.grid(row=4, column=1, sticky=customtkinter.W, padx=14, pady=14)
        self.camera_functions_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Camera Functions",
                                                             font=customtkinter.CTkFont("Helvetica", 20, "bold"))
        self.camera_functions_label.grid(row=5, column=0, sticky=customtkinter.W, padx=14, pady=14)
        self.live_capture_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Live Capture",
                                                         font=customtkinter.CTkFont(size=20))
        self.live_capture_label.grid(row=6, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.capture_snapshot_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Capture Snapshot",
                                                             font=customtkinter.CTkFont(size=20))
        self.capture_snapshot_label.grid(row=7, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.button_3_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Button 3",
                                                     font=customtkinter.CTkFont(size=20))
        self.button_3_label.grid(row=8, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.button_4_label = customtkinter.CTkLabel(self.right_side_bar_frame, text="Button 4",
                                                     font=customtkinter.CTkFont(size=20))
        self.button_4_label.grid(row=9, column=0, padx=20, pady=0, sticky=customtkinter.W)
        self.live_capture_button = customtkinter.CTkButton(self.right_side_bar_frame, text="OFF", fg_color="#3b82f6",
                                                           corner_radius=8, text_color="white", font=("Helvetica", 14),
                                                           command=live_capture_test_event, width=all_width)
        self.live_capture_button.grid(row=6, column=1, padx=20, pady=14, sticky=customtkinter.W)
        self.capture_snapshot_button = customtkinter.CTkButton(self.right_side_bar_frame, text="Capture",
                                                               fg_color="#3b82f6", corner_radius=8, text_color="white",
                                                               font=("Helvetica", 14), command=capture_test_event,
                                                               width=all_width)
        self.capture_snapshot_button.grid(row=7, column=1, padx=20, pady=14, sticky=customtkinter.W)
        self.button_3 = customtkinter.CTkButton(self.right_side_bar_frame, text="Button 3", fg_color="#3b82f6",
                                                corner_radius=8, hover_color=None, text_color="white",
                                                font=("Helvetica", 14), command=message_box_test_event, width=all_width)
        self.button_3.grid(row=8, column=1, padx=20, pady=14, sticky=customtkinter.W)
        self.button_4 = customtkinter.CTkButton(self.right_side_bar_frame, text="Button 4", fg_color="#3b82f6",
                                                corner_radius=8, hover_color=None,
                                                text_color="white", font=("Helvetica", 14),
                                                command=message_box_test_event, width=all_width)
        self.button_4.grid(row=9, column=1, padx=20, pady=14, sticky=customtkinter.W)

        # @description: Right sidebar frame ends here

        # @description: Status bar frame starts here
        self.status_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=54)
        self.status_bar_frame.pack(fill=customtkinter.X, side=customtkinter.BOTTOM)

        self.status_objective_option = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Objective: {self.objective_options.get()}", font=("Helvetica", 14),
            corner_radius=8)
        self.status_objective_option.pack(side=customtkinter.LEFT, padx=2, pady=8)
        self.status_condenser_option = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Condenser: {self.condenser_options.get()}", font=("Helvetica", 14),
            corner_radius=8)
        self.status_condenser_option.pack(side=customtkinter.LEFT, padx=2, pady=8)
        self.status_reflection_option = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Reflection: {self.reflector_options.get()}", font=("Helvetica", 14),
            corner_radius=8)
        self.status_reflection_option.pack(side=customtkinter.LEFT, padx=2, pady=8)
        self.status_side_port_option = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Side Port: {self.side_port.get()}", font=("Helvetica", 14),
            corner_radius=8)
        self.status_side_port_option.pack(side=customtkinter.LEFT, padx=2, pady=8)
        self.status_tube_lens_option = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Tube Lens: {self.tube_lens_options.get()}", font=("Helvetica", 14),
            corner_radius=8)
        self.status_tube_lens_option.pack(side=customtkinter.LEFT, padx=2, pady=8)
        self.status_shutter_option = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Shutter: {self.shutter_options.get()}", font=("Helvetica", 14),
            corner_radius=8)
        self.status_shutter_option.pack(side=customtkinter.LEFT, padx=2, pady=8)
        self.status_condenser_diaphragm_value = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Condenser Diaphragm: {self.condenser_diaphragm_options.get():,}",
            font=("Helvetica", 14), corner_radius=8)
        self.status_condenser_diaphragm_value.pack(side=customtkinter.LEFT, padx=2, pady=8)
        self.status_coarse_focus_value = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Coarse Focus: {self.coarse_focus_options.get():,}",
            font=("Helvetica", 14), corner_radius=8)
        self.status_coarse_focus_value.pack(side=customtkinter.LEFT, padx=2, pady=8)
        self.status_fine_focus_value = customtkinter.CTkLabel(
            self.status_bar_frame, text=f"Fine Focus: {self.fine_focus_options.get():,}", font=("Helvetica", 14),
            corner_radius=8)
        self.status_fine_focus_value.pack(side=customtkinter.LEFT, padx=2, pady=8)
        # @description: Status bar frame ends here

        # @description: Main frame starts here
        self.content_frame = customtkinter.CTkFrame(self, )
        self.content_frame.pack(fill=customtkinter.BOTH, expand=customtkinter.YES, side=customtkinter.TOP)

        self.camera_canvas = customtkinter.CTkCanvas(self.content_frame, width=self.content_frame.winfo_width(),
                                                     height=self.content_frame.winfo_height())
        self.camera_canvas.pack(fill="both", expand=True)

        # @description: Camera VideoCapture
        # VideoCapture here:
        self.cap = cv2.VideoCapture(0)

        def inactive_camera():
            self.cap.release()
            self.camera_canvas.destroy()
            self.camera_canvas = customtkinter.CTkCanvas(self.content_frame, width=self.content_frame.winfo_width(),
                                                         height=self.content_frame.winfo_height(), closeenough=1)
            self.camera_canvas.pack(fill="both", expand=True)
            self.inactive_camera_label = customtkinter.CTkLabel(self.camera_canvas, text="Camera not in use",
                                                                font=customtkinter.CTkFont(size=20, weight="bold"))
            self.inactive_camera_label.place(relx=0.5, rely=0.5, anchor="center")

        # @description: Update the image
        inactive_camera()


if __name__ == "__main__":
    app = App()
    app.bind("<Escape>", lambda e: app.left_side_bar_frame.place(x=app.left_side_bar.get(), y=60,
                                                                 relwidth=app.relwidth_side_bar.get(),
                                                                 relheight=0.89) or
                                   app.right_side_bar_frame.place(x=app.left_side_bar.get(), y=60,
                                                                  relwidth=app.relwidth_side_bar.get(),
                                                                  relheight=0.89))
    app.bind("<Control-l>", lambda e: app.left_side_bar_frame.place(x=0, y=60,
                                                                    relwidth=app.relwidth_side_bar.get(),
                                                                    relheight=0.89))
    app.bind("<Control-r>", lambda e: app.right_side_bar_frame.place(x=app.right_side_bar.get(), y=60,
                                                                     relwidth=app.relwidth_side_bar.get(),
                                                                     relheight=0.89))
    app.mainloop()
