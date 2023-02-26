import customtkinter as tk
from tkinter import messagebox

root = tk.CTk()
root.geometry("300x200")

w = tk.CTkLabel(root, text='GeeksForGeeks', font=("Helvetica", 16))
w.pack()


messagebox.showinfo("showinfo", "Information")

messagebox.showwarning("showwarning", "Warning")

messagebox.showerror("showerror", "Error")

messagebox.askquestion("askquestion", "Are you sure?")

messagebox.askokcancel("askokcancel", "Want to continue?")

messagebox.askyesno("askyesno", "Find the value?")

messagebox.askretrycancel("askretrycancel", "Try again?")

messageboxdemo = tk.CTk
messageboxdemo.pack()



root.mainloop()