import customtkinter as tk

on = 1


def close_frame(evt):
    global on, frame, lbx

    if on:
        frame.pack_forget()
        on = 0
    else:
        frame.pack_forget()
        frame1.pack_forget()
        create_frame()
        on = 1


root = tk.CTk()


def create_frame():
    """create frame to be hidden when we press k"""
    global lbx, lbx1, frame, frame1

    frame = tk.CTkFrame(root)
    frame.pack(side="left")
    lbx = tk.CTkTextbox(frame, bg_color="gold")
    lbx.pack()
    lbx.insert(
        "0.0", "This is a test of the emergency broadcast system. This is only a test.",
    )
    frame1 = tk.CTkFrame(root)
    frame1.pack()
    lbx1 = tk.CTkTextbox(frame1, bg_color="cyan")
    lbx1.pack(side="left")
    lbx1.insert(
        "0.0", "This is a test of the emergency broadcast system. This is only a test.",
    )


create_frame()

root.bind("<k>", close_frame)

root.mainloop()
