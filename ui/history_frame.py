# File: ui/history_frame.py
import tkinter
from tkinter import ttk
import customtkinter
import database as db

class HistoryFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Konfigurasi grid agar frame bisa membesar
        # Baris self.pack() dihapus karena menyebabkan konflik dengan .grid() di file app.py
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        label = customtkinter.CTkLabel(self, text="Histori Pengambilan Barang", font=customtkinter.CTkFont(size=16, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
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

        self.history_table = ttk.Treeview(self, columns=("Tanggal", "Nama Barang", "Jumlah", "Pengambil"), show="headings")
        self.history_table.heading("Tanggal", text="Tanggal Pengambilan")
        self.history_table.heading("Nama Barang", text="Nama Barang")
        self.history_table.heading("Jumlah", text="Jumlah")
        self.history_table.heading("Pengambil", text="Nama Pengambil")
        
        self.history_table.column("Tanggal", width=170)
        self.history_table.column("Nama Barang", width=250)
        self.history_table.column("Jumlah", width=100, anchor="center")
        self.history_table.column("Pengambil", width=200)
        
        self.history_table.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    def refresh_history_table(self):
        """Mengambil data histori terbaru dari database dan menampilkannya di tabel."""
        # Hapus data lama
        for row in self.history_table.get_children():
            self.history_table.delete(row)
        
        # Ambil data baru
        history_logs = db.get_history()
        
        # Mencegah error jika koneksi gagal dan tidak ada data yang dikembalikan
        if history_logs is None: 
            return
        
        # Masukkan data baru ke tabel
        for log in history_logs:
            # log format: (date_taken, item_name, quantity_taken, taker_name)
            # Menangani jika item sudah dihapus (item_name akan menjadi None/NULL)
            item_name = log[1] or "ITEM TELAH DIHAPUS"
            self.history_table.insert("", "end", values=(log[0], item_name, log[2], log[3]))
