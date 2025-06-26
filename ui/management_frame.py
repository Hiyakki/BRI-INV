# File: ui/management_frame.py (dengan Implementasi Lengkap)
import tkinter
from tkinter import ttk, messagebox, filedialog
import customtkinter
import database as db
from PIL import Image
import io
import requests
import uuid
import os
import threading
import logging

class ManagementFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Variabel untuk menyimpan ID item & kategori yang dipilih
        self.selected_item_id = None
        self.cat_name_to_id = {}
        self.current_image_url = None
        self.selected_image_path = None # Path gambar baru dari lokal

        self.tab_view = customtkinter.CTkTabview(self, anchor="w")
        self.tab_view.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab_view.add("Manajemen Item")
        self.tab_view.add("Manajemen Kategori")
        
        self.setup_item_management_tab()
        self.setup_category_management_tab()

    def refresh_all_tables(self):
        """Fungsi ini dipanggil saat tab Manajemen diaktifkan."""
        self.refresh_item_manage_table()
        self.refresh_cat_table()
        self.refresh_category_combobox()

    def setup_item_management_tab(self):
        tab = self.tab_view.tab("Manajemen Item")
        tab.grid_columnconfigure(0, weight=1) 
        tab.grid_columnconfigure(1, weight=3) 
        tab.grid_rowconfigure(0, weight=1)

        # --- Form Frame (Sebelah Kiri) ---
        form_frame = customtkinter.CTkFrame(tab)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        form_scrollable = customtkinter.CTkScrollableFrame(form_frame, label_text="Form Data Item")
        form_scrollable.pack(expand=True, fill="both")

        self.item_id_label = customtkinter.CTkLabel(form_scrollable, text="ID Item: -")
        self.item_id_label.pack(anchor="w", padx=10, pady=(5,0))
        
        customtkinter.CTkLabel(form_scrollable, text="Nama Item:").pack(anchor="w", padx=10, pady=(5,0))
        self.item_name_entry = customtkinter.CTkEntry(form_scrollable)
        self.item_name_entry.pack(fill="x", padx=10)
        
        customtkinter.CTkLabel(form_scrollable, text="Kategori:").pack(anchor="w", padx=10, pady=(5,0))
        self.item_cat_combobox = customtkinter.CTkComboBox(form_scrollable, values=[])
        self.item_cat_combobox.pack(fill="x", padx=10)
        
        customtkinter.CTkLabel(form_scrollable, text="Stok Awal:").pack(anchor="w", padx=10, pady=(5,0))
        self.item_stock_entry = customtkinter.CTkEntry(form_scrollable)
        self.item_stock_entry.pack(fill="x", padx=10)
        
        customtkinter.CTkLabel(form_scrollable, text="Deskripsi:").pack(anchor="w", padx=10, pady=(5,0))
        self.item_desc_textbox = customtkinter.CTkTextbox(form_scrollable, height=100)
        self.item_desc_textbox.pack(fill="x", padx=10, pady=5)

        self.image_preview_label = customtkinter.CTkLabel(form_scrollable, text="Tidak ada gambar", width=200, height=150)
        self.image_preview_label.pack(pady=5, padx=10, expand=True)
        browse_image_button = customtkinter.CTkButton(form_scrollable, text="Pilih Gambar...", command=self.browse_for_image)
        browse_image_button.pack(pady=(0, 10), padx=10)
        
        action_form_frame = customtkinter.CTkFrame(form_scrollable, fg_color="transparent")
        action_form_frame.pack(fill="x", pady=10, padx=10)
        save_button = customtkinter.CTkButton(action_form_frame, text="Simpan", command=self.save_item)
        save_button.pack(side="left", expand=True, padx=(0,5))
        clear_button = customtkinter.CTkButton(action_form_frame, text="Bersihkan Form", command=self.clear_item_form, fg_color="#565b5e")
        clear_button.pack(side="left", expand=True, padx=(5,0))
        
        delete_item_button = customtkinter.CTkButton(form_scrollable, text="Hapus Item Terpilih", fg_color="#D32F2F", hover_color="#B71C1C", command=self.delete_selected_item)
        delete_item_button.pack(fill="x", pady=(5,10), padx=10)

        # --- Tampilan Kartu Item (Sebelah Kanan) ---
        display_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        display_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        self.item_scrollable_frame = customtkinter.CTkScrollableFrame(display_frame, label_text="Pilih Item untuk Diedit")
        self.item_scrollable_frame.pack(expand=True, fill="both")
        self.item_scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def refresh_item_manage_table(self):
        for widget in self.item_scrollable_frame.winfo_children():
            widget.destroy()
        items = db.get_all_items_with_category()
        if not items:
            customtkinter.CTkLabel(self.item_scrollable_frame, text="Belum ada item.").pack(pady=20)
            return
        for i, item_data in enumerate(items):
            row, column = i // 4, i % 4
            self.create_item_card(item_data, row, column)
            
    def create_item_card(self, item_data, row, column):
        item_name, stock = item_data[1], item_data[3]
        card = customtkinter.CTkFrame(self.item_scrollable_frame, border_width=1, border_color="gray70")
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(0, weight=1)
        card_button = customtkinter.CTkButton(card, text=f"{item_name}\nStok: {stock}",
                                              font=customtkinter.CTkFont(size=14),
                                              command=lambda data=item_data: self.on_item_select(data),
                                              fg_color="gray20", hover_color="gray30")
        card_button.grid(row=0, column=0, sticky="nsew", ipady=40)

    def on_item_select(self, selected_data):
        self.clear_item_form()
        self.selected_item_id = selected_data[0]
        self.item_id_label.configure(text=f"ID Item: {self.selected_item_id}")
        self.item_name_entry.insert(0, selected_data[1])
        self.item_cat_combobox.set(selected_data[2] or "Pilih Kategori")
        self.item_stock_entry.insert(0, str(selected_data[3]))
        self.item_desc_textbox.insert("1.0", selected_data[4] or "")
        self.current_image_url = selected_data[6]
        self.image_preview_label.configure(image=None, text="Memuat gambar...")
        if self.current_image_url:
            threading.Thread(target=self.load_image_from_url, args=(self.current_image_url,)).start()
        else:
            self.image_preview_label.configure(text="Tidak ada gambar")

    def browse_for_image(self):
        path = filedialog.askopenfilename(filetypes=(("Image Files", "*.jpg *.jpeg *.png"), ("All files", "*.*")))
        if path:
            self.selected_image_path = path
            try:
                img = Image.open(path)
                ctk_img = customtkinter.CTkImage(light_image=img, size=(200, 150))
                self.image_preview_label.configure(image=ctk_img, text="")
            except Exception as e:
                self.image_preview_label.configure(image=None, text="Gagal memuat pratinjau")

    def upload_image(self, image_path):
        IMGBB_API_KEY = "GANTI_DENGAN_API_KEY_ANDA"
        url = "https://api.imgbb.com/1/upload"
        try:
            with open(image_path, "rb") as file:
                payload = {"key": IMGBB_API_KEY}
                response = requests.post(url, params=payload, files={"image": file})
                response.raise_for_status()
                result = response.json()
                if result.get("success"):
                    return result["data"]["url"]
                else:
                    messagebox.showerror("Upload Gagal", f"API Error: {result.get('error', {}).get('message', 'Unknown')}")
                    return None
        except Exception as e:
            messagebox.showerror("Upload Gagal", f"Error: {e}")
            return None

    def load_image_from_url(self, url):
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            img = Image.open(io.BytesIO(response.content))
            ctk_img = customtkinter.CTkImage(light_image=img, size=(200, 150))
            self.image_preview_label.configure(image=ctk_img, text="")
        except Exception as e:
            self.image_preview_label.configure(image=None, text="Gagal memuat gambar")

    def save_item(self):
        name = self.item_name_entry.get()
        desc = self.item_desc_textbox.get("1.0", "end-1c")
        stock_str = self.item_stock_entry.get()
        cat_name = self.item_cat_combobox.get()
        cat_id = self.cat_name_to_id.get(cat_name)
        image_url_to_save = self.current_image_url

        if self.selected_image_path:
            messagebox.showinfo("Proses", "Mengunggah gambar...")
            self.update_idletasks()
            new_url = self.upload_image(self.selected_image_path)
            if new_url:
                image_url_to_save = new_url
            else:
                return

        if not name.strip() or not stock_str.strip():
            messagebox.showerror("Error", "Nama Item dan Stok wajib diisi.")
            return
        try:
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka.")
            return

        if self.selected_item_id:
            db.update_item(self.selected_item_id, name, desc, stock, cat_id, image_url_to_save)
            messagebox.showinfo("Sukses", "Item berhasil diperbarui.")
        else:
            db.add_item(name, desc, stock, cat_id, image_url_to_save)
            messagebox.showinfo("Sukses", "Item baru berhasil ditambahkan.")

        self.master.item_list_frame.refresh_item_table()
        self.refresh_all_tables()
        self.clear_item_form()

    def delete_selected_item(self):
        if not self.selected_item_id:
            messagebox.showwarning("Peringatan", "Pilih item untuk dihapus.")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus item ini?"):
            db.delete_item(self.selected_item_id)
            messagebox.showinfo("Sukses", "Item berhasil dihapus.")
            self.master.item_list_frame.refresh_item_table()
            self.refresh_all_tables()
            self.clear_item_form()

    def refresh_category_combobox(self):
        categories = self.master.category_cache if self.master.category_cache else db.get_all_categories()
        self.master.category_cache = categories
        if categories:
            self.cat_name_to_id = {name: cat_id for cat_id, name in categories}
            self.item_cat_combobox.configure(values=[name for _, name in categories])
        else:
            self.item_cat_combobox.configure(values=[])
        self.item_cat_combobox.set("Pilih Kategori" if self.item_cat_combobox.cget("values") else "Buat kategori dulu")

    def clear_item_form(self):
        self.selected_item_id = None
        self.current_image_url = None
        self.selected_image_path = None
        self.item_id_label.configure(text="ID Item: - (Item Baru)")
        self.item_name_entry.delete(0, "end")
        self.item_stock_entry.delete(0, "end")
        self.item_desc_textbox.delete("1.0", "end")
        self.item_cat_combobox.set("Pilih Kategori")
        self.image_preview_label.configure(image=None, text="Tidak ada gambar")
        self.item_name_entry.focus()

    def setup_category_management_tab(self):
        tab = self.tab_view.tab("Manajemen Kategori")
        form_frame = customtkinter.CTkFrame(tab)
        form_frame.pack(fill="x", padx=10, pady=10)
        label_cat = customtkinter.CTkLabel(form_frame, text="Nama Kategori:")
        label_cat.pack(side="left", padx=10)
        self.cat_name_entry = customtkinter.CTkEntry(form_frame, width=300)
        self.cat_name_entry.pack(side="left", padx=10)
        add_cat_button = customtkinter.CTkButton(form_frame, text="Tambah Kategori", command=self.add_category)
        add_cat_button.pack(side="left", padx=10)
        self.cat_table = ttk.Treeview(tab, columns=("ID", "Nama"), show="headings")
        self.cat_table.heading("ID", text="ID Kategori")
        self.cat_table.heading("Nama", text="Nama Kategori")
        self.cat_table.pack(expand=True, fill="both", padx=10, pady=10)
        action_frame = customtkinter.CTkFrame(tab)
        action_frame.pack(fill="x", padx=10, pady=10)
        del_cat_button = customtkinter.CTkButton(action_frame, text="Hapus Terpilih", fg_color="#D32F2F", hover_color="#B71C1C", command=self.delete_category)
        del_cat_button.pack(side="right", padx=10)

    def add_category(self):
        cat_name = self.cat_name_entry.get()
        if cat_name.strip():
            try:
                db.add_category(cat_name)
                self.master.category_cache = None
                self.refresh_all_tables()
                self.cat_name_entry.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menambah kategori.\n{e}")
        else:
            messagebox.showwarning("Peringatan", "Nama kategori tidak boleh kosong.")

    def delete_category(self):
        selected_item = self.cat_table.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih kategori untuk dihapus.")
            return
        item_values = self.cat_table.item(selected_item, "values")
        cat_id = item_values[0]
        if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus kategori '{item_values[1]}'?"):
            db.delete_category(cat_id)
            self.master.category_cache = None
            self.refresh_all_tables()

    def refresh_cat_table(self):
        for row in self.cat_table.get_children():
            self.cat_table.delete(row)
        self.refresh_category_combobox()
        categories = self.master.category_cache
        if categories:
            for cat in categories:
                self.cat_table.insert("", "end", values=cat)
