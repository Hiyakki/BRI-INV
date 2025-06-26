# File: ui/item_frame.py (Versi Baru dengan Filter Kategori)
import tkinter
from tkinter import ttk, messagebox
import customtkinter
import database as db
from PIL import Image
import io
import requests
import threading
import logging

class ItemFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Row 2 untuk area scroll

        # --- Judul Halaman ---
        self.title_label = customtkinter.CTkLabel(self, text="Daftar Semua Item", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # --- Frame untuk Filter Kategori ---
        self.filter_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.filter_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # --- Frame Konten yang Bisa di-scroll ---
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Item Tersedia")
        self.scrollable_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1) # 5 kolom

        # --- Inisialisasi awal ---
        self.setup_category_filters()
        self.display_items() # Tampilkan semua item saat pertama kali dibuka

    def setup_category_filters(self):
        """Membuat tombol filter untuk setiap kategori."""
        # Hapus filter lama jika ada
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        # Tombol "Semua"
        all_button = customtkinter.CTkButton(self.filter_frame, text="Semua", 
                                              command=lambda: self.display_items(category_id=None))
        all_button.pack(side="left", padx=5, pady=5)

        # Tombol untuk setiap kategori dari DB
        categories = db.get_all_categories()
        if categories:
            for cat_id, cat_name in categories:
                # 'c_id=cat_id' diperlukan agar lambda menangkap nilai yang benar
                button = customtkinter.CTkButton(self.filter_frame, text=cat_name, 
                                                 command=lambda c_id=cat_id: self.display_items(category_id=c_id))
                button.pack(side="left", padx=5, pady=5)

    def display_items(self, category_id=None):
        """Menghapus item lama dan menampilkan item baru berdasarkan filter."""
        # Hapus semua kartu item yang ada
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Ambil data dari database
        if category_id is None:
            items = db.get_all_items_with_category()
            self.scrollable_frame.configure(label_text="Semua Item Tersedia")
        else:
            items = db.get_items_by_category(category_id)
            # Dapatkan nama kategori untuk judul
            # (Ini bisa dioptimalkan, tapi sudah cukup untuk sekarang)
            all_categories = db.get_all_categories()
            cat_name = next((name for c_id, name in all_categories if c_id == category_id), "Kategori")
            self.scrollable_frame.configure(label_text=f"Item dalam Kategori: {cat_name}")

        if items is None or not items:
            no_item_label = customtkinter.CTkLabel(self.scrollable_frame, text="Tidak ada item untuk ditampilkan.", font=("Inter", 16))
            no_item_label.pack(pady=50)
            return

        # Buat kartu untuk setiap item
        for i, item_data in enumerate(items):
            row = i // 5
            column = i % 5
            self.create_item_card(item_data, row, column)

    def create_item_card(self, item_data, row, column):
        """Membuat satu kartu UI untuk sebuah item."""
        # item_data format: (id, name, cat_name, stock, desc, date_added, image_url)
        item_id, item_name, _, stock, _, _, image_url = item_data

        card = customtkinter.CTkFrame(self.scrollable_frame, border_width=1, border_color="gray70")
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        card.grid_rowconfigure(0, weight=3) # Area gambar
        card.grid_rowconfigure(1, weight=1) # Area teks
        card.grid_columnconfigure(0, weight=1)

        # Label untuk gambar
        image_label = customtkinter.CTkLabel(card, text="Memuat...", height=140, fg_color="gray30")
        image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Memuat gambar di thread terpisah agar UI tidak freeze
        if image_url:
            thread = threading.Thread(target=self.load_image_from_url, args=(image_url, image_label))
            thread.start()
        else:
            image_label.configure(text="Tidak ada\ngambar")

        # Frame untuk teks di bawah gambar
        text_frame = customtkinter.CTkFrame(card, fg_color="transparent")
        text_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_columnconfigure(1, weight=0)

        # Nama item
        name_label = customtkinter.CTkLabel(text_frame, text=item_name, font=customtkinter.CTkFont(weight="bold"))
        name_label.grid(row=0, column=0, sticky="w")
        
        # Stok
        stock_label = customtkinter.CTkLabel(text_frame, text=f"{stock}", fg_color="#4A55A2", corner_radius=6)
        stock_label.grid(row=0, column=1, sticky="e", padx=(5,0))
    
    def load_image_from_url(self, url, image_label):
        """Mengunduh gambar dari URL dan menampilkannya di CTkLabel."""
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            image_data = response.content
            
            img = Image.open(io.BytesIO(image_data))
            ctk_img = customtkinter.CTkImage(light_image=img, size=(180, 140))
            image_label.configure(image=ctk_img, text="")
        except Exception as e:
            logging.warning(f"Gagal memuat gambar dari URL {url}: {e}")
            image_label.configure(image=None, text="Gagal memuat\ngambar")

    def refresh_item_table(self):
        """Nama fungsi ini dipertahankan untuk kompatibilitas, tapi sekarang memanggil display_items."""
        self.setup_category_filters()
        self.display_items()
