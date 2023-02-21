import time
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
    # @description: Only the last option will be displayed in the status bar
    app.status_cam.configure(text=option + " selected")


def sidebar_button_event1():
    print("sidebar_button click")
    # @description: Only the last option will be displayed in the status bar
    app.status_cam.configure(text="Button 1.1 clicked")


def sidebar_button_event2():
    print("sidebar_button click")
    # @description: Only the last option will be displayed in the status bar
    app.status_cam.configure(text="Button 2.2 clicked")


def sidebar_button_event3():
    print("sidebar_button click")
    # @description: Only the last option will be displayed in the status bar
    app.status_cam.configure(text="Button 3.3 clicked")


def sidebar_button_event4():
    print("sidebar_button click")
    # @description: Only the last option will be displayed in the status bar
    app.status_cam.configure(text="Button 4.4 clicked")


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

        self.status_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white", height=50)
        self.status_bar_frame.pack(fill=customtkinter.X, side=customtkinter.BOTTOM)

        # @description: Menu icon
        bars = customtkinter.CTkImage(
            light_image=Image.open("assets/icons/bars.png"),
            dark_image=Image.open("assets/icons/bars.png"),
            size=(24, 24)
        )

        # @description: Left Side Bar frame with widgets (hambuger menu, title...)
        self.left_side_bar_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.left_side_bar_frame.pack(side=customtkinter.LEFT, fill=customtkinter.Y)

        # @description: Initial state of sidebar is hidden (pack_forget)
        self.left_side_bar_frame.pack_forget()

        # @description: Rows Config for sidebar_frame
        self.left_side_bar_frame.grid_rowconfigure(15, weight=1)

        # @description: Sidebar OptionMenu
        self.label_options = customtkinter.CTkLabel(self.left_side_bar_frame, text="Microscope Options",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_options.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_option_1 = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.1", "Option 2.1", "Option 3.1"], command=test_event)
        self.sidebar_option_1.grid(row=1, column=0, padx=0, pady=10)
        self.sidebar_option_2 = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.2", "Option 2.2", "Option 3.2"], command=test_event)
        self.sidebar_option_2.grid(row=2, column=0, padx=0, pady=10)
        self.sidebar_option_3 = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.3", "Option 2.3", "Option 3.3"], command=test_event)
        self.sidebar_option_3.grid(row=3, column=0, padx=0, pady=10)
        self.sidebar_option_4 = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.4", "Option 2.4", "Option 3.4"], command=test_event)
        self.sidebar_option_4.grid(row=4, column=0, padx=0, pady=10)

        self.sidebar_segmented_button_1 = customtkinter.CTkSegmentedButton(self.left_side_bar_frame,
                                                                           values=["S-Button 1", "S-Button 2"],
                                                                           command=test_event)
        self.sidebar_segmented_button_1.grid(row=5, column=0, padx=0, pady=10)
        self.sidebar_segmented_button_1.set("Button 1")

        # @description: Combobox with values
        self.sidebar_combobox_1 = customtkinter.CTkOptionMenu(
            self.left_side_bar_frame, values=["Option 1.5", "Option 2.5", "Option 3.5"], command=test_event)
        self.sidebar_combobox_1.grid(row=6, column=0, padx=0, pady=10)

        # @description: Camera buttons
        self.label_options_3 = customtkinter.CTkLabel(self.left_side_bar_frame, text="Camera Options",
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_options_3.grid(row=7, column=0, padx=0, pady=10)
        self.camera_button_1 = customtkinter.CTkButton(self.left_side_bar_frame, text="Button 1.1",
                                                       command=sidebar_button_event1)
        self.camera_button_1.grid(row=8, column=0, padx=0, pady=10, sticky="s")
        self.camera_button_2 = customtkinter.CTkButton(self.left_side_bar_frame, text="Button 2.2",
                                                       command=sidebar_button_event2)
        self.camera_button_2.grid(row=9, column=0, padx=0, pady=10, sticky="s")
        self.camera_button_3 = customtkinter.CTkButton(self.left_side_bar_frame, text="Button 3.3",
                                                       command=sidebar_button_event3)
        self.camera_button_3.grid(row=10, column=0, padx=0, pady=10, sticky="s")
        self.camera_button_4 = customtkinter.CTkButton(self.left_side_bar_frame, text="Button 4.4",
                                                       command=sidebar_button_event4)
        self.camera_button_4.grid(row=11, column=0, padx=0, pady=10, sticky="s")

        # @description: Content frame with widgets (camera, ...)
        self.content_frame = customtkinter.CTkFrame(self, )
        self.content_frame.pack(fill=customtkinter.BOTH, expand=customtkinter.YES, side=customtkinter.RIGHT)

        # @description: Top Bar frame with widgets (hambuger menu, title, settings, ...)
        self.menu_button = customtkinter.CTkButton(self.top_bar_frame, width=18, image=bars, text="",
                                                   fg_color="white", corner_radius=8, hover_color="white",
                                                   text_color="white", command=toggle_sidebar_event)
        self.menu_button.pack(side=customtkinter.LEFT, padx=14, pady=14)

        # @description: Camera status label
        self.status_cam = customtkinter.CTkLabel(self.status_bar_frame, text="System idle", fg_color="#bfdbfe",
                                                 font=("Helvetica", 20), corner_radius=8, text_color="#3b82f6",
                                                 )
        self.status_cam.pack(side=customtkinter.LEFT, padx=14, pady=14)

        self.top_bar_title = customtkinter.CTkLabel(self.top_bar_frame, text="App title",
                                                    font=("Helvetica", 20, "bold"), text_color="black")
        self.top_bar_title.pack(side=customtkinter.LEFT, padx=0, pady=14)

        # @description: Canvas for the camera image
        self.camera_canvas = customtkinter.CTkCanvas(self.content_frame, width=self.content_frame.winfo_width(),
                                                     height=self.content_frame.winfo_height())
        self.camera_canvas.pack(fill="both", expand=True)

        self.camera_canvas.update()
        # @description: Camera VideoCapture
        # VideoCapture here:
        self.cap = cv2.VideoCapture(0)

        # Set the time limit to 30 seconds
        self.time_limit = 30

        # Initialize the last frame time and the hover flag
        self.last_frame_time = time.time()

        # @description: Camera image update function
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
            self.camera_canvas = customtkinter.CTkCanvas(self.content_frame, width=self.content_frame.winfo_width(),
                                                         height=self.content_frame.winfo_height(), closeenough=1)
            self.camera_canvas.pack(fill="both", expand=True)
            self.inactive_camera_label = customtkinter.CTkLabel(self.camera_canvas, text="Camera not in use",
                                                                font=customtkinter.CTkFont(size=20, weight="bold"))
            self.inactive_camera_label.place(relx=0.5, rely=0.5, anchor="center")

        # @description: Update the image
        # update_image()
        inactive_camera()

    # @description: Hides the sidebar when escape is pressed and shows it when it is pressed again
    def toggle_sidebar_esc(self):
        if self.left_side_bar_frame.winfo_ismapped():
            self.left_side_bar_frame.pack_forget()
        else:
            self.left_side_bar_frame.pack(fill=customtkinter.BOTH, expand=customtkinter.NO, side=customtkinter.LEFT)

    # description: Sidebar will appear either by mouse hover or by pressing the hamburger menu or by pressing Ctrl + P



if __name__ == "__main__":
    app = App()
    # @description: Hides the sidebar when escape is pressed and shows it when it is pressed again
    app.bind("<Escape>", lambda e: app.toggle_sidebar_esc())
    app.mainloop()
