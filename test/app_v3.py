import time
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


# def test_event(option: str):
#     print(option)
#     # @description: Only the last option will be displayed in the status bar
#     app.status_cam.configure(text=option + " selected")
#
#
# def sidebar_button_event1():
#     print("sidebar_button click")
#     # @description: Only the last option will be displayed in the status bar
#     app.status_cam.configure(text="Button 1.1 clicked")
#
#
# def sidebar_button_event2():
#     print("sidebar_button click")
#     # @description: Only the last option will be displayed in the status bar
#     app.status_cam.configure(text="Button 2.2 clicked")
#
#
# def sidebar_button_event3():
#     print("sidebar_button click")
#     # @description: Only the last option will be displayed in the status bar
#     app.status_cam.configure(text="Button 3.3 clicked")
#
#
# def sidebar_button_event4():
#     print("sidebar_button click")
#     # @description: Only the last option will be displayed in the status bar
#     app.status_cam.configure(text="Button 4.4 clicked")
#
#
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

        self.title("App title")
        self.geometry(f"{1280}x{832}")
        self.configure(fg_color="#d1d5db", bg_color="#1f2937")

        # Create top bar, left side bar, camera frame, and status bar frames
        self.top_bar_frame = self.top_bar_frame
        self.left_side_bar_frame = self.left_side_bar_frame
        self.camera_frame = self.camera_frame
        self.status_bar_frame = self.status_bar_frame

        # Icon for the menu button
        menu_icon = customtkinter.CTkImage(
            light_image=Image.open("../assets/icons/bars.png"),
            dark_image=Image.open("../assets/icons/bars.png"),
            size=(24, 24)
        )

        # Create menu button using the top bar frame as the master
        self.menu_button = customtkinter.CTkButton(
            master=self.top_bar_frame, width=18, height=18, image=menu_icon,
            fg_color="white", bg_color="black", corner_radius=8,
            hover_color="white",
            text_color="white", command=toggle_sidebar_event
        )
        self.menu_button.pack(side=customtkinter.LEFT, padx=14, pady=14)

    def top_bar_frame(self):
        self.top_bar_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="white", height=50
        )
        self.top_bar_frame.pack(fill=customtkinter.X, side=customtkinter.TOP)

    def left_side_bar_frame(self):
        self.left_side_bar_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="white"
        )
        self.left_side_bar_frame.pack(
            side=customtkinter.LEFT, fill=customtkinter.Y
        )
        self.left_side_bar_frame.grid_rowconfigure(15, weight=1)
        self.left_side_bar_frame.pack_forget()

    def camera_frame(self):
        self.camera_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="white"
        )
        self.camera_frame.pack(
            fill=customtkinter.BOTH, expand=customtkinter.YES, side=customtkinter.RIGHT
        )

    def status_bar_frame(self):
        self.status_bar_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="white", height=50
        )
        self.status_bar_frame.pack(fill=customtkinter.X, side=customtkinter.BOTTOM)


if __name__ == "__main__":
    app = App()
    # @description: Hides the sidebar when escape is pressed and shows it when it is pressed again
    # app.bind("<Escape>", lambda e: app.toggle_sidebar_esc())
    app.mainloop()
