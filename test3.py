import tkinter as tk


class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("My GUI")

        # create label
        self.label = tk.Label(master, text="Initial Text")
        self.label.pack()

        # create buttons
        self.button1 = tk.Button(master, text="Button 1", command=lambda: self.set_text("Button 1 clicked"))
        self.button1.pack()

        self.button2 = tk.Button(master, text="Button 2", command=lambda: self.set_text("Button 2 clicked"))
        self.button2.pack()

        self.button3 = tk.Button(master, text="Button 3", command=lambda: self.set_text("Button 3 clicked"))
        self.button3.pack()

        self.button4 = tk.Button(master, text="Button 4", command=lambda: self.set_text("Button 4 clicked"))
        self.button4.pack()

    def set_text(self, text):
        # set label text based on button clicked
        self.label.configure(text=text)


def external_function(gui_instance, text):
    gui_instance.set_text(text)


root = tk.Tk()
my_gui = MyGUI(root)

# access set_text externally
external_function(my_gui, "External function called")

root.mainloop()
