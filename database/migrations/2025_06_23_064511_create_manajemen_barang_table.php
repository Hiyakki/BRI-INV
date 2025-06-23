<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{

    public function up(): void
    {
        Schema::create('manajemen_barang', function (Blueprint $table) {
            $table->id(); // Mengganti IDbarang jika di gambar adalah primary key manajemen
            $table->foreignId('barang_id')->constrained('barang')->onDelete('cascade');
            $table->foreignId('user_id')->constrained('users')->onDelete('cascade');
            $table->string('nama_barang'); // Bisa juga diambil dari relasi, ini untuk denormalisasi sederhana
            $table->text('deskripsi')->nullable();
            $table->string('kategori'); // Bisa juga diambil dari relasi
            $table->integer('stock_sebelum');
            $table->integer('jumlah_perubahan');
            $table->integer('stock_sesudah');
            $table->enum('status', ['keluar', 'masuk']);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('manajemen_barang');
    }
};
