import tkinter as tk
from tkinter import font, colorchooser, filedialog
from PIL import Image

class QSLDesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QSL Card Designer")
        self.dark_mode = True

        # Main frame
        self.main_frame = tk.Frame(root, bg="#444444")
        self.main_frame.pack(padx=20, pady=20)

        # Canvas for image display
        self.canvas = tk.Canvas(self.main_frame, width=800, height=600, bg="white", highlightbackground="#cccccc")
        self.canvas.pack(side=tk.LEFT)

        # Side frame for controls
        self.side_frame = tk.Frame(self.main_frame, bg="#444444")
        self.side_frame.pack(side=tk.RIGHT, padx=20)

        # Text input field
        tk.Label(self.side_frame, text="Text:", bg="#444444", fg="white").pack(anchor="w", pady=5)
        self.text_entry = tk.Entry(self.side_frame, bg="#cccccc", fg="black")
        self.text_entry.pack(anchor="w", pady=5)

        # Font selection
        tk.Label(self.side_frame, text="Font:", bg="#444444", fg="white").pack(anchor="w", pady=5)
        self.font_var = tk.StringVar()
        self.font_var.set("Arial")  # Default font
        font_options = font.families()
        self.font_dropdown = tk.OptionMenu(self.side_frame, self.font_var, *font_options, command=self.update_font)
        self.font_dropdown.pack(anchor="w", pady=5)

        # Text size selection
        tk.Label(self.side_frame, text="Text Size:", bg="#444444", fg="white").pack(anchor="w", pady=5)
        self.text_size_var = tk.StringVar()
        self.text_size_var.set("12")  # Default text size
        text_size_options = [str(i) for i in range(8, 41)]  # Text sizes from 8 to 40
        self.text_size_dropdown = tk.OptionMenu(self.side_frame, self.text_size_var, *text_size_options, command=self.update_text_size)
        self.text_size_dropdown.pack(anchor="w", pady=5)

        # Text color selection
        self.text_color_button = tk.Button(self.side_frame, text="Select Text Color", command=self.choose_text_color, bg="#666666")
        self.text_color_button.pack(anchor="w", pady=5)

        # Background color selection
        self.bg_color_button = tk.Button(self.side_frame, text="Select Background Color", command=self.choose_bg_color, bg="#666666")
        self.bg_color_button.pack(anchor="w", pady=5)

        # Select background image button
        self.bg_image_button = tk.Button(self.side_frame, text="Select Background Image", command=self.choose_bg_image, bg="#666666")
        self.bg_image_button.pack(anchor="w", pady=5)

        # Add text to image button
        self.add_text_button = tk.Button(self.side_frame, text="Add Text to Image", command=self.add_text_to_image, bg="#666666")
        self.add_text_button.pack(anchor="w", pady=5)

        # Remove text from image button
        self.remove_text_button = tk.Button(self.side_frame, text="Remove Text from Image", command=self.remove_text_from_image, bg="#666666")
        self.remove_text_button.pack(anchor="w", pady=5)

        # Save image as PNG button
        self.save_button = tk.Button(self.side_frame, text="Save as PNG", command=self.save_image_as_png, bg="#666666")
        self.save_button.pack(anchor="w", pady=5)

        # Default colors
        self.text_color = "white"
        self.bg_color = "#cccccc"
        self.bg_image = None

        # Variables for drag-and-drop
        self.drag_data = {"x": 0, "y": 0}
        self.selected_text = None

        # Bind events for drag-and-drop
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.drop)

    def add_text_to_image(self):
        text = self.text_entry.get()
        font_family = self.font_var.get()
        text_size = int(self.text_size_var.get())
        x, y = 100, 100  # Default coordinates
        text_object = self.canvas.create_text(x, y, text=text, font=(font_family, text_size), fill=self.text_color, anchor="nw", tags="text")
        self.selected_text = text_object

    def remove_text_from_image(self):
        if self.selected_text:
            self.canvas.delete(self.selected_text)
            self.selected_text = None

    def choose_text_color(self):
        color = colorchooser.askcolor()
        if color:
            self.text_color = color[1]

    def choose_bg_color(self):
        color = colorchooser.askcolor()
        if color:
            self.bg_color = color[1]
            self.canvas.config(bg=self.bg_color)

    def choose_bg_image(self):
        file_path = filedialog.askopenfilename(title="Select Background Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.bg_image = tk.PhotoImage(file=file_path)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        if self.selected_text:
            self.canvas.move(self.selected_text, delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drop(self, event):
        pass

    def update_font(self, event):
        font_family = self.font_var.get()
        if self.selected_text:
            self.canvas.itemconfig(self.selected_text, font=(font_family, int(self.text_size_var.get())))

    def update_text_size(self, event):
        text_size = int(self.text_size_var.get())
        if self.selected_text:
            self.canvas.itemconfig(self.selected_text, font=(self.font_var.get(), text_size))

    def save_image_as_png(self):
        # Get the dimensions and position of the canvas
        x0 = self.canvas.winfo_rootx()
        y0 = self.canvas.winfo_rooty()
        x1 = x0 + self.canvas.winfo_width()
        y1 = y0 + self.canvas.winfo_height()

        # Create an empty image with the same size as the canvas
        image = Image.new("RGBA", (x1 - x0, y1 - y0), color="white")

        # Capture the content of the canvas and paste it onto the image
        self.canvas.postscript(file="temp.ps", colormode="color")
        image = Image.open("temp.ps")
        image.save("canvas_content.png", "png")

        # Ask the user to select a file path to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        # Save the captured image as a PNG file
        if file_path:
            image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = QSLDesignApp(root)
    root.mainloop()
