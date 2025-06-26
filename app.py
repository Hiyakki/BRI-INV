# File: app.py (Versi Sederhana dengan Login Pop-up)
import tkinter
from tkinter import ttk, messagebox
import customtkinter
import database as db
import os

# Import kelas-kelas Frame dari folder 'ui'
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
        self.geometry("1100x650")

        # Status Login
        self.is_admin = False
        
        # Inisialisasi cache
        self.category_cache = None

        # Membuat Grid Layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Frame Navigasi (Sidebar) ---
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Menu Utama",
                                                             font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Tombol Navigasi
        self.item_list_button = customtkinter.CTkButton(self.navigation_frame, text="Daftar Item",
                                                        command=lambda: self.select_frame_by_name("items"))
        self.item_list_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.management_button = customtkinter.CTkButton(self.navigation_frame, text="Manajemen",
                                                         command=lambda: self.select_frame_by_name("management"))
        
        self.history_button = customtkinter.CTkButton(self.navigation_frame, text="Histori",
                                                      command=lambda: self.select_frame_by_name("history"))
        
        self.login_logout_button = customtkinter.CTkButton(self.navigation_frame, text="Login Admin",
                                                           command=self.handle_login_logout)
        self.login_logout_button.grid(row=5, column=0, padx=20, pady=20)
        
        # --- Frame Konten ---
        self.item_list_frame = ItemFrame(self)
        self.management_frame = ManagementFrame(self)
        self.history_frame = HistoryFrame(self)

        # Tampilkan frame awal dan atur UI sesuai status login
        self.select_frame_by_name("items")
        self.update_ui_for_login_status()

    def select_frame_by_name(self, name):
        self.item_list_frame.grid_forget()
        self.management_frame.grid_forget()
        self.history_frame.grid_forget()

        if name == "items":
            self.item_list_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            # Selalu refresh saat halaman ditampilkan
            self.item_list_frame.refresh_item_table()
        elif name == "management" and self.is_admin:
            self.management_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.management_frame.refresh_all_tables()
        elif name == "history" and self.is_admin:
            self.history_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.history_frame.refresh_history_table()

    def handle_login_logout(self):
        if self.is_admin:
            # Proses Logout
            if messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin logout?"):
                self.is_admin = False
                self.update_ui_for_login_status()
                self.select_frame_by_name("items") # Kembali ke halaman item
        else:
            # Proses Login
            self.open_login_window()

    def open_login_window(self):
        login_window = customtkinter.CTkToplevel(self)
        login_window.title("Login Admin")
        login_window.geometry("400x200")
        login_window.transient(self)
        login_window.grab_set()

        pn_label = customtkinter.CTkLabel(login_window, text="Personal Number:")
        pn_label.pack(pady=10)
        pn_entry = customtkinter.CTkEntry(login_window, width=200)
        pn_entry.pack()
        pn_entry.focus()

        pw_label = customtkinter.CTkLabel(login_window, text="Password:")
        pw_label.pack(pady=10)
        pw_entry = customtkinter.CTkEntry(login_window, show="*", width=200)
        pw_entry.pack()
        pw_entry.bind("<Return>", lambda event: attempt_login())

        def attempt_login():
            pn = pn_entry.get()
            pw = pw_entry.get()
            if db.validate_admin(pn, pw):
                self.is_admin = True
                self.update_ui_for_login_status()
                login_window.destroy()
                messagebox.showinfo("Login Sukses", "Selamat datang, Admin!")
            else:
                messagebox.showerror("Login Gagal", "Personal Number atau Password salah.")
                pn_entry.focus()

        login_button = customtkinter.CTkButton(login_window, text="Login", command=attempt_login)
        login_button.pack(pady=20)
        
    def update_ui_for_login_status(self):
        """Menampilkan atau menyembunyikan tombol admin berdasarkan status login."""
        if self.is_admin:
            self.management_button.grid(row=2, column=0, padx=20, pady=10)
            self.history_button.grid(row=3, column=0, padx=20, pady=10)
            self.login_logout_button.configure(text="Logout")
        else:
            self.management_button.grid_forget()
            self.history_button.grid_forget()
            self.login_logout_button.configure(text="Login Admin")

# --- Main Execution ---
if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Gagal memulai aplikasi:\n{e}")

