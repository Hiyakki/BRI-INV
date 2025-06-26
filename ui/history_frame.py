# File: ui/history_frame.py (dengan Fitur Dropdown Kalender)
import tkinter
from tkinter import ttk, messagebox, filedialog
import customtkinter
import database as db
import pandas as pd
import datetime
from tkcalendar import DateEntry # <-- Import baru untuk kalender

class HistoryFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Konfigurasi grid agar frame bisa membesar
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Ubah ke row 2 untuk tabel

        # --- FRAME BARU UNTUK FILTER DAN EKSPOR ---
        top_frame = customtkinter.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")

        label = customtkinter.CTkLabel(top_frame, text="Histori Pengambilan Barang", font=customtkinter.CTkFont(size=16, weight="bold"))
        label.pack(side="left", padx=10, pady=10)
        
        # Spacer
        top_frame.pack_propagate(False)

        # --- WIDGET FILTER TANGGAL DENGAN KALENDER ---
        filter_frame = customtkinter.CTkFrame(self)
        filter_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        customtkinter.CTkLabel(filter_frame, text="Dari Tanggal:").pack(side="left", padx=(10,5))
        
        # Widget Kalender untuk Tanggal Mulai
        self.start_date_entry = DateEntry(filter_frame, 
                                          date_pattern='y-mm-dd', 
                                          width=12,
                                          background='#4A55A2', # Warna biru BRI
                                          foreground='white',
                                          borderwidth=2,
                                          selectbackground='#4A55A2',
                                          font=('Inter', 12))
        self.start_date_entry.pack(side="left", padx=5, pady=5)

        customtkinter.CTkLabel(filter_frame, text="Sampai Tanggal:").pack(side="left", padx=(20,5))
        
        # Widget Kalender untuk Tanggal Akhir
        self.end_date_entry = DateEntry(filter_frame, 
                                        date_pattern='y-mm-dd', 
                                        width=12,
                                        background='#4A55A2',
                                        foreground='white',
                                        borderwidth=2,
                                        selectbackground='#4A55A2',
                                        font=('Inter', 12))
        self.end_date_entry.pack(side="left", padx=5, pady=5)
        
        self.filter_button = customtkinter.CTkButton(filter_frame, text="Filter", width=100, command=self.refresh_history_table)
        self.filter_button.pack(side="left", padx=10)

        self.export_button = customtkinter.CTkButton(filter_frame, text="Export ke Excel", fg_color="#107C41", hover_color="#0B532B", command=self.export_to_excel)
        self.export_button.pack(side="right", padx=10)

        # --- Membuat Treeview (Tabel) ---
        # (Styling untuk Treeview tetap sama)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.history_table = ttk.Treeview(self, columns=("Tanggal", "Nama Barang", "Jumlah", "Pengambil"), show="headings")
        self.history_table.heading("Tanggal", text="Tanggal Pengambilan")
        self.history_table.heading("Nama Barang", text="Nama Barang")
        self.history_table.heading("Jumlah", text="Jumlah")
        self.history_table.heading("Pengambil", text="Nama Pengambil")
        self.history_table.column("Tanggal", width=170)
        self.history_table.column("Nama Barang", width=250)
        self.history_table.column("Jumlah", width=100, anchor="center")
        self.history_table.column("Pengambil", width=200)
        self.history_table.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def refresh_history_table(self):
        """Mengambil data histori, bisa dengan filter tanggal, dan menampilkannya."""
        # .get() pada DateEntry akan mengembalikan string tanggal 'YYYY-MM-DD'
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        for row in self.history_table.get_children():
            self.history_table.delete(row)
        
        # Jika kedua tanggal diisi, filter. Jika tidak, tampilkan semua.
        if start_date and end_date:
            history_logs = db.get_history_by_date_range(start_date, end_date)
        else:
            history_logs = db.get_history()
        
        if history_logs is None: return
        
        for log in history_logs:
            item_name = log[1] or "ITEM TELAH DIHAPUS"
            self.history_table.insert("", "end", values=(log[0], item_name, log[2], log[3]))

    def export_to_excel(self):
        """Mengambil data sesuai filter dan mengekspornya ke file Excel."""
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not (start_date and end_date):
            messagebox.showerror("Error", "Harap pilih 'Dari Tanggal' dan 'Sampai Tanggal' untuk mengekspor.")
            return
            
        # Ambil data dari database
        data_to_export = db.get_history_by_date_range(start_date, end_date)

        if not data_to_export:
            messagebox.showinfo("Kosong", "Tidak ada data histori ditemukan pada rentang tanggal tersebut.")
            return
            
        # Meminta pengguna lokasi untuk menyimpan file
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Workbook", "*.xlsx"), ("All Files", "*.*")],
                title="Simpan Laporan Histori",
                initialfile=f"Laporan Histori {start_date} sampai {end_date}.xlsx"
            )

            if not filename:
                return # Pengguna membatalkan dialog simpan

            # Buat DataFrame pandas dari data
            df = pd.DataFrame(data_to_export, columns=["Tanggal Pengambilan", "Nama Barang", "Jumlah", "Nama Pengambil"])
            
            # Ekspor DataFrame ke file Excel
            df.to_excel(filename, index=False)
            
            messagebox.showinfo("Berhasil", f"Data berhasil diekspor ke:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Ekspor Gagal", f"Terjadi error saat mengekspor file:\n{e}")
