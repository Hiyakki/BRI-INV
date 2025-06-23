<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('barang', function (Blueprint $table) {
            $table->id(); // Mengganti IDbarang
            $table->string('kategori');
            $table->string('nama_barang');
            $table->integer('stock')->default(0);
            $table->text('deskripsi_barang')->nullable();
            $table->timestamps();
        });
    }


    public function down(): void
    {
        Schema::dropIfExists('barang');
    }
};
