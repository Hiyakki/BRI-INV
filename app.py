# File: app.py (Versi Baru dengan Alur Login dari Frame)
import tkinter
from tkinter import ttk, messagebox
import customtkinter
import database as db # <-- DIPINDAHKAN KE ATAS agar bisa diakses semua kelas
import os

# Import kelas-kelas Frame dari folder 'ui'
from ui.login_frame import LoginFrame
from ui.item_frame import ItemFrame
from ui.management_frame import ManagementFrame
from ui.history_frame import HistoryFrame

# Pengaturan dasar CustomTkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Manajemen Inventaris")
        self.geometry("1100x650") # Sedikit lebih besar untuk UI baru
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Hapus blok debug pop-up jika sudah tidak diperlukan
        
        self.current_frame = None # Untuk melacak frame yang sedang tampil
        self.show_login_screen()

    def show_login_screen(self):
        """Menampilkan halaman login."""
        # Hapus frame lama jika ada
        if self.current_frame:
            self.current_frame.destroy()
        
        # Buat dan tampilkan LoginFrame
        self.current_frame = LoginFrame(self, login_callback=self.attempt_login)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def attempt_login(self, personal_number, password):
        """Mencoba memvalidasi login dan menampilkan aplikasi utama jika berhasil."""
        if db.validate_admin(personal_number, password):
            messagebox.showinfo("Login Sukses", "Selamat datang, Admin!")
            self.show_main_app()
        else:
            messagebox.showerror("Login Gagal", "Personal Number atau Password salah.")
    
    def show_main_app(self):
        """Membuat dan menampilkan UI aplikasi utama setelah login berhasil."""
        # Hapus frame login
        if self.current_frame:
            self.current_frame.destroy()

        # --- Buat UI Utama di sini ---
        # Membuat Grid Layout (1x2)
        self.grid_columnconfigure(0, weight=0) # Sidebar tidak membesar
        self.grid_columnconfigure(1, weight=1) # Konten membesar
        self.grid_rowconfigure(0, weight=1)

        # --- Frame Navigasi (Sidebar) ---
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # (Tempel semua kode untuk membuat navigation_frame, tombol-tombolnya, dll di sini...)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Menu Utama",
                                                             font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.item_list_button = customtkinter.CTkButton(self.navigation_frame, text="Daftar Item",
                                                        command=lambda: self.select_frame_by_name("items"))
        self.item_list_button.grid(row=1, column=0, padx=20, pady=10)
        self.management_button = customtkinter.CTkButton(self.navigation_frame, text="Manajemen",
                                                         command=lambda: self.select_frame_by_name("management"))
        self.management_button.grid(row=2, column=0, padx=20, pady=10) # Langsung tampilkan
        self.history_button = customtkinter.CTkButton(self.navigation_frame, text="Histori",
                                                      command=lambda: self.select_frame_by_name("history"))
        self.history_button.grid(row=3, column=0, padx=20, pady=10) # Langsung tampilkan
        self.login_logout_button = customtkinter.CTkButton(self.navigation_frame, text="Logout",
                                                           command=self.logout)
        self.login_logout_button.grid(row=5, column=0, padx=20, pady=20)
        
        # --- Frame Konten ---
        self.item_list_frame = ItemFrame(self)
        self.management_frame = ManagementFrame(self)
        self.history_frame = HistoryFrame(self)

        # Tampilkan frame awal
        self.select_frame_by_name("items")

    def logout(self):
        """Proses logout."""
        # Hancurkan semua widget UI utama
        self.navigation_frame.destroy()
        self.item_list_frame.destroy()
        self.management_frame.destroy()
        self.history_frame.destroy()

        # Atur ulang konfigurasi grid untuk layar login
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        # Tampilkan kembali layar login
        self.show_login_screen()

    def select_frame_by_name(self, name):
        # Sembunyikan semua frame dulu
        self.item_list_frame.grid_forget()
        self.management_frame.grid_forget()
        self.history_frame.grid_forget()

        # Tampilkan frame yang dipilih
        if name == "items":
            self.item_list_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.item_list_frame.refresh_item_table()
        elif name == "management":
            self.management_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.management_frame.refresh_all_tables()
        elif name == "history":
            self.history_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.history_frame.refresh_history_table()

# --- Main Execution ---
if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Gagal memulai aplikasi:\n{e}")
