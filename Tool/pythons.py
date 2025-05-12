# Face and Signature Detection Tool using Tkinter

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import magic
import os

class ForensicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Forensics - Face and Signature Detection")

        self.label = tk.Label(root, text="Upload an Image for Analysis")
        self.label.pack(pady=10)

        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=5)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.result_text = tk.Text(root, height=10, width=60)
        self.result_text.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            # Display image
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

            # Signature Detection
            signature = self.detect_signature(file_path)

            # Face Detection
            face_result = self.detect_faces(file_path)

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"File Signature Info:\n{signature}\n\nFace Detection Result:\n{face_result}")

    def detect_signature(self, path):
        try:
            file_type = magic.from_file(path, mime=True)
            file_info = magic.from_file(path)
            return f"MIME Type: {file_type}\nDetails: {file_info}"
        except Exception as e:
            return f"Error detecting file signature: {e}"

    def detect_faces(self, path):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        return f"Faces detected: {len(faces)}"

if __name__ == '__main__':
    root = tk.Tk()
    app = ForensicsApp(root)
    root.mainloop()
