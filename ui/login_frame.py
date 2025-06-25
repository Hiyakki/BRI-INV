# File: ui/login_frame.py
# Berisi kelas untuk membuat UI halaman login sesuai desain Anda.

import customtkinter
from PIL import Image
import os
import database as db # <-- TAMBAHAN: Import yang terlewat

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, login_callback, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.login_callback = login_callback # Fungsi yang akan dipanggil saat tombol 'Masuk' ditekan

        # Konfigurasi grid utama untuk dua panel (1 baris, 2 kolom)
        self.grid_columnconfigure(0, weight=2) # Panel kiri lebih lebar
        self.grid_columnconfigure(1, weight=3) # Panel kanan
        self.grid_rowconfigure(0, weight=1)

        # --- Panel Kiri (Form Login) ---
        self.left_panel = customtkinter.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.left_panel.grid(row=0, column=0, sticky="nsew")

        # Konfigurasi grid di dalam panel kiri agar konten terpusat
        self.left_panel.grid_rowconfigure((0, 4), weight=1)
        self.left_panel.grid_columnconfigure((0, 2), weight=1)
        
        # Path ke folder assets, sekarang bisa menggunakan db.get_base_path()
        assets_path = os.path.join(db.get_base_path(), "assets")

        # Logo BRI INV
        try:
            logo_image = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(assets_path, "logo_bri.png")),
                dark_image=Image.open(os.path.join(assets_path, "logo_bri.png")),
                size=(120, 40) # Sesuaikan ukuran logo
            )
            logo_label = customtkinter.CTkLabel(self.left_panel, image=logo_image, text="")
            logo_label.grid(row=0, column=1, pady=(20, 10), padx=20, sticky="nw")
        except FileNotFoundError:
            logo_label = customtkinter.CTkLabel(self.left_panel, text="BRI INV Logo")
            logo_label.grid(row=0, column=1, pady=(20, 10), padx=20, sticky="nw")


        # Frame untuk menampung form
        form_container = customtkinter.CTkFrame(self.left_panel, fg_color="transparent")
        form_container.grid(row=1, column=1, rowspan=3, sticky="n")

        title_label = customtkinter.CTkLabel(form_container, text="Masuk", text_color="#000000",
                                             font=customtkinter.CTkFont(size=32, weight="bold"))
        title_label.pack(anchor="w", pady=(50, 30))

        # Personal Number
        pn_label = customtkinter.CTkLabel(form_container, text="Personal Number", text_color="#555555",
                                           font=customtkinter.CTkFont(size=14))
        pn_label.pack(anchor="w", pady=(0, 5))
        self.pn_entry = customtkinter.CTkEntry(form_container, width=350, height=45, 
                                               border_color="#DDDDDD", fg_color="#FFFFFF",
                                               text_color="#000000")
        self.pn_entry.pack(pady=(0, 20))

        # Password
        pw_label = customtkinter.CTkLabel(form_container, text="Password", text_color="#555555",
                                           font=customtkinter.CTkFont(size=14))
        pw_label.pack(anchor="w", pady=(0, 5))
        self.pw_entry = customtkinter.CTkEntry(form_container, width=350, height=45, 
                                               border_color="#DDDDDD", fg_color="#FFFFFF",
                                               text_color="#000000", show="*")
        self.pw_entry.pack(pady=(0, 30))
        
        # Bind tombol Enter untuk login
        self.pw_entry.bind("<Return>", self.on_login_button_press)

        # Tombol Masuk
        login_button = customtkinter.CTkButton(form_container, text="Masuk", width=350, height=45,
                                               font=customtkinter.CTkFont(size=16, weight="bold"),
                                               fg_color="#4A55A2", hover_color="#3A4482",
                                               command=self.on_login_button_press)
        login_button.pack()

        # --- Panel Kanan (Logo Besar) ---
        self.right_panel = customtkinter.CTkFrame(self, fg_color="#4A55A2", corner_radius=0)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        # Logo Utama
        try:
            main_logo_image = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(assets_path, "logo_main_blue.png")),
                dark_image=Image.open(os.path.join(assets_path, "logo_main_blue.png")),
                size=(250, 250) # Sesuaikan ukuran logo
            )
            main_logo_label = customtkinter.CTkLabel(self.right_panel, image=main_logo_image, text="")
            main_logo_label.grid(row=0, column=0, pady=20, padx=20)
        except FileNotFoundError:
            main_logo_label = customtkinter.CTkLabel(self.right_panel, text="Logo Utama", font=("Arial", 40))
            main_logo_label.grid(row=0, column=0, pady=20, padx=20)


    def on_login_button_press(self, event=None):
        """Mengambil data dari entry dan memanggil fungsi callback dari master."""
        pn = self.pn_entry.get()
        pw = self.pw_entry.get()
        self.login_callback(pn, pw)
