<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Barang extends Model
{
    use HasFactory;

    protected $table = 'barang'; // Pastikan nama tabel benar
    protected $fillable = [
        'kategori',
        'nama_barang',
        'stock',
        'deskripsi_barang',
    ];

    public function manajemenBarangs()
    {
        return $this->hasMany(ManajemenBarang::class);
    }
}