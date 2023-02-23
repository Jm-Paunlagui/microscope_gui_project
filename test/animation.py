import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Canvas animation example")

        self.c = tk.Canvas(self, width=400, height=400)
        self.c.pack()

        self.f_index = 0 # index so we know which frame to draw next
        # array to hold our frame data,
        # you'll probably need this to hold more than
        # just a set of coordinates to draw a line...
        self.f_data = []

        for num in range(0, 400, 5): # make up a set of fake data
            self.f_data.append([num, num, num+10, num+10])

    def next_frame(self):
        data = self.f_data[self.f_index] # fetch frame data
        self.c.delete('all') # clear canvas
        self.c.create_line(*data) # draw new frame data
        self.f_index += 1 # increment frame index
        if (self.f_index >= len(self.f_data)): # check and wrap if at end of sequence
            self.f_index = 0
        self.c.after(50, self.next_frame) # call again after 50ms

if __name__ == "__main__":
    app = App()
    app.next_frame() # called manually once to start animation
    # could be started with 'after' instead if desired
    app.mainloop()