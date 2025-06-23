<?php

namespace App\Http\Controllers\Admin;

use App\Models\User;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\Rule;
use Illuminate\Support\Facades\Auth; // Tambahkan ini jika belum ada

class UserController extends Controller
{
    public function index()
    {
        $users = User::latest()->paginate(10);
        return view('admin.users.index', compact('users'));
    }

    public function create()
    {
        return view('admin.users.create');
    }

    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'personal_number' => 'required|string|max:255|unique:users', // Personal number adalah identifikasi unik
            // 'email' => 'nullable|string|email|max:255|unique:users', // HAPUS ATAU KOMENTARI BARIS INI
            'password' => 'required|string|min:8|confirmed',
            'role' => ['required', 'string', Rule::in(['admin', 'super_admin'])],
        ]);

        User::create([
            'name' => $request->name,
            'personal_number' => $request->personal_number,
            // 'email' => null, // Tidak perlu menyimpan email jika tidak ada kolomnya
            'password' => Hash::make($request->password),
            'role' => $request->role,
        ]);

        return redirect()->route('users.index')->with('success', 'User berhasil ditambahkan!');
    }

    public function show(User $user)
    {
        return view('admin.users.show', compact('user'));
    }

    public function edit(User $user)
    {
        if (Auth::user()->id === $user->id && Auth::user()->role === 'super_admin') {
            return redirect()->route('dashboard')->with('error', 'Anda tidak dapat mengedit profil Super Admin Anda sendiri melalui halaman ini. Gunakan halaman profil jika ada.');
        }
        return view('admin.users.edit', compact('user'));
    }

    public function update(Request $request, User $user)
    {
        $rules = [
            'name' => 'required|string|max:255',
            'personal_number' => ['required', 'string', 'max:255', Rule::unique('users')->ignore($user->id)], // Personal number wajib dan unik
            // 'email' => ['nullable', 'string', 'email', 'max:255', Rule::unique('users')->ignore($user->id)], // HAPUS ATAU KOMENTARI BARIS INI
        ];

        if ($request->filled('password')) {
            $rules['password'] = 'required|string|min:8|confirmed';
        }

        if (Auth::user()->role === 'super_admin') {
            if (Auth::user()->id === $user->id && $request->role !== 'super_admin') {
                return redirect()->back()->withErrors(['role' => 'Super Admin tidak dapat mengubah role-nya sendiri.'])->withInput();
            }
            if ($user->role === 'super_admin' && $request->role !== 'super_admin') {
                return redirect()->back()->withErrors(['role' => 'Anda tidak dapat mengubah role Super Admin lain.'])->withInput();
            }
            $rules['role'] = ['required', 'string', Rule::in(['admin', 'super_admin'])];
        } else {
            unset($request['role']);
        }

        $request->validate($rules);

        // Siapkan data untuk diupdate
        $data = $request->only(['name', 'personal_number']); // Email dihapus dari sini

        if ($request->filled('password')) {
            $data['password'] = Hash::make($request->password);
        }

        if (isset($request->role)) {
            $data['role'] = $request->role;
        }

        $user->update($data);

        return redirect()->route('users.index')->with('success', 'User berhasil diperbarui!');
    }

    public function destroy(User $user)
    {
        if (Auth::user()->id === $user->id) {
            return redirect()->back()->with('error', 'Anda tidak dapat menghapus akun Anda sendiri.');
        }

        if ($user->role === 'super_admin') {
            return redirect()->back()->with('error', 'Anda tidak dapat menghapus Super Admin lain.');
        }

        $user->delete();

        return redirect()->route('users.index')->with('success', 'User berhasil dihapus!');
    }
}