<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            {{ __('Dashboard Admin') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900">
                    Selamat datang, Admin! Anda dapat mengelola barang dan transaksi inventaris.
                    <br><br>
                    <h3 class="font-semibold text-lg mb-2">Akses Cepat:</h3>
                    <ul class="list-disc ml-5">
                        <li><a href="{{ route('barang.index') }}" class="text-blue-600 hover:underline">Kelola Barang</a></li>
                        <li><a href="{{ route('manajemen-barang.index') }}" class="text-blue-600 hover:underline">Manajemen Barang</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</x-app-layout>
