<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use Illuminate\Support\Facades\Auth; // Tambahkan ini jika belum ada

class CheckRole
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, ...$roles): Response
    {
        // Pastikan user sudah login
        if (!Auth::check()) { // Menggunakan Auth::check() adalah alternatif yang aman
            return redirect('/login');
        }

        // Dapatkan user yang sedang login
        $user = Auth::user();

        // Pastikan user object tidak null dan memiliki properti 'role'
        // Ini adalah pengecekan ekstra untuk debug, bisa dihapus setelah yakin
        if (!$user || !property_exists($user, 'role')) {
            // Log atau laporkan error di sini
            abort(500, 'User object or role property not found.');
        }

        // Periksa apakah role user ada di dalam daftar roles yang diizinkan
        if (!in_array($user->role, $roles)) {
            abort(403, 'Unauthorized action.');
        }

        return $next($request);
    }
}