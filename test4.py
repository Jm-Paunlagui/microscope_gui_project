import tkinter as tk


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create a sidebar frame
        self.sidebar = tk.Frame(self, width=200, bg="gray")
        self.sidebar.pack(side="left", fill="y")

        # Create a content frame
        self.content = tk.Frame(self, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        # Bind the mouse enter and leave events to show and hide the sidebar
        self.content.bind("<Enter>", self.show_sidebar)
        self.content.bind("<Leave>", self.schedule_hide_sidebar)

        # Create a hamburger menu button
        self.menu_button = tk.Button(self.content, text="☰", font=("Arial", 14), bg="white", bd=0,
                                     command=self.toggle_sidebar)
        self.menu_button.pack(side="left")

        # Bind the Ctrl+P key to toggle the sidebar
        self.bind("<Control-p>", self.toggle_sidebar)

        # Set the delay time for hiding the sidebar on mouse leave
        self.hide_delay = 300  # in milliseconds

    def toggle_sidebar(self, event=None):
        # Check if the sidebar is currently visible
        if self.sidebar.winfo_ismapped():
            # Hide the sidebar
            self.sidebar.pack_forget()
        else:
            # Show the sidebar
            self.sidebar.pack(side="left", fill="y")

    def show_sidebar(self, event):
        # Show the sidebar
        self.sidebar.pack(side="left", fill="y")

    def hide_sidebar(self):
        # Hide the sidebar
        self.sidebar.pack_forget()

    def schedule_hide_sidebar(self, event):
        # Use the after method to delay the execution of the hide_sidebar method
        self.after(self.hide_delay, self.hide_sidebar)


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
