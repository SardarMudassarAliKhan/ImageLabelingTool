import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import json

class ImageLabelingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Mudassar Ali Solution - Image Labeling Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")
        
        self.folder_path = ""
        self.image_list = []
        self.current_image = None
        self.annotations = []
        self.selected_tool = None
        self.selected_label = None

        self.init_gui()

    def init_gui(self):
        menu = tk.Menu(self.root, bg="#333333", fg="#ffffff")
        self.root.config(menu=menu)
        
        menu.add_cascade(label="Mudassar Ali Solution", background="#333333", foreground="#ffffff")

        file_menu = tk.Menu(menu, bg="#333333", fg="#ffffff")
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Folder", command=self.load_folder, background="#444444", foreground="#ffffff")
        file_menu.add_command(label="Save Annotations", command=self.save_annotations, background="#444444", foreground="#ffffff")

        left_frame = tk.Frame(self.root, bg="#1e1e1e", padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky=tk.N, padx=10, pady=10)

        right_frame = tk.Frame(self.root, bg="#1e1e1e", padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky=tk.N, padx=10, pady=10)

        annotation_frame = tk.LabelFrame(left_frame, text="Annotations", font=("Arial", 12, "bold"), bg="#2d2d2d", fg="#ffffff", padx=10, pady=10, relief=tk.GROOVE)
        annotation_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.annotation_listbox = tk.Listbox(annotation_frame, height=10, width=40, font=("Arial", 10), bg="#333333", fg="#ffffff", relief=tk.SUNKEN)
        self.annotation_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        image_frame = tk.LabelFrame(left_frame, text="Images", font=("Arial", 12, "bold"), bg="#2d2d2d", fg="#ffffff", padx=10, pady=10, relief=tk.GROOVE)
        image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.image_listbox = tk.Listbox(image_frame, height=10, width=40, font=("Arial", 10), bg="#333333", fg="#ffffff", relief=tk.SUNKEN)
        self.image_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.image_listbox.bind('<<ListboxSelect>>', self.load_image)

        label_frame = tk.LabelFrame(left_frame, text="Labels", font=("Arial", 12, "bold"), bg="#2d2d2d", fg="#ffffff", padx=10, pady=10, relief=tk.GROOVE)
        label_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.label_listbox = tk.Listbox(label_frame, height=10, width=40, font=("Arial", 10), bg="#333333", fg="#ffffff", relief=tk.SUNKEN)
        self.label_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label_entry = tk.Entry(label_frame, font=("Arial", 10), relief=tk.SUNKEN, bg="#333333", fg="#ffffff")
        self.label_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        add_label_button = tk.Button(label_frame, text="Add Label", command=self.add_label, bg="#007bff", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED)
        add_label_button.pack(side=tk.LEFT, padx=5)
        
        remove_label_button = tk.Button(label_frame, text="Remove Label", command=self.remove_label, bg="#dc3545", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED)
        remove_label_button.pack(side=tk.LEFT, padx=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#1e1e1e")
        self.canvas_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=600, bg="#2d2d2d", relief=tk.SUNKEN)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.start_annotation)
        self.canvas.bind("<B1-Motion>", self.create_annotation)
        self.canvas.bind("<ButtonRelease-1>", self.end_annotation)

        tools_frame = tk.LabelFrame(right_frame, text="Tools", font=("Arial", 12, "bold"), bg="#2d2d2d", fg="#ffffff", padx=10, pady=10, relief=tk.GROOVE)
        tools_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        point_button = tk.Button(tools_frame, text="Point", command=lambda: self.select_tool("point"), bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED)
        point_button.pack(side=tk.TOP, pady=5)

        rect_button = tk.Button(tools_frame, text="Rectangle", command=lambda: self.select_tool("rectangle"), bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED)
        rect_button.pack(side=tk.TOP, pady=5)

        circle_button = tk.Button(tools_frame, text="Circle", command=lambda: self.select_tool("circle"), bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED)
        circle_button.pack(side=tk.TOP, pady=5)

        polygon_button = tk.Button(tools_frame, text="Polygon", command=lambda: self.select_tool("polygon"), bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED)
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
        img.thumbnail((800, 600))
        img_tk = ImageTk.PhotoImage(img)

        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

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
        self.canvas.delete("preview")
        if self.selected_tool == "rectangle":
            self.canvas.create_rectangle(self.annotation_start[0], self.annotation_start[1],
                                         event.x, event.y, outline='red', tags="preview")

    def end_annotation(self, event):
        if self.selected_tool == "rectangle":
            annotation = {
                "label": self.selected_label,
                "type": self.selected_tool,
                "coords": (self.annotation_start[0], self.annotation_start[1], event.x, event.y)
            }
            self.annotations.append(annotation)
            self.annotation_listbox.insert(tk.END, f"{self.selected_label}: Rectangle at {annotation['coords']}")
            self.canvas.create_rectangle(self.annotation_start[0], self.annotation_start[1],
                                         event.x, event.y, outline='red', tags="annotation")

    def save_annotations(self):
        if not self.current_image:
            messagebox.showwarning("No Image", "Please load an image first.")
            return

        image_name = os.path.basename(self.current_image.filename)
        annotation_file = os.path.join(self.folder_path, f"{image_name}.json")

        with open(annotation_file, 'w') as f:
            json.dump(self.annotations, f, indent=4)

        messagebox.showinfo("Saved", f"Annotations saved to {annotation_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLabelingTool(root)
    root.mainloop()
