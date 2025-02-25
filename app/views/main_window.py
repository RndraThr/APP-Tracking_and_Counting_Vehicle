import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import sys
import os
from ..auth.login import verify_password, hash_password
from ..core.detector import VehicleDetector
from ..core.tracker import VehicleTracker
from ..core.counter import VehicleCounter

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Smartcounting v.4")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.video_path = tk.StringVar()
        self.rtsp_url = tk.StringVar()
        self.location_entry = tk.StringVar()
        self.password_entry = tk.StringVar()  
        self._setup_ui()
    
    def _resource_path(self, relative_path):
        """Mendapatkan absolute path untuk resource yang bekerja di development dan executable."""
        try:
            # PyInstaller membuat _MEIPASS jika aplikasi di-bundle
            base_path = getattr(sys, '_MEIPASS', None)
            if base_path:
                return os.path.join(base_path, relative_path)
            
            # Jika bukan PyInstaller, coba beberapa lokasi relatif
            possible_paths = [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', relative_path),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path),
                os.path.join(os.getcwd(), relative_path)
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return path
            
            # Jika tidak ditemukan, gunakan path terakhir
            return possible_paths[0]
            
        except Exception as e:
            print(f"Error in _resource_path: {e}")
            return relative_path
    
    def _create_entry(self, parent, label_text, textvariable, is_password=False):
        """Membuat label dan entry field."""
        label = tk.Label(parent, 
                        text=label_text, 
                        bg="#083c75", 
                        fg="white", 
                        font=("Arial", 12, "bold"))
        label.pack(anchor="w", padx=20, pady=5)
        
        entry = ttk.Entry(parent, 
                         textvariable=textvariable, 
                         font=("Arial", 12),
                         show="*" if is_password else None)
        entry.pack(fill="x", padx=20, pady=5)
        return entry
        
    def _setup_ui(self):
        bg_color = "#eaf4fc"
        form_color = "#083c75"
        self.root.configure(bg=bg_color)
        
        left_frame = tk.Frame(self.root, bg=bg_color)
        left_frame.place(x=0, y=0, width=400, height=500)

        self._setup_logos(left_frame, bg_color)

        right_frame = tk.Frame(self.root, bg=form_color)
        right_frame.place(x=400, y=0, width=400, height=500)
        
        self._setup_form(right_frame, form_color)
    
    def _setup_logos(self, frame, bg_color):
        # Logo pertama
        logo_path = self._resource_path(os.path.join("assets", "logo.png"))
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((100, 115))
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        
        logo_label = tk.Label(frame, image=self.logo_photo, bg=bg_color)
        logo_label.pack(pady=20)
        
        # Judul aplikasi
        app_title = tk.Label(frame, 
                            text="APLIKASI\nSMART COUNTING", 
                            bg=bg_color, 
                            fg="#083c75", 
                            font=("Arial", 20, "bold"), 
                            justify="center")
        app_title.pack()
        
        # Logo kedua
        logo_path2 = self._resource_path(os.path.join("assets", "logo_sc.png"))
        logo_image2 = Image.open(logo_path2)
        logo_image2 = logo_image2.resize((100, 115))
        self.logo_photo2 = ImageTk.PhotoImage(logo_image2)
        
        logo_label2 = tk.Label(frame, image=self.logo_photo2, bg=bg_color)
        logo_label2.pack(pady=20)
    
    def _setup_form(self, frame, form_color):
        form_title = tk.Label(frame, 
                            text="DISHUB BANYUMAS", 
                            bg=form_color, 
                            fg="white", 
                            font=("Arial", 18, "bold"))
        form_title.pack(pady=20)
        btn_browse = ttk.Button(frame, 
                            text="File Video / URL RTSP", 
                            command=self.upload_file)
        btn_browse.pack(fill="x", padx=20, pady=5)
        self._create_entry(frame, "Video Path / RTSP URL:", self.video_path)
        self._create_entry(frame, "Lokasi Survey:", self.location_entry)
        self._create_entry(frame, "Password:", self.password_entry, is_password=True)
        
        submit_button = ttk.Button(frame, text="SUBMIT", command=self.submit)
        submit_button.pack(fill="x", padx=20, pady=20)
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if file_path:
            self.video_path.set(file_path)
    
    def submit(self):
        location = self.location_entry.get()
        password = self.password_entry.get()
        video = self.video_path.get()
        
        if not location or not password:
            messagebox.showerror("Error", "Lokasi Dan Password Harus Diisi")
            return

        test_password = "tes"
        salt, hashed_password = hash_password(test_password)
        
        if verify_password(password, salt, hashed_password):
            self._save_input_data(location, video)
            self.root.withdraw()
            self._start_detection()
        else:
            messagebox.showerror("Error", "Password Salah!!!")
    
    def _save_input_data(self, location, video):
        with open("data_input.txt", "w") as f:
            f.write(f"{location}\n{video}")
        messagebox.showinfo("Sukses", 
                          f"Data terkirim:\nVideo: {video}\nLokasi: {location}")

    def _start_detection(self):
        from .detection_window import DetectionWindow
        detection = DetectionWindow(
            self.video_path.get(),
            self.location_entry.get()
        )
        detection.run()