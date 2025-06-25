# File: ui/item_frame.py
import tkinter
from tkinter import ttk, messagebox
import customtkinter
import database as db

class ItemFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Label dan tombol
        label = customtkinter.CTkLabel(self, text="Daftar Semua Item", font=customtkinter.CTkFont(size=16, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        take_item_button = customtkinter.CTkButton(self, text="Ambil Item Terpilih", command=self.open_take_item_window)
        take_item_button.grid(row=0, column=0, padx=20, pady=10, sticky="e")
        
        # Membuat Treeview (Tabel)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        self.item_table = ttk.Treeview(self, columns=("ID", "Nama", "Kategori", "Stok", "Deskripsi"), show="headings")
        self.item_table.heading("ID", text="ID")
        self.item_table.heading("Nama", text="Nama Item")
        self.item_table.heading("Kategori", text="Kategori")
        self.item_table.heading("Stok", text="Stok")
        self.item_table.heading("Deskripsi", text="Deskripsi")

        # Atur lebar kolom
        self.item_table.column("ID", width=50, anchor="center")
        self.item_table.column("Nama", width=200)
        self.item_table.column("Kategori", width=150)
        self.item_table.column("Stok", width=80, anchor="center")
        self.item_table.column("Deskripsi", width=300)

        self.item_table.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
    def refresh_item_table(self):
        # Hapus data lama
        for row in self.item_table.get_children():
            self.item_table.delete(row)
        # Ambil data baru dan masukkan ke tabel
        items = db.get_all_items_with_category()
        if items is None: return # Mencegah error jika koneksi gagal
        for item in items:
            # item format: (item_id, item_name, category_name, stock, description, date_added, ...)
            self.item_table.insert("", "end", values=(item[0], item[1], item[2] or "Tanpa Kategori", item[3], item[4]))
            
    def open_take_item_window(self):
        selected_item = self.item_table.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih item yang ingin diambil terlebih dahulu.")
            return

        item_values = self.item_table.item(selected_item, "values")
        item_id = item_values[0]
        item_name = item_values[1]
        current_stock = int(item_values[3])

        take_window = customtkinter.CTkToplevel(self)
        take_window.title(f"Ambil Item: {item_name}")
        take_window.geometry("400x300")
        take_window.transient(self)
        
        label_info = customtkinter.CTkLabel(take_window, text=f"Stok saat ini: {current_stock}")
        label_info.pack(pady=10)
        
        label_qty = customtkinter.CTkLabel(take_window, text="Jumlah yang diambil:")
        label_qty.pack()
        qty_entry = customtkinter.CTkEntry(take_window)
        qty_entry.pack()
        
        label_name = customtkinter.CTkLabel(take_window, text="Nama Pengambil:")
        label_name.pack(pady=(10,0))
        name_entry = customtkinter.CTkEntry(take_window)
        name_entry.pack()
        
        def confirm_take():
            try:
                quantity = int(qty_entry.get())
                taker_name = name_entry.get()
                
                if not taker_name.strip():
                    messagebox.showerror("Error", "Nama pengambil tidak boleh kosong.")
                    return
                if quantity <= 0:
                    messagebox.showerror("Error", "Jumlah harus lebih dari 0.")
                    return
                if quantity > current_stock:
                    messagebox.showerror("Error", f"Jumlah pengambilan ({quantity}) melebihi stok ({current_stock}).")
                    return

                if db.take_item(item_id, quantity, taker_name):
                    messagebox.showinfo("Sukses", f"{quantity} {item_name} berhasil diambil.")
                    self.refresh_item_table()
                    take_window.destroy()
                else:
                    messagebox.showerror("Gagal", "Terjadi kesalahan saat memperbarui database.")

            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa angka.")

        confirm_button = customtkinter.CTkButton(take_window, text="Konfirmasi Pengambilan", command=confirm_take)
        confirm_button.pack(pady=20)
