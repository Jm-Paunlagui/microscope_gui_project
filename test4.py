import tkinter as tk
import cv2
from PIL import Image, ImageTk


class CustomLayout(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.cap = cv2.VideoCapture(0)
        self.main_content = tk.Frame(self.master, bg="white")
        self.bottom_bar = tk.Frame(self.master, bg="gray", height=50)
        self.right_bar = tk.Frame(self.master, bg="lightgray", width=200)
        self.left_bar = tk.Frame(self.master, bg="lightgray", width=200)
        self.top_bar = tk.Frame(self.master, bg="gray", height=50)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create the top bar
        self.top_bar.pack(side="top", fill="x")

        # Create the left side bar
        self.left_bar.pack(side="left", fill="y")

        # Create the right side bar
        self.right_bar.pack(side="right", fill="y")

        # Create the bottom bar
        self.bottom_bar.pack(side="bottom", fill="x")

        # Create the main content area
        self.main_content.pack(side="top", fill="both", expand=True)

        # Add the video capture to the main content area
        self.video_label = tk.Label(self.main_content)
        self.video_label.pack(padx=20, pady=20)
        self.update_video()

    def update_video(self):
        # Get a frame from the video capture
        ret, frame = self.cap.read()

        if ret:
            # Convert the frame from BGR to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize the image to fit the label
            image = cv2.resize(image, (640, 480))

            # Convert the image to PIL format
            image = Image.fromarray(image)

            # Convert the image to Tkinter PhotoImage format
            photo = ImageTk.PhotoImage(image)

            # Update the label with the new image
            self.video_label.configure(image=photo)
            self.video_label.image = photo

        # Schedule the next update in 1 millisecond
        self.video_label.after(1, self.update_video)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = CustomLayout(master=root)
    app.mainloop()
