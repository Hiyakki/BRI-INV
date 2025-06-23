<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ManajemenBarang extends Model
{
    use HasFactory;

    protected $table = 'manajemen_barang'; // Pastikan nama tabel benar
    protected $fillable = [
        'barang_id',
        'user_id',
        'nama_barang',
        'deskripsi',
        'kategori',
        'stock_sebelum',
        'jumlah_perubahan',
        'stock_sesudah',
        'status',
    ];

    public function barang()
    {
        return $this->belongsTo(Barang::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}