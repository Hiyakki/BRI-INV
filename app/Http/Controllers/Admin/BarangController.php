<?php

namespace App\Http\Controllers\Admin; // Pastikan namespace ini benar

use App\Models\Barang; // Import model Barang
use Illuminate\Http\Request; // Import Request
use App\Http\Controllers\Controller; // <-- TAMBAHKAN BARIS INI

class BarangController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        // Logika untuk menampilkan daftar barang
        $barangs = Barang::all(); // Contoh: mengambil semua barang
        return view('admin.barang.index', compact('barangs')); // Contoh: kembalikan view
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        // Logika untuk menampilkan form tambah barang
        return view('admin.barang.create');
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        // Logika untuk menyimpan data barang baru
        $request->validate([
            'kategori' => 'required|string|max:255',
            'nama_barang' => 'required|string|max:255',
            'stock' => 'required|integer|min:0',
            'deskripsi_barang' => 'nullable|string',
        ]);

        Barang::create($request->all());

        return redirect()->route('barang.index')->with('success', 'Barang berhasil ditambahkan!');
    }

    /**
     * Display the specified resource.
     */
    public function show(Barang $barang)
    {
        // Logika untuk menampilkan detail barang
        return view('admin.barang.show', compact('barang'));
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Barang $barang)
    {
        // Logika untuk menampilkan form edit barang
        return view('admin.barang.edit', compact('barang'));
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, Barang $barang)
    {
        // Logika untuk memperbarui data barang
        $request->validate([
            'kategori' => 'required|string|max:255',
            'nama_barang' => 'required|string|max:255',
            'stock' => 'required|integer|min:0',
            'deskripsi_barang' => 'nullable|string',
        ]);

        $barang->update($request->all());

        return redirect()->route('barang.index')->with('success', 'Barang berhasil diperbarui!');
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Barang $barang)
    {
        // Logika untuk menghapus barang
        $barang->delete();

        return redirect()->route('barang.index')->with('success', 'Barang berhasil dihapus!');
    }
}