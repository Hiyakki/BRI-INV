<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Http\Requests\Auth\LoginRequest; // Pastikan ini ada
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class AuthenticatedSessionController extends Controller
{
    /**
     * Display the login view.
     */
    public function create(): View
    {
        return view('auth.login');
    }

    /**
     * Handle an incoming authentication request.
     */
    public function store(LoginRequest $request): RedirectResponse
    {
        $request->authenticate(); // Ini akan mencoba mengautentikasi pengguna

        $request->session()->regenerate();

        // Dapatkan user yang baru saja login
        $user = Auth::user();

        // Cek role user dan arahkan ke dashboard yang sesuai
        if ($user->role === 'super_admin') {
            return redirect()->intended(route('superadmin.dashboard')); // Arahkan ke dashboard Super Admin
        } elseif ($user->role === 'admin') {
            return redirect()->intended(route('admin.dashboard')); // Arahkan ke dashboard Admin
        }

        // Fallback jika role tidak terdefinisi atau tidak sesuai
        return redirect()->intended(route('dashboard', absolute: false));
    }

    /**
     * Destroy an authenticated session.
     */
    public function destroy(Request $request): RedirectResponse
    {
        Auth::guard('web')->logout();

        $request->session()->invalidate();

        $request->session()->regenerateToken();

        return redirect('/');
    }
}