import time
from typing import Union, Callable
import customtkinter
import cv2
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"]


def test_event(option):
    """
    :description: Only the last option will be displayed in the status bar.

    To be more specific, you can statically define, which status text should be displayed for each option.
    For example:
        def objective_event(option):
            app.status_cam.configure(text="Objective: " + option + " selected")
    :param option:
    :return:
    """
    app.status_cam.configure(text=option + " selected")


def toggle_left_sidebar_event():
    """
    :description: Toggle left sidebar, which contains the microscope functions.
    :return:
    """
    if app.left_side_bar_frame.winfo_ismapped():
        # @description: Animation for sidebar
        app.left_side_bar_frame.grid_rowconfigure(15, weight=0)
        time.sleep(0.01)
        app.update()
        app.left_side_bar_frame.pack_forget()
    else:
        app.left_side_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y)
        app.left_side_bar_frame.grid_rowconfigure(15, weight=1)
        time.sleep(0.01)
        app.update()
        app.left_side_bar_frame.lift()


def toggle_right_sidebar_event():
    """
    :description: Toggle right sidebar, which contains the camera settings and functions.
    :return:
    """
    if app.right_side_bar_frame.winfo_ismapped():
        # @description: Animation for sidebar
        app.right_side_bar_frame.grid_rowconfigure(15, weight=0)
        time.sleep(0.01)
        app.update()
        app.right_side_bar_frame.pack_forget()
    else:
        app.right_side_bar_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.Y)
        app.right_side_bar_frame.grid_rowconfigure(15, weight=1)
        time.sleep(0.01)
        app.update()
        app.right_side_bar_frame.lift()


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


class FloatSpinbox(customtkinter.CTkFrame):
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
                 width: Union[int, float] = 100,
                 height: Union[int, float] = 30,
                 step_size: Union[int, float] = 1,
                 min_value: Union[int, float] = None,
                 max_value: Union[int, float] = None,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.min_value = min_value
        self.max_value = max_value
        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

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
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        """
        :description: Increase the value by the step size.

        If the value is greater than the maximum value, the value is set to the maximum value.
        :return:
        """
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            if value > self.max_value:
                value = self.max_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value if value >= 0 else 0)
            app.z_drive_config.configure(text=f"{app.coarse_focus_options.get() + app.fine_focus_options.get()}")
            if app.condenser_diaphragm_options.get() is not None:
                app.status_cam.configure(
                    text=f"Condenser : {app.condenser_diaphragm_options.get()}")
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
            value = float(self.entry.get()) - self.step_size
            if value < self.min_value:
                value = self.min_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value if value <= self.max_value else self.max_value)
            app.z_drive_config.configure(text=f"{app.coarse_focus_options.get() + app.fine_focus_options.get()}")
            if app.condenser_diaphragm_options.get() is not None:
                app.status_cam.configure(
                    text=f"Condenser : {app.condenser_diaphragm_options.get()}")
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        """
        :description: Get the current value.
        If the value is not a float, None is returned.

        :return: The current value.
        """
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        """
        :description: Set a new value.
        :param value:
        :return:
        """
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))


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

        # @description: configure window by 1100x580 pixels with title "App title"
        self.title("App title")
        self.geometry(f"{1280}x{832}")
        self.configure(fg_color="#d1d5db")

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
        self.top_bar_title = customtkinter.CTkLabel(self.top_bar_frame, text="App title",
                                                    font=("Helvetica", 20, "bold"), text_color="black")
        self.top_bar_title.pack(side=customtkinter.LEFT, padx=0, pady=14)
        # @description: Top bar frame ends here

        # @description: Left sidebar frame starts here
        self.left_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.left_side_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y)
        self.left_side_bar_frame.grid_rowconfigure(15, weight=1)
        self.left_side_bar_frame.pack_forget()

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
            "Option 1.1", "Option 2.1", "Option 3.1", "Option 4.1", "Option 5.1", "Option 6.1",
        ]

        condenser_options_lists = [
            "Option 1.2", "Option 2.2", "Option 3.2", "Option 4.2", "Option 5.2", "Option 6.2",
        ]

        reflector_options_lists = [
            "Option 1.3", "Option 2.3", "Option 3.3", "Option 4.3", "Option 5.3",
        ]

        side_port_options_lists = [
            "Option 1.4", "Option 2.4", "Option 3.4"
        ]

        tube_lens_options_lists = [
            "Option 1.5", "Option 2.5", "Option 3.5"
        ]

        self.objective_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=objective_options_lists, command=test_event)
        self.objective_options.grid(row=1, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.condenser_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=condenser_options_lists, command=test_event)
        self.condenser_options.grid(row=2, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.reflector_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=reflector_options_lists, command=test_event)
        self.reflector_options.grid(row=3, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.side_port = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=side_port_options_lists, command=test_event)
        self.side_port.grid(row=4, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.tube_lens_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=tube_lens_options_lists, command=test_event)
        self.tube_lens_options.grid(row=5, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.shutter_options = customtkinter.CTkSegmentedButton(self.left_side_bar_frame,
                                                                values=["S-Button 1", "S-Button 2"],
                                                                command=test_event)
        self.shutter_options.grid(row=6, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.condenser_diaphragm_options = FloatSpinbox(self.left_side_bar_frame, width=150, step_size=1, min_value=0.0,
                                                        max_value=1400.0)
        self.condenser_diaphragm_options.grid(row=7, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.condenser_diaphragm_options.set(700.0)
        self.coarse_focus_options = FloatSpinbox(self.left_side_bar_frame, width=150, step_size=100, min_value=0.0,
                                                 max_value=40000.0)
        self.coarse_focus_options.grid(row=9, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.coarse_focus_options.set(20000.0)
        self.fine_focus_options = FloatSpinbox(self.left_side_bar_frame, width=150, step_size=1, min_value=0.0,
                                               max_value=99)
        self.fine_focus_options.grid(row=10, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.fine_focus_options.set(50.0)
        self.z_drive_config = customtkinter.CTkLabel(
            self.left_side_bar_frame, text=f"{self.coarse_focus_options.get() + self.fine_focus_options.get()}",
            fg_color="#bfdbfe", font=("Helvetica", 20), corner_radius=8,
            text_color="#3b82f6", )
        self.z_drive_config.grid(row=8, column=1, padx=20, pady=10, sticky=customtkinter.W)
        # @description: Left sidebar frame ends here

        # @description: Right sidebar frame starts here
        self.right_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.right_side_bar_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.Y)
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
                                                          command=awb_test_event)
        self.auto_white_balance.grid(row=1, column=1, sticky=customtkinter.W, padx=14, pady=14)
        self.sharpness_level = FloatSpinbox(self.right_side_bar_frame, step_size=1, min_value=0.0, max_value=9.0)
        self.sharpness_level.grid(row=2, column=1, sticky=customtkinter.W, padx=14, pady=14)
        self.contrast_level = FloatSpinbox(self.right_side_bar_frame, step_size=1, min_value=0.0, max_value=100.0)
        self.contrast_level.grid(row=3, column=1, sticky=customtkinter.W, padx=14, pady=14)
        self.brightness_level = FloatSpinbox(self.right_side_bar_frame, step_size=1, min_value=0.0, max_value=100.0)
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
                                                           command=live_capture_test_event)
        self.live_capture_button.grid(row=6, column=1, padx=20, pady=14, sticky=customtkinter.W)
        self.capture_snapshot_button = customtkinter.CTkButton(self.right_side_bar_frame, text="Capture",
                                                               fg_color="#3b82f6", corner_radius=8, text_color="white",
                                                               font=("Helvetica", 14), command=capture_test_event)
        self.capture_snapshot_button.grid(row=7, column=1, padx=20, pady=14, sticky=customtkinter.W)
        self.button_3 = customtkinter.CTkButton(self.right_side_bar_frame, text="Button 3",  fg_color="#3b82f6",
                                                corner_radius=8, hover_color=None,  text_color="white",
                                                font=("Helvetica", 14))
        self.button_3.grid(row=8, column=1, padx=20, pady=14, sticky=customtkinter.W)
        self.button_4 = customtkinter.CTkButton(self.right_side_bar_frame, text="Button 4", fg_color="#3b82f6",
                                                corner_radius=8, hover_color=None,
                                                text_color="white", font=("Helvetica", 14))
        self.button_4.grid(row=9, column=1, padx=20, pady=14, sticky=customtkinter.W)

        # @description: Right sidebar frame ends here

        # @description: Status bar frame starts here
        self.status_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=54)
        self.status_bar_frame.pack(fill=customtkinter.X, side=customtkinter.BOTTOM)

        self.status_cam = customtkinter.CTkLabel(self.status_bar_frame, text="System idle", fg_color="#bfdbfe",
                                                 font=("Helvetica", 20), corner_radius=8, text_color="#3b82f6", )
        self.status_cam.pack(side=customtkinter.LEFT, padx=14, pady=14)
        # @description: Status bar frame ends here


if __name__ == "__main__":
    app = App()
    # @description: Hides the sidebar when escape is pressed
    app.bind("<Escape>", lambda e: app.left_side_bar_frame.pack_forget() or app.right_side_bar_frame.pack_forget())
    # @description: Shows the Left sidebar when F1 is pressed
    app.bind("<F1>", lambda e: app.left_side_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y))
    # @description: Shows the Right sidebar when F2 is pressed
    app.bind("<F2>", lambda e: app.right_side_bar_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.Y))
    app.mainloop()
