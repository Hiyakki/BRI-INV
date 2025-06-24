# File: app.py
import tkinter
from tkinter import ttk, messagebox
import customtkinter
import database as db # Mengimpor file database kita

# Pengaturan dasar CustomTkinter
customtkinter.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi Window Utama
        self.title("Aplikasi Manajemen Inventaris")
        self.geometry("1100x580")

        # Status Login
        self.is_admin = False

        # Membuat Grid Layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Membuat Frame Navigasi (Sidebar)
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
        # self.management_button.grid(row=2, column=0, padx=20, pady=10) # Disembunyikan dulu

        self.history_button = customtkinter.CTkButton(self.navigation_frame, text="Histori",
                                                      command=lambda: self.select_frame_by_name("history"))
        # self.history_button.grid(row=3, column=0, padx=20, pady=10) # Disembunyikan dulu

        # Tombol Login/Logout
        self.login_logout_button = customtkinter.CTkButton(self.navigation_frame, text="Login Admin",
                                                           command=self.handle_login_logout)
        self.login_logout_button.grid(row=5, column=0, padx=20, pady=20)
        
        # --- Frame Konten ---
        self.item_list_frame = ItemFrame(self, corner_radius=0, fg_color="transparent")
        self.management_frame = ManagementFrame(self, corner_radius=0, fg_color="transparent")
        self.history_frame = HistoryFrame(self, corner_radius=0, fg_color="transparent")

        # Tampilkan frame awal
        self.select_frame_by_name("items")
        self.update_ui_for_login_status()

    def select_frame_by_name(self, name):
        # Sembunyikan semua frame dulu
        self.item_list_frame.grid_forget()
        self.management_frame.grid_forget()
        self.history_frame.grid_forget()

        # Tampilkan frame yang dipilih
        if name == "items":
            self.item_list_frame.grid(row=0, column=1, sticky="nsew")
            self.item_list_frame.refresh_item_table()
        elif name == "management" and self.is_admin:
            self.management_frame.grid(row=0, column=1, sticky="nsew")
            self.management_frame.refresh_all_tables()
        elif name == "history" and self.is_admin:
            self.history_frame.grid(row=0, column=1, sticky="nsew")
            self.history_frame.refresh_history_table()

    def handle_login_logout(self):
        if self.is_admin:
            # Logout
            self.is_admin = False
            self.select_frame_by_name("items") # Kembali ke halaman item
            self.update_ui_for_login_status()
            messagebox.showinfo("Logout", "Anda telah berhasil logout.")
        else:
            # Buka jendela login
            self.open_login_window()

    def open_login_window(self):
        login_window = customtkinter.CTkToplevel(self)
        login_window.title("Login Admin")
        login_window.geometry("400x200")
        login_window.transient(self) # Selalu di atas window utama

        pn_label = customtkinter.CTkLabel(login_window, text="Personal Number:")
        pn_label.pack(pady=10)
        pn_entry = customtkinter.CTkEntry(login_window, width=200)
        pn_entry.pack()

        pw_label = customtkinter.CTkLabel(login_window, text="Password:")
        pw_label.pack(pady=10)
        pw_entry = customtkinter.CTkEntry(login_window, show="*", width=200)
        pw_entry.pack()

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

        login_button = customtkinter.CTkButton(login_window, text="Login", command=attempt_login)
        login_button.pack(pady=20)
        
    def update_ui_for_login_status(self):
        if self.is_admin:
            self.management_button.grid(row=2, column=0, padx=20, pady=10)
            self.history_button.grid(row=3, column=0, padx=20, pady=10)
            self.login_logout_button.configure(text="Logout")
        else:
            self.management_button.grid_forget()
            self.history_button.grid_forget()
            self.login_logout_button.configure(text="Login Admin")


# --- Definisi Frame/Halaman ---

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
        self.item_table.column("ID", width=50)
        self.item_table.column("Nama", width=200)
        self.item_table.column("Kategori", width=150)
        self.item_table.column("Stok", width=80)
        self.item_table.column("Deskripsi", width=300)

        self.item_table.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
    def refresh_item_table(self):
        # Hapus data lama
        for row in self.item_table.get_children():
            self.item_table.delete(row)
        # Ambil data baru dan masukkan ke tabel
        for item in db.get_all_items_with_category():
            # item format: (item_id, item_name, category_name, stock, description, date_added)
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
                
                if not taker_name:
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


# GANTI KELAS ManagementFrame DI app.py DENGAN KODE DI BAWAH INI

class ManagementFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Variabel untuk menyimpan ID item & kategori yang dipilih
        self.selected_item_id = None
        self.cat_name_to_id = {} # Untuk mapping nama kategori ke ID

        self.tab_view = customtkinter.CTkTabview(self, anchor="w")
        self.tab_view.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Tambahkan tab dengan urutan Item dulu baru Kategori
        self.tab_view.add("Manajemen Item")
        self.tab_view.add("Manajemen Kategori")
        
        # Setup UI untuk setiap tab
        self.setup_item_management_tab()
        self.setup_category_management_tab()

    def refresh_all_tables(self):
        """Fungsi ini dipanggil saat tab Manajemen diaktifkan."""
        self.refresh_cat_table()
        self.refresh_item_manage_table()
        self.refresh_category_combobox() # Pastikan combobox juga terupdate

    # ===================================================================
    # ==================== KODE MANAJEMEN ITEM ==========================
    # ===================================================================
    def setup_item_management_tab(self):
        tab = self.tab_view.tab("Manajemen Item")
        
        # Konfigurasi grid layout untuk tab item
        tab.grid_columnconfigure(0, weight=1) # Form frame
        tab.grid_columnconfigure(1, weight=3) # Table frame
        tab.grid_rowconfigure(0, weight=1)

        # --- Form Frame (Sebelah Kiri) ---
        form_frame = customtkinter.CTkFrame(tab)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        form_label = customtkinter.CTkLabel(form_frame, text="Form Data Item", font=customtkinter.CTkFont(size=14, weight="bold"))
        form_label.pack(pady=10, padx=10)

        # Widget-widget form
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
        self.item_desc_textbox.pack(fill="x", padx=10)
        
        # Tombol Aksi Form
        action_form_frame = customtkinter.CTkFrame(form_frame, fg_color="transparent")
        action_form_frame.pack(fill="x", pady=15, padx=10)
        
        save_button = customtkinter.CTkButton(action_form_frame, text="Simpan", command=self.save_item)
        save_button.pack(side="left", expand=True, padx=(0,5))
        
        clear_button = customtkinter.CTkButton(action_form_frame, text="Bersihkan Form", command=self.clear_item_form, fg_color="#565b5e")
        clear_button.pack(side="left", expand=True, padx=(5,0))

        # --- Table Frame (Sebelah Kanan) ---
        table_frame = customtkinter.CTkFrame(tab)
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.item_manage_table = ttk.Treeview(table_frame, columns=("ID", "Nama", "Kategori", "Stok"), show="headings")
        self.item_manage_table.heading("ID", text="ID")
        self.item_manage_table.heading("Nama", text="Nama Item")
        self.item_manage_table.heading("Kategori", text="Kategori")
        self.item_manage_table.heading("Stok", text="Stok")
        self.item_manage_table.column("ID", width=40)
        self.item_manage_table.column("Nama", width=200)
        self.item_manage_table.column("Kategori", width=120)
        self.item_manage_table.column("Stok", width=60)
        
        self.item_manage_table.grid(row=0, column=0, sticky="nsew")
        self.item_manage_table.bind("<<TreeviewSelect>>", self.on_item_select)
        
        delete_item_button = customtkinter.CTkButton(table_frame, text="Hapus Item Terpilih", fg_color="#D32F2F", hover_color="#B71C1C", command=self.delete_selected_item)
        delete_item_button.grid(row=1, column=0, pady=10)
        
    def refresh_item_manage_table(self):
        for row in self.item_manage_table.get_children():
            self.item_manage_table.delete(row)
        for item in db.get_all_items_with_category():
            self.item_manage_table.insert("", "end", values=(item[0], item[1], item[2] or "Tanpa Kategori", item[3]))
            
    def refresh_category_combobox(self):
        categories = db.get_all_categories()
        self.cat_name_to_id = {name: cat_id for cat_id, name in categories}
        cat_names = [name for _, name in categories]
        self.item_cat_combobox.configure(values=cat_names)
        if not cat_names:
            self.item_cat_combobox.set("Buat kategori dulu")
        else:
            self.item_cat_combobox.set("Pilih Kategori")
            
    def on_item_select(self, event=None):
        selected_row = self.item_manage_table.focus()
        if not selected_row:
            return
            
        # Dapatkan semua data dari database untuk item yang dipilih
        all_items = db.get_all_items_with_category()
        item_id = self.item_manage_table.item(selected_row, "values")[0]
        
        selected_data = None
        for item in all_items:
            if item[0] == int(item_id):
                selected_data = item
                break
        
        if not selected_data:
            return

        # (item_id, item_name, category_name, stock, description, date_added)
        self.clear_item_form()
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
        # Ambil data dari form
        name = self.item_name_entry.get()
        desc = self.item_desc_textbox.get("1.0", "end-1c")
        stock_str = self.item_stock_entry.get()
        cat_name = self.item_cat_combobox.get()
        cat_id = self.cat_name_to_id.get(cat_name)

        # Validasi
        if not name or not stock_str:
            messagebox.showerror("Error", "Nama Item dan Stok tidak boleh kosong.")
            return
        try:
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka.")
            return

        if self.selected_item_id: # Mode Update
            db.update_item(self.selected_item_id, name, desc, stock, cat_id)
            messagebox.showinfo("Sukses", "Item berhasil diperbarui.")
        else: # Mode Tambah
            db.add_item(name, desc, stock, cat_id)
            messagebox.showinfo("Sukses", "Item baru berhasil ditambahkan.")

        # Refresh dan bersihkan
        self.refresh_item_manage_table()
        self.master.item_list_frame.refresh_item_table() # Refresh juga di halaman utama
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

    # ===================================================================
    # ================= KODE MANAJEMEN KATEGORI =========================
    # ===================================================================
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
        if cat_name:
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
        for cat in db.get_all_categories():
            self.cat_table.insert("", "end", values=cat)

class HistoryFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        label = customtkinter.CTkLabel(self, text="Histori Pengambilan Barang", font=customtkinter.CTkFont(size=16, weight="bold"))
        label.pack(padx=20, pady=20)
        
        self.history_table = ttk.Treeview(self, columns=("Tanggal", "Nama Barang", "Jumlah", "Pengambil"), show="headings")
        self.history_table.heading("Tanggal", text="Tanggal Pengambilan")
        self.history_table.heading("Nama Barang", text="Nama Barang")
        self.history_table.heading("Jumlah", text="Jumlah")
        self.history_table.heading("Pengambil", text="Nama Pengambil")
        
        self.history_table.column("Tanggal", width=150)
        self.history_table.column("Nama Barang", width=250)
        self.history_table.column("Jumlah", width=100)
        self.history_table.column("Pengambil", width=200)
        
        self.history_table.pack(expand=True, fill="both", padx=20, pady=10)

    def refresh_history_table(self):
        for row in self.history_table.get_children():
            self.history_table.delete(row)
        for log in db.get_history():
            self.history_table.insert("", "end", values=(log[0], log[1] or "ITEM DIHAPUS", log[2], log[3]))
            

# --- Main Execution ---
if __name__ == "__main__":
    # Inisialisasi awal database jika diperlukan
    # Disarankan menjalankan `python database.py` secara terpisah sekali saja
    
    app = App()
    app.mainloop()