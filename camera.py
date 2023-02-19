import cv2
import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        # Create main window
        self.window = customtkinter.CTk()
        self.window.geometry("640x480")
        self.window.resizable(False, False)
        self.window.title("Video Capture")

        # Create main frame
        self.main_frame = customtkinter.CTkFrame(self.window)
        self.main_frame.pack()

        # Create canvas widget to display video
        self.canvas = customtkinter.CTkCanvas(self.main_frame, width=640, height=480)
        self.canvas.pack()

        # Create video capture object
        self.video_capture = cv2.VideoCapture(0)

        # Start video capture loop
        self.update_video()

        # Start main loop
        self.window.mainloop()

    def update_video(self):
        # Read frame from video capture
        ret, frame = self.video_capture.read()

        if ret:
            # Convert frame to image
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = customtkinter.CTkImage.fromarray(img)

            # Update image in canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=img)

        # Schedule next update
        self.window.after(10, self.update_video)


if __name__ == "__main__":
    app = App()
    app.mainloop()
