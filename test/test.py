import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

# create top bar frame
top_bar_frame = tk.Frame(root, bg="gray", height=50)
top_bar_frame.pack(side=tk.TOP, fill=tk.X)

# create left buttons frame
left_buttons_frame = tk.Frame(top_bar_frame, bg="gray")
left_buttons_frame.pack(side=tk.LEFT)

# create right buttons frame
right_buttons_frame = tk.Frame(top_bar_frame, bg="gray")
right_buttons_frame.pack(side=tk.RIGHT)


# create content frame
content_frame = tk.Frame(root, bg="white")
content_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# add widgets to the frames
tk.Button(left_buttons_frame, text="Left Button 1").pack(side=tk.LEFT, padx=5)

tk.Button(right_buttons_frame, text="Right Button 1").pack(side=tk.RIGHT, padx=5)

tk.Label(content_frame, text="Content", fg="black", bg="black").pack(fill=tk.BOTH, expand=True)

root.mainloop()
