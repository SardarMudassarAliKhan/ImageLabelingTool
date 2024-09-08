import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import json

class ImageLabelingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Mudassar Ali Solution - Image Labeling Tool")  # Set title with your name

        self.folder_path = ""
        self.image_list = []
        self.current_image = None
        self.image_display = None
        self.annotations = []
        self.selected_tool = None
        self.selected_label = None

        self.init_gui()

    def init_gui(self):
        # Menu for file actions
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        # Add your name in the top menu bar
        menu.add_cascade(label="Mudassar Ali Solution")

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Folder", command=self.load_folder)
        file_menu.add_command(label="Save Annotations", command=self.save_annotations)

        # Frames
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Annotation Pane (listbox for annotations)
        annotation_label = tk.Label(left_frame, text="Annotations")
        annotation_label.pack(side=tk.TOP, pady=5)

        self.annotation_listbox = tk.Listbox(left_frame, height=10, width=40)
        self.annotation_listbox.pack(side=tk.TOP, pady=5)

        # Listbox for images
        self.image_listbox = tk.Listbox(left_frame, height=10, width=40)
        self.image_listbox.pack(side=tk.TOP, pady=5)
        self.image_listbox.bind('<<ListboxSelect>>', self.load_image)

        # Listbox for labels
        label_frame = tk.Frame(left_frame)
        label_frame.pack(side=tk.TOP)

        label_title = tk.Label(label_frame, text="Labels")
        label_title.pack(side=tk.TOP, pady=5)

        self.label_listbox = tk.Listbox(left_frame, height=10, width=40)
        self.label_listbox.pack(side=tk.TOP, pady=10)

        self.label_entry = tk.Entry(left_frame)
        self.label_entry.pack(side=tk.LEFT)
        add_label_button = tk.Button(left_frame, text="Add Label", command=self.add_label)
        add_label_button.pack(side=tk.LEFT)
        remove_label_button = tk.Button(left_frame, text="Remove Label", command=self.remove_label)
        remove_label_button.pack(side=tk.LEFT)

        # Canvas for image display
        self.canvas = tk.Canvas(right_frame, width=800, height=600)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<ButtonPress-1>", self.start_annotation)
        self.canvas.bind("<B1-Motion>", self.create_annotation)
        self.canvas.bind("<ButtonRelease-1>", self.end_annotation)

        # Tools frame (on the right side)
        tools_frame = tk.Frame(right_frame)
        tools_frame.pack(side=tk.RIGHT, padx=20)  # Padding to separate tools from the image

        point_button = tk.Button(tools_frame, text="Point", command=lambda: self.select_tool("point"))
        point_button.pack(side=tk.TOP, pady=5)

        rect_button = tk.Button(tools_frame, text="Rectangle", command=lambda: self.select_tool("rectangle"))
        rect_button.pack(side=tk.TOP, pady=5)

        circle_button = tk.Button(tools_frame, text="Circle", command=lambda: self.select_tool("circle"))
        circle_button.pack(side=tk.TOP, pady=5)

        polygon_button = tk.Button(tools_frame, text="Polygon", command=lambda: self.select_tool("polygon"))
        polygon_button.pack(side=tk.TOP, pady=5)

    def load_folder(self):
        self.folder_path = filedialog.askdirectory()
        if not self.folder_path:
            return

        self.image_listbox.delete(0, tk.END)
        self.image_list = [f for f in os.listdir(self.folder_path) if f.endswith(('jpg', 'png'))]
        for img in self.image_list:
            self.image_listbox.insert(tk.END, img)

    def load_image(self, event):
        selected_image = self.image_listbox.get(self.image_listbox.curselection())
        img_path = os.path.join(self.folder_path, selected_image)
        img = Image.open(img_path)
        self.current_image = img
        img.thumbnail((800, 600))  # Resize to fit the canvas
        img_tk = ImageTk.PhotoImage(img)

        self.canvas.image = img_tk  # Keep a reference to avoid garbage collection
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

        # Clear annotations for the new image
        self.annotations.clear()
        self.canvas.delete("annotation")
        self.annotation_listbox.delete(0, tk.END)

    def add_label(self):
        new_label = self.label_entry.get()
        if new_label:
            self.label_listbox.insert(tk.END, new_label)
            self.label_entry.delete(0, tk.END)

    def remove_label(self):
        selected_label_index = self.label_listbox.curselection()
        if selected_label_index:
            self.label_listbox.delete(selected_label_index)

    def select_tool(self, tool):
        self.selected_tool = tool
        messagebox.showinfo("Tool Selected", f"Selected tool: {tool}")

    def start_annotation(self, event):
        if not self.selected_tool or not self.label_listbox.curselection():
            messagebox.showwarning("No Tool or Label", "Please select a tool and label first.")
            return

        self.selected_label = self.label_listbox.get(self.label_listbox.curselection())
        self.annotation_start = (event.x, event.y)

    def create_annotation(self, event):
        # Visual feedback for annotation while dragging
        self.canvas.delete("preview")
        if self.selected_tool == "rectangle":
            self.canvas.create_rectangle(self.annotation_start[0], self.annotation_start[1],
                                         event.x, event.y, outline='red', tags="preview")

    def end_annotation(self, event):
        if self.selected_tool == "rectangle":
            x1, y1 = self.annotation_start
            x2, y2 = event.x, event.y
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', tags="annotation")
            annotation_details = f"Label: {self.selected_label}, Type: rectangle, Coords: [{x1},{y1},{x2},{y2}]"
            self.annotation_listbox.insert(tk.END, annotation_details)
            self.annotations.append({
                "label": self.selected_label,
                "type": "rectangle",
                "coordinates": [x1, y1, x2, y2]
            })
        elif self.selected_tool == "point":
            x, y = event.x, event.y
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='blue', tags="annotation")
            annotation_details = f"Label: {self.selected_label}, Type: point, Coords: [{x},{y}]"
            self.annotation_listbox.insert(tk.END, annotation_details)
            self.annotations.append({
                "label": self.selected_label,
                "type": "point",
                "coordinates": [x, y]
            })

    def save_annotations(self):
        if not self.current_image:
            messagebox.showwarning("No Image", "No image loaded to save annotations.")
            return

        image_name = self.image_listbox.get(self.image_listbox.curselection())
        annotation_file = os.path.join(self.folder_path, f"{image_name}.json")
        with open(annotation_file, "w") as f:
            json.dump(self.annotations, f)
        messagebox.showinfo("Saved", f"Annotations saved for {image_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLabelingTool(root)
    root.mainloop()
