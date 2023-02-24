import time
from typing import Union, Callable
import customtkinter
import cv2
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"]


def test_event(option: str):
    print(option)
    # @description: Only the last option will be displayed in the status bar
    app.status_cam.configure(text=option + " selected")


def toggle_sidebar_event():
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


class FloatSpinbox(customtkinter.CTkFrame):
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
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            if value > self.max_value:
                value = self.max_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value if value >= 0 else 0)
            app.z_drive_config.configure(text=f"{app.coarse_focus_options.get()} - {app.fine_focus_options.get()}")
            if app.condenser_diaphragm_options.get() is not None:
                app.status_cam.configure(
                    text=f"Condenser : {app.condenser_diaphragm_options.get()}")
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            if value < self.min_value:
                value = self.min_value
            self.entry.delete(0, "end")
            self.entry.insert(0, value if value <= self.max_value else self.max_value)
            app.z_drive_config.configure(text=f"{app.coarse_focus_options.get()} - {app.fine_focus_options.get()}")
            if app.condenser_diaphragm_options.get() is not None:
                app.status_cam.configure(
                    text=f"Condenser : {app.condenser_diaphragm_options.get()}")
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))


class App(customtkinter.CTk):
    def __init__(self):
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

        # @description: Top Bar frame with widgets (hambuger menu, title, settings, ...)
        self.top_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=48)
        self.top_bar_frame.pack(fill=customtkinter.X, side=customtkinter.TOP)

        # @description: Top Bar frame with widgets (hambuger menu, title, settings, ...)
        self.menu_button = customtkinter.CTkButton(self.top_bar_frame, width=18, image=bars, text="", fg_color="white",
                                                   corner_radius=8, hover_color="white", text_color="white",
                                                   command=toggle_sidebar_event)
        self.menu_button.pack(side=customtkinter.LEFT, padx=14, pady=14)
        self.top_bar_title = customtkinter.CTkLabel(self.top_bar_frame, text="App title",
                                                    font=("Helvetica", 20, "bold"), text_color="black")
        self.top_bar_title.pack(side=customtkinter.LEFT, padx=0, pady=14)
        self.left_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.left_side_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y)
        self.left_side_bar_frame.grid_rowconfigure(15, weight=1)
        # @description: Initial state of the sidebar is hidden (pack_forget)
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

        self.objective_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.1", "Option 2.1", "Option 3.1"], command=test_event)
        self.objective_options.grid(row=1, column=1, padx=20, pady=10, sticky=customtkinter.W)
        self.condenser_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.2", "Option 2.2", "Option 3.2"], command=test_event)
        self.condenser_options.grid(row=2, column=1, padx=0, pady=10)
        self.reflector_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.3", "Option 2.3", "Option 3.3"], command=test_event)
        self.reflector_options.grid(row=3, column=1, padx=0, pady=10)
        self.side_port = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.4", "Option 2.4", "Option 3.4"], command=test_event)
        self.side_port.grid(row=4, column=1, padx=0, pady=10)
        self.tube_lens_options = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.5", "Option 2.5", "Option 3.5"], command=test_event)
        self.tube_lens_options.grid(row=5, column=1, padx=0, pady=10)
        self.shutter_options = customtkinter.CTkSegmentedButton(self.left_side_bar_frame,
                                                                values=["S-Button 1", "S-Button 2"],
                                                                command=test_event)
        self.shutter_options.grid(row=6, column=1, padx=0, pady=10)
        self.condenser_diaphragm_options = FloatSpinbox(self.left_side_bar_frame, width=150, step_size=1, min_value=0.0,
                                                        max_value=1400.0)
        self.condenser_diaphragm_options.grid(row=7, column=1, padx=0, pady=10)
        self.condenser_diaphragm_options.set(700.0)
        self.coarse_focus_options = FloatSpinbox(self.left_side_bar_frame, width=150, step_size=100, min_value=0.0,
                                                 max_value=40000.0)
        self.coarse_focus_options.grid(row=9, column=1, padx=0, pady=10)
        self.coarse_focus_options.set(20000.0)
        self.fine_focus_options = FloatSpinbox(self.left_side_bar_frame, width=150, step_size=1, min_value=0.0,
                                               max_value=99)
        self.fine_focus_options.grid(row=10, column=1, padx=0, pady=10)
        self.fine_focus_options.set(50.0)
        self.z_drive_config = customtkinter.CTkLabel(
            self.left_side_bar_frame, text=f"{self.coarse_focus_options.get()} - {self.fine_focus_options.get()}",
            fg_color="#bfdbfe", font=("Helvetica", 20), corner_radius=8,
            text_color="#3b82f6", )
        self.z_drive_config.grid(row=8, column=1, padx=0, pady=10)

        self.status_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=50)
        self.status_bar_frame.pack(fill=customtkinter.X, side=customtkinter.BOTTOM)

        self.status_cam = customtkinter.CTkLabel(self.status_bar_frame, text="System idle", fg_color="#bfdbfe",
                                                 font=("Helvetica", 20), corner_radius=8, text_color="#3b82f6", )
        self.status_cam.pack(side=customtkinter.LEFT, padx=14, pady=14)
        self.auto_white_balance = customtkinter.CTkButton(self.status_bar_frame, text="Auto White Balance",
                                                          font=("Helvetica", 20), corner_radius=8, )
        self.auto_white_balance.pack(side=customtkinter.RIGHT, padx=14, pady=14)
        # self.auto_white_balance_label = customtkinter.CTkLabel(self.status_bar_frame, text="Auto White Balance",
        #                                                        fg_color="#bfdbfe", font=("Helvetica", 20),
        #                                                        corner_radius=8, text_color="#3b82f6")
        # self.auto_white_balance_label.pack(side=customtkinter.RIGHT, padx=14, pady=14)
        self.sharpness_level = FloatSpinbox(self.status_bar_frame, step_size=1, min_value=0.0, max_value=9.0)
        self.sharpness_level.pack(side=customtkinter.RIGHT, padx=0, pady=14)
        self.sharpness_label = customtkinter.CTkLabel(self.status_bar_frame, text="Sharpness", fg_color="#bfdbfe",
                                                      font=("Helvetica", 20), corner_radius=8, text_color="#3b82f6", )
        self.sharpness_label.pack(side=customtkinter.RIGHT, padx=14, pady=14)
        self.contrast_level = FloatSpinbox(self.status_bar_frame, step_size=1, min_value=0.0, max_value=100.0)
        self.contrast_level.pack(side=customtkinter.RIGHT, padx=0, pady=14)
        self.contrast_label = customtkinter.CTkLabel(self.status_bar_frame, text="Contrast", fg_color="#bfdbfe",
                                                     font=("Helvetica", 20), corner_radius=8, text_color="#3b82f6", )
        self.contrast_label.pack(side=customtkinter.RIGHT, padx=14, pady=14)
        self.brightness_level = FloatSpinbox(self.status_bar_frame, step_size=1, min_value=0.0, max_value=100.0)
        self.brightness_level.pack(side=customtkinter.RIGHT, padx=0, pady=14)
        self.brightness_label = customtkinter.CTkLabel(self.status_bar_frame, text="Brightness", fg_color="#bfdbfe",
                                                       font=("Helvetica", 20), corner_radius=8, text_color="#3b82f6", )
        self.brightness_label.pack(side=customtkinter.RIGHT, padx=14, pady=14)


if __name__ == "__main__":
    app = App()
    # @description: Hides the sidebar when escape is pressed and shows it when it is pressed again
    # app.bind("<Escape>", lambda e: app.toggle_sidebar_esc())
    app.mainloop()
