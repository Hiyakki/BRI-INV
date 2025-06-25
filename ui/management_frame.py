# File: ui/management_frame.py
import tkinter
from tkinter import ttk, messagebox, filedialog
import customtkinter
import database as db
from PIL import Image
import io
import shutil
import uuid
import os
import threading

class ManagementFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Variabel untuk menyimpan ID item & kategori yang dipilih
        self.selected_item_id = None
        self.cat_name_to_id = {} # Untuk mapping nama kategori ke ID

        self.tab_view = customtkinter.CTkTabview(self, anchor="w")
        self.tab_view.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab_view.add("Manajemen Item")
        self.tab_view.add("Manajemen Kategori")
        
        self.setup_item_management_tab()
        self.setup_category_management_tab()

    def refresh_all_tables(self):
        """Fungsi ini dipanggil saat tab Manajemen diaktifkan."""
        self.refresh_cat_table()
        self.refresh_item_manage_table()
        self.refresh_category_combobox()

    def setup_item_management_tab(self):
        tab = self.tab_view.tab("Manajemen Item")
        
        tab.grid_columnconfigure(0, weight=1) 
        tab.grid_columnconfigure(1, weight=3) 
        tab.grid_rowconfigure(0, weight=1)

        form_frame = customtkinter.CTkFrame(tab)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        form_label = customtkinter.CTkLabel(form_frame, text="Form Data Item", font=customtkinter.CTkFont(size=14, weight="bold"))
        form_label.pack(pady=10, padx=10)

        self.item_id_label = customtkinter.CTkLabel(form_frame, text="ID Item: -")
        self.item_id_label.pack(anchor="w", padx=10)
        
        customtkinter.CTkLabel(form_frame, text="Nama Item:").pack(anchor="w", padx=10, pady=(5,0))
        self.item_name_entry = customtkinter.CTkEntry(form_frame)
        self.item_name_entry.pack(fill="x", padx=10)
        
        customtkinter.CTkLabel(form_frame, text="Kategori:").pack(anchor="w", padx=10, pady=(5,0))
        self.item_cat_combobox = customtkinter.CTkComboBox(form_frame, values=[])
        self.item_cat_combobox.pack(fill="x", padx=10)
        self.item_cat_combobox.set("Pilih Kategori")

        customtkinter.CTkLabel(form_frame, text="Stok Awal:").pack(anchor="w", padx=10, pady=(5,0))
        self.item_stock_entry = customtkinter.CTkEntry(form_frame)
        self.item_stock_entry.pack(fill="x", padx=10)
        
        customtkinter.CTkLabel(form_frame, text="Deskripsi:").pack(anchor="w", padx=10, pady=(5,0))
        self.item_desc_textbox = customtkinter.CTkTextbox(form_frame, height=100)
        self.item_desc_textbox.pack(fill="x", padx=10, pady=5)
        
        action_form_frame = customtkinter.CTkFrame(form_frame, fg_color="transparent")
        action_form_frame.pack(fill="x", pady=15, padx=10)
        
        save_button = customtkinter.CTkButton(action_form_frame, text="Simpan", command=self.save_item)
        save_button.pack(side="left", expand=True, padx=(0,5))
        
        clear_button = customtkinter.CTkButton(action_form_frame, text="Bersihkan Form", command=self.clear_item_form, fg_color="#565b5e")
        clear_button.pack(side="left", expand=True, padx=(5,0))

        table_frame = customtkinter.CTkFrame(tab)
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.item_manage_table = ttk.Treeview(table_frame, columns=("ID", "Nama", "Kategori", "Stok"), show="headings")
        self.item_manage_table.heading("ID", text="ID")
        self.item_manage_table.heading("Nama", text="Nama Item")
        self.item_manage_table.heading("Kategori", text="Kategori")
        self.item_manage_table.heading("Stok", text="Stok")
        self.item_manage_table.column("ID", width=40, anchor="center")
        self.item_manage_table.column("Nama", width=200)
        self.item_manage_table.column("Kategori", width=120)
        self.item_manage_table.column("Stok", width=60, anchor="center")
        
        self.item_manage_table.grid(row=0, column=0, sticky="nsew")
        self.item_manage_table.bind("<<TreeviewSelect>>", self.on_item_select)
        
        delete_item_button = customtkinter.CTkButton(table_frame, text="Hapus Item Terpilih", fg_color="#D32F2F", hover_color="#B71C1C", command=self.delete_selected_item)
        delete_item_button.grid(row=1, column=0, pady=10)
        
    def refresh_item_manage_table(self):
        for row in self.item_manage_table.get_children():
            self.item_manage_table.delete(row)
        items = db.get_all_items_with_category()
        if items is None: return
        for item in items:
            self.item_manage_table.insert("", "end", values=(item[0], item[1], item[2] or "Tanpa Kategori", item[3]))
            
    def refresh_category_combobox(self):
        categories = db.get_all_categories()
        if categories is None: return
        self.cat_name_to_id = {name: cat_id for cat_id, name in categories}
        cat_names = [name for _, name in categories]
        self.item_cat_combobox.configure(values=cat_names)
        if not cat_names:
            self.item_cat_combobox.set("Buat kategori dulu")
        else:
            self.item_cat_combobox.set("Pilih Kategori")
            
    def on_item_select(self, event=None):
        selected_row = self.item_manage_table.focus()
        if not selected_row: return
            
        all_items = db.get_all_items_with_category()
        if all_items is None: return
        item_id = self.item_manage_table.item(selected_row, "values")[0]
        
        selected_data = next((item for item in all_items if item[0] == int(item_id)), None)
        if not selected_data: return

        self.clear_item_form()
        
        # (id, name, cat, stock, desc, date, filename)
        self.selected_item_id = selected_data[0]
        self.item_id_label.configure(text=f"ID Item: {self.selected_item_id}")
        self.item_name_entry.insert(0, selected_data[1])
        self.item_cat_combobox.set(selected_data[2] or "Pilih Kategori")
        self.item_stock_entry.insert(0, selected_data[3])
        self.item_desc_textbox.insert("1.0", selected_data[4] or "")
        
    def clear_item_form(self):
        self.selected_item_id = None
        self.item_id_label.configure(text="ID Item: - (Item Baru)")
        self.item_name_entry.delete(0, "end")
        self.item_stock_entry.delete(0, "end")
        self.item_desc_textbox.delete("1.0", "end")
        self.item_cat_combobox.set("Pilih Kategori")
        self.item_name_entry.focus()
        
    def save_item(self):
        name = self.item_name_entry.get()
        desc = self.item_desc_textbox.get("1.0", "end-1c")
        stock_str = self.item_stock_entry.get()
        cat_name = self.item_cat_combobox.get()
        cat_id = self.cat_name_to_id.get(cat_name)

        if not name.strip() or not stock_str.strip():
            messagebox.showerror("Error", "Nama Item dan Stok tidak boleh kosong.")
            return
        try:
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka.")
            return

        if self.selected_item_id:
            db.update_item(self.selected_item_id, name, desc, stock, cat_id)
            messagebox.showinfo("Sukses", "Item berhasil diperbarui.")
        else:
            db.add_item(name, desc, stock, cat_id)
            messagebox.showinfo("Sukses", "Item baru berhasil ditambahkan.")

        self.refresh_item_manage_table()
        self.master.item_list_frame.refresh_item_table()
        self.clear_item_form()
        
    def delete_selected_item(self):
        if not self.selected_item_id:
            messagebox.showwarning("Peringatan", "Pilih item dari tabel untuk dihapus.")
            return
        
        if messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus item ini secara permanen?\nID: {self.selected_item_id}"):
            db.delete_item(self.selected_item_id)
            messagebox.showinfo("Sukses", "Item berhasil dihapus.")
            self.refresh_item_manage_table()
            self.master.item_list_frame.refresh_item_table()
            self.clear_item_form()

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
                self.refresh_all_tables()
                self.cat_name_entry.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menambah kategori, mungkin nama sudah ada.\n{e}")
        else:
            messagebox.showwarning("Peringatan", "Nama kategori tidak boleh kosong.")
            
    def delete_category(self):
        selected_item = self.cat_table.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih kategori untuk dihapus.")
            return
        
        item_values = self.cat_table.item(selected_item, "values")
        cat_id = item_values[0]
        
        if messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus kategori '{item_values[1]}'?\nItem dalam kategori ini tidak akan terhapus, tetapi kategorinya akan dikosongkan."):
            db.delete_category(cat_id)
            self.refresh_all_tables()

    def refresh_cat_table(self):
        for row in self.cat_table.get_children():
            self.cat_table.delete(row)
        categories = db.get_all_categories()
        if categories:
            for cat in categories:
                self.cat_table.insert("", "end", values=cat)
