import tkinter as tk


class MyApp:
    def __init__(self, master):
        self.master = master
        self.master.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Set minimum width and height
        min_width = 1280
        min_height = 823

        # Check if the new size is less than the minimum
        if event.width < min_width or event.height < min_height:
            self.master.geometry(f"{min_width}x{min_height}+0+0")
            print("Window size set to minimum:", min_width, "x", min_height)
        else:
            # Set the window size to the maximum screen size
            self.master.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}+0+0")
            print("Window resized to:", self.master.winfo_screenwidth(), "x", self.master.winfo_screenheight())


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
