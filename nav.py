import customtkinter
import customtkinter as ctk
customtkinter.set_appearance_mode("Light")


class NavigationBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Set the app title
        self.app_title = ctk.CTkLabel(self, text="My App", font=("Helvetica", 20))
        self.app_title.pack(side="top", padx=10)

        # Create the hamburger menu
        self.menu_button = ctk.CTkButton(self, text="☰", font=("Helvetica", 20),
                                         command=self.toggle_menu)
        self.menu_button.pack(side="top")

        # Create the menu
        self.menu_frame = ctk.CTkFrame(self, bg_color="#EEE", height=800)
        self.menu_frame.place(y=-900)
        self.menu_visible = False

        # Add some menu items
        self.menu_item1 = ctk.CTkLabel(self.menu_frame, text="Menu Item 1",
                                       font=("Helvetica", 16), bg_color="#EEE")
        self.menu_item1.pack(pady=10, padx=20)
        self.menu_item2 = ctk.CTkLabel(self.menu_frame, text="Menu Item 2",
                                       font=("Helvetica", 16), bg_color="#EEE")
        self.menu_item2.pack(pady=10, padx=20)
        self.menu_item3 = ctk.CTkLabel(self.menu_frame, text="Menu Item 3",
                                       font=("Helvetica", 16), bg_color="#EEE")
        self.menu_item3.pack(pady=10, padx=20)

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self, bg_color="#FFF", height=800)
        self.content_frame.pack(side="bottom", fill="both", expand=True)

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_frame.place(x=-900, y=-100)  # Place menu offscreen
            self.menu_visible = False
        else:
            self.menu_frame.place(x=0, y=-100)  # Place menu below app title
            self.menu_visible = True
            self.menu_frame.lift()  # Bring menu to front


# Create the main CustomTkinter window and add the NavigationBar
root = ctk.CTk()
root.geometry("800x600")
nav_bar = NavigationBar(root)
nav_bar.pack(fill="x")
root.mainloop()
