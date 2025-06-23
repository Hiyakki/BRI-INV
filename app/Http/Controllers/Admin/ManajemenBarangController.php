<?php

namespace App\Http\Controllers\Admin; // Pastikan namespace ini benar

use App\Models\ManajemenBarang;
use App\Models\Barang; // Import model Barang
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Auth; // Untuk mendapatkan user yang sedang login

class ManajemenBarangController extends Controller
{

    public function index()
    {
        $manajemenBarangs = ManajemenBarang::with(['barang', 'user'])->latest()->paginate(10);
        return view('admin.manajemen_barang.index', compact('manajemenBarangs'));
    }

    public function create()
    {
        $barangs = Barang::all(); // Ambil semua barang untuk pilihan di form
        return view('admin.manajemen_barang.create', compact('barangs'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'barang_id' => 'required|exists:barang,id',
            'jumlah_perubahan' => 'required|integer|min:1',
            'status' => 'required|in:masuk,keluar',
            'deskripsi' => 'nullable|string',
        ]);

        $barang = Barang::findOrFail($request->barang_id);
        $stock_sebelum = $barang->stock;
        $jumlah_perubahan = $request->jumlah_perubahan;
        $stock_sesudah = $stock_sebelum;

        if ($request->status === 'keluar') {
            if ($barang->stock < $jumlah_perubahan) {
                return redirect()->back()->withErrors(['jumlah_perubahan' => 'Jumlah barang keluar tidak boleh melebihi stok yang tersedia.'])->withInput();
            }
            $stock_sesudah = $stock_sebelum - $jumlah_perubahan;
        } else { // status === 'masuk'
            $stock_sesudah = $stock_sebelum + $jumlah_perubahan;
        }

        // Update stok barang
        $barang->stock = $stock_sesudah;
        $barang->save();

        // Buat catatan di manajemen_barang
        ManajemenBarang::create([
            'barang_id' => $barang->id,
            'user_id' => Auth::id(), // Dapatkan ID user yang sedang login
            'nama_barang' => $barang->nama_barang, // Bisa diambil dari relasi, ini untuk denormalisasi sederhana
            'deskripsi' => $request->deskripsi,
            'kategori' => $barang->kategori, // Bisa diambil dari relasi
            'stock_sebelum' => $stock_sebelum,
            'jumlah_perubahan' => $jumlah_perubahan,
            'stock_sesudah' => $stock_sesudah,
            'status' => $request->status,
        ]);

        return redirect()->route('manajemen-barang.index')->with('success', 'Transaksi manajemen barang berhasil dicatat!');
    }


    public function show(ManajemenBarang $manajemenBarang)
    {
        // Untuk menampilkan detail transaksi, kita juga bisa memuat relasi
        $manajemenBarang->load('barang', 'user');
        return view('admin.manajemen_barang.show', compact('manajemenBarang'));
    }


    public function edit(ManajemenBarang $manajemenBarang)
    {
        $barangs = Barang::all(); // Ambil semua barang untuk pilihan di form
        return view('admin.manajemen_barang.edit', compact('manajemenBarang', 'barangs'));
    }

    public function update(Request $request, ManajemenBarang $manajemenBarang)
    {
        $request->validate([
            'barang_id' => 'required|exists:barang,id',
            'jumlah_perubahan' => 'required|integer|min:1',
            'status' => 'required|in:masuk,keluar',
            'deskripsi' => 'nullable|string',
        ]);

        $manajemenBarang->update($request->all());

        return redirect()->route('manajemen-barang.index')->with('success', 'Catatan manajemen barang berhasil diperbarui!');
    }

    public function destroy(ManajemenBarang $manajemenBarang)
    {
        // Dalam kasus nyata, Anda perlu memikirkan apakah menghapus transaksi manajemen barang
        // harus mengembalikan stok barang ke kondisi sebelum transaksi ini.
        // Untuk kesederhanaan, ini hanya menghapus catatan transaksi.
        $manajemenBarang->delete();

        return redirect()->route('manajemen-barang.index')->with('success', 'Catatan manajemen barang berhasil dihapus!');
    }

    /**
     * Custom method to reduce stock for a specific item.
     * Metode khusus untuk mengurangi jumlah barang (keluar).
     * Ini adalah metode yang akan dipanggil oleh route `manajemen-barang.kurangi`.
     */
    public function kurangiBarang(Request $request, ManajemenBarang $manajemenBarang = null)
    {
        // Jika Anda ingin metode ini hanya untuk mengurangi, pastikan validasi dan logika sesuai.
        // Parameter $manajemenBarang di sini mungkin tidak relevan jika Anda hanya ingin mengurangi barang berdasarkan ID_Barang,
        // bukan berdasarkan transaksi manajemen_barang yang sudah ada.

        $request->validate([
            'barang_id' => 'required|exists:barang,id',
            'jumlah_kurang' => 'required|integer|min:1',
            'deskripsi' => 'nullable|string', // Deskripsi mengapa barang dikurangi
        ]);

        $barang = Barang::findOrFail($request->barang_id);

        if ($barang->stock < $request->jumlah_kurang) {
            return redirect()->back()->withErrors(['jumlah_kurang' => 'Jumlah yang ingin dikurangi melebihi stok yang tersedia.'])->withInput();
        }

        $stock_sebelum = $barang->stock;
        $jumlah_perubahan = $request->jumlah_kurang;
        $stock_sesudah = $stock_sebelum - $jumlah_perubahan;

        // Update stok barang
        $barang->stock = $stock_sesudah;
        $barang->save();

        // Catat transaksi di tabel manajemen_barang
        ManajemenBarang::create([
            'barang_id' => $barang->id,
            'user_id' => Auth::id(),
            'nama_barang' => $barang->nama_barang,
            'deskripsi' => $request->deskripsi,
            'kategori' => $barang->kategori,
            'stock_sebelum' => $stock_sebelum,
            'jumlah_perubahan' => $jumlah_perubahan,
            'stock_sesudah' => $stock_sesudah,
            'status' => 'keluar', // Status selalu 'keluar' untuk fungsi ini
        ]);

        return redirect()->route('manajemen-barang.index')->with('success', 'Barang berhasil dikurangi dan transaksi dicatat!');
    }
}