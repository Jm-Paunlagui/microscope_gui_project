import tkinter as tk

root = tk.Tk()

# Set minimum and maximum window size
MIN_WIDTH, MIN_HEIGHT = 1280, 823
MAX_WIDTH, MAX_HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


# Function to handle window resizing
def on_resize(event):
    # Get the new size of the window
    width, height = event.width, event.height
    print(f"Window resized to: {width}x{height}")

    # Check if the new size is less than the minimum size
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        # Resize the window to the minimum size
        root.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
    # Check if the new size is greater than the minimum size and set the maximum size
    elif width > MAX_WIDTH or height > MAX_HEIGHT:
        # Resize the window to the maximum size
        root.geometry(f"{MAX_WIDTH}x{MAX_HEIGHT}")


# Bind the "<Configure>" event to the on_resize function
root.bind("<Configure>", on_resize)

# Start the main loop
root.mainloop()
