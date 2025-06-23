<?php

use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

// Import Controller dari folder Admin (jika sudah diatur)
use App\Http\Controllers\Admin\BarangController;
use App\Http\Controllers\Admin\ManajemenBarangController;
use App\Http\Controllers\Admin\UserController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

// Ubah rute utama agar langsung diarahkan ke halaman login
Route::get('/', function () {
    return redirect()->route('login');
});


Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

// Rute Dashboard Default (jika ada) - ini akan digantikan oleh rute role-specific
// Route::get('/dashboard', function () {
//     return view('dashboard');
// })->middleware(['auth', 'verified'])->name('dashboard');

// Rute Dashboard untuk Super Admin
Route::get('/superadmin/dashboard', function () {
    return view('superadmin_dashboard'); // Mengarahkan ke view superadmin_dashboard.blade.php
})->middleware(['auth', 'verified', 'role:super_admin'])->name('superadmin.dashboard');

// Rute Dashboard untuk Admin
Route::get('/admin/dashboard', function () {
    return view('admin_dashboard'); // Mengarahkan ke view admin_dashboard.blade.php
})->middleware(['auth', 'verified', 'role:admin'])->name('admin.dashboard');


// Grup rute untuk Super Admin saja (mengelola user)
Route::middleware(['auth', 'role:super_admin'])->group(function () {
    Route::resource('users', UserController::class);
});

// Grup rute untuk Admin dan Super Admin (mengelola barang dan manajemen barang)
Route::middleware(['auth', 'role:admin,super_admin'])->group(function () {
    Route::resource('barang', BarangController::class);
    Route::resource('manajemen-barang', ManajemenBarangController::class);
    Route::post('manajemen-barang/{manajemen_barang}/kurangi', [ManajemenBarangController::class, 'kurangiBarang'])->name('manajemen-barang.kurangi');
});


require __DIR__.'/auth.php'; // Ini berisi rute-rute login, register, dll.