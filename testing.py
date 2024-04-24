import tkinter as tk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Static Buttons Example")

        # Create a frame to contain the buttons
        button_frame = tk.Frame(root)

        # Create buttons
        btn1 = tk.Button(button_frame, text="Button 1", command=self.button1_click)
        btn2 = tk.Button(button_frame, text="Button 2", command=self.button2_click)

        # Pack buttons inside the frame
        btn1.pack(side=tk.LEFT, padx=5)
        btn2.pack(side=tk.LEFT, padx=5)

        # Pack the frame at the bottom of the window
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def button1_click(self):
        print("Button 1 clicked")

    def button2_click(self):
        print("Button 2 clicked")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
