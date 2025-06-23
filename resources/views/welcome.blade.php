<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Inventory BRI</title>

        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=figtree:400,500,600&display=swap" rel="stylesheet" />

        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="antialiased">
        <div class="relative sm:flex sm:justify-center sm:items-center min-h-screen bg-dots-darker bg-center bg-gray-100 dark:bg-dots-lighter dark:bg-gray-900 selection:bg-red-500 selection:text-white">
            @if (Route::has('login'))
                <div class="sm:fixed sm:top-0 sm:right-0 p-6 text-right z-10">
                    @auth
                        {{-- Jika user sudah login, arahkan ke dashboard mereka --}}
                        <a href="{{ url('/dashboard') }}" class="font-semibold text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white focus:outline focus:outline-2 focus:rounded-sm focus:outline-red-500">Dashboard</a>
                    @else
                        {{-- Jika user belum login, tampilkan link login dan register --}}
                        <a href="{{ route('login') }}" class="font-semibold text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white focus:outline focus:outline-2 focus:rounded-sm focus:outline-red-500">Log in</a>

                        @if (Route::has('register'))
                            <a href="{{ route('register') }}" class="ml-4 font-semibold text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white focus:outline focus:outline-2 focus:rounded-sm focus:outline-red-500">Register</a>
                        @endif
                    @endauth
                </div>
            @endif

            <div class="max-w-7xl mx-auto p-6 lg:p-8 text-center">
                <div class="flex justify-center">
                    {{-- Anda bisa menempatkan logo atau ikon di sini --}}
                    {{-- <img src="/images/your-logo.png" alt="Logo Perusahaan" class="h-20 w-auto"> --}}
                </div>

                <h1 class="mt-8 text-4xl font-bold text-gray-900 dark:text-white">Selamat Datang di Sistem Inventory BRI</h1>
                <p class="mt-4 text-lg text-gray-600 dark:text-gray-400">
                    Aplikasi ini membantu Anda mengelola pencatatan inventaris barang dengan mudah dan efisien.
                </p>
                <p class="mt-2 text-md text-gray-500 dark:text-gray-500">
                    Masuk sebagai Admin atau Super Admin untuk mengakses fitur manajemen inventaris.
                </p>

                <div class="mt-8 flex justify-center space-x-4">
                    <a href="{{ route('login') }}" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Login Sekarang
                    </a>
                    <a href="{{ route('register') }}" class="inline-flex items-center px-6 py-3 border border-indigo-600 text-base font-medium rounded-md text-indigo-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Daftar (Admin)
                    </a>
                </div>

                <div class="mt-16 text-center text-sm text-gray-500 dark:text-gray-400 sm:text-right sm:ml-0">
                    Laravel v{{ Illuminate\Foundation\Application::VERSION }} (PHP v{{ PHP_VERSION }})
                </div>
            </div>
        </div>
    </body>
</html>