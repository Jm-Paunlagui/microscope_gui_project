from tkinter import PhotoImage
import customtkinter as tk
from PIL import Image

# dictionary of colors:
color = {"nero": "#252726", "orange": "#FF8700", "darkorange": "#FE6101"}

# setting root window:
root = tk.CTk()
root.title("Tkinter Navbar")
root.config(bg="gray17")
root.geometry("400x600+850+50")

# setting switch state:
btnState = False

# loading Navbar icon image:
navIcon = tk.CTkImage(
            light_image=Image.open("../assets/icons/bars.png"),
            size=(24, 24)
        )
closeIcon = tk.CTkImage(
            light_image=Image.open("../assets/icons/bars.png"),
            size=(24, 24)
        )


# setting switch function:
def switch():
    global btnState
    if btnState is True:
        # create animated Navbar closing:
        for x in range(301):
            navRoot.place(x=-x, y=0)
            topFrame.update()

        # resetting widget colors:
        brandLabel.configure(bg_color="gray17", fg_color="green")
        homeLabel.configure(bg_color=color["orange"])
        topFrame.configure(bg_color=color["orange"])
        root.configure(bg_color="gray17")

        # turning button OFF:
        btnState = False
    else:
        # make root dim:
        brandLabel.configure(bg_color=color["nero"], fg_color="#5F5A33")
        homeLabel.configure(bg_color=color["nero"])
        topFrame.configure(bg_color=color["nero"])
        root.configure(bg_color=color["nero"])

        # created animated Navbar opening:
        for x in range(-300, 0):
            navRoot.place(x=x, y=0)
            topFrame.update()

        # turing button ON:
        btnState = True


# top Navigation bar:
topFrame = tk.CTkFrame(root, bg_color=color["orange"])
topFrame.pack(side="top", fill=tk.X)

# Header label text:
homeLabel = tk.CTkLabel(topFrame, text="PE", font=("BahnschriftLight", 15), bg_color=color["orange"], fg_color="gray17",
                        height=50, padx=20)
homeLabel.pack(side="right")

# Main label text:
brandLabel = tk.CTkLabel(root, text="Pythonista\nEmpire", font=("BahnschriftLight", 15), bg_color="gray17",
                         fg_color="green")
brandLabel.place(x=100, y=250)

# Navbar button:
navbarBtn = tk.CTkButton(topFrame, image=navIcon, bg_color=color["orange"], command=switch)
navbarBtn.place(x=10, y=10)

# setting Navbar frame:
navRoot = tk.CTkFrame(root, bg_color="gray17", height=1000, width=300)
navRoot.place(x=-300, y=0)
tk.CTkLabel(navRoot, font=("BahnschriftLight", 15), bg_color=color["orange"], fg_color="black", height=2, width=300,
            padx=20).place(x=0, y=0)

# set y-coordinate of Navbar widgets:
y = 80
# option in the navbar:
options = ["Profile", "Settings", "Help", "About", "Feedback"]
# Navbar Option Buttons:
for i in range(5):
    tk.CTkButton(navRoot, text=options[i], font=("BahnschriftLight", 15), bg_color="gray17", fg_color=color["orange"],
                 ).place(x=25, y=y)
    y += 40

# Navbar Close Button:
closeBtn = tk.CTkButton(navRoot, image=closeIcon, bg_color=color["orange"],
                        command=switch)
closeBtn.place(x=250, y=10)

# window in mainloop:
root.mainloop()
