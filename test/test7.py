import tkinter as tk

# create a tkinter window
root = tk.Tk()

# get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(f"Screen width: {screen_width}")
print(f"Screen height: {screen_height}")
# set window geometry to the center of the screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

# run the main loop
root.mainloop()
