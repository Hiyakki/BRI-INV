<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - BRI INV</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Font: Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            /* Pastikan body mengisi seluruh layar dan tidak ada margin/padding default */
            margin: 0;
            padding: 0;
            overflow: hidden; /* Mencegah scrollbar jika ada konten yang melebihi viewport */
        }
        /* Custom styling to ensure the right panel is rounded */
        .right-panel-wrapper {
            /* This div wraps the actual blue content and applies the border-radius */
            border-top-left-radius: 2rem; /* Matches the image's rounded corner */
            border-bottom-left-radius: 2rem; /* Matches the image's rounded corner */
            overflow: hidden; /* Ensures content inside respects the border-radius */
        }
        /* Adjust h-screen on small devices to prevent content overflow issues */
        @media (max-width: 767px) { /* Tailwind's 'md' breakpoint is 768px */
            body {
                min-height: 100vh; /* Ensure body takes full viewport height on small screens */
                overflow-y: auto; /* Allow vertical scrolling if content overflows */
            }
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Kontainer Utama yang mengisi seluruh layar -->
    <div class="flex w-full h-screen">
        <!-- Panel Kiri: Form Login (Putih) -->
        <div class="relative flex flex-col items-center justify-center w-full md:w-1/2 bg-white p-8 sm:p-12 lg:p-16">
            <!-- Placeholder Logo Kiri Atas -->
            <div class="absolute top-8 left-8">
                <!-- Ganti div ini dengan tag <img> Anda -->
                <div id="bri-logo-placeholder" class="text-2xl font-bold text-gray-800">
                    <img src="{{ asset('images/logo_login_atasKIRI.png') }}" alt="Logo BRI INV" class="h-50">
                </div>
            </div>

            <!-- Konten Form Login -->
            <div class="w-full max-w-sm mx-auto">
                <h1 class="text-3xl font-bold text-gray-800 mb-8">Masuk</h1>

                <form action="#" method="POST">
                    <!-- Input Personal Number -->
                    <div class="mb-6">
                        <label for="personal_number" class="block text-gray-700 text-sm font-semibold mb-2">Personal Number</label>
                        <input type="text" id="personal_number" name="personal_number" placeholder="" class="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2.5 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200" required>
                    </div>

                    <!-- Input Password -->
                    <div class="mb-8">
                        <label for="password" class="block text-gray-700 text-sm font-semibold mb-2">Password</label>
                        <input type="password" id="password" name="password" placeholder="" class="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2.5 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200" required>
                    </div>

                    <!-- Tombol Masuk -->
                    <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-white shadow-md transition-all duration-300">
                        Masuk
                    </button>
                </form>
            </div>
        </div>

        <!-- Panel Kanan: Ilustrasi/Ikon (Biru) -->
        <div class="hidden md:flex md:w-1/2 bg-blue-600 items-center justify-center right-panel-wrapper relative">
            <!-- Placeholder untuk Ikon Besar atau Ilustrasi di Tengah Kanan -->
            <div id="large-icon-placeholder" class="relative w-full h-full flex items-center justify-center">
                <!-- Ganti div ini dengan tag <img> atau SVG Anda -->
                <!-- Contoh ikon SVG sederhana: -->
                <!-- <svg class="w-64 h-64 text-white opacity-70" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                </svg> -->
                <img src="{{ asset('images/logo_kanan_login.png') }}" alt="Logo Kanan Login" class="w-64 h-auto opacity-70">

                <!-- Placeholder untuk Pola/Gambar Overlay di Background -->
                <div id="right-panel-overlay-image" class="absolute inset-0 z-10 opacity-10">
                    <!-- Ganti div ini dengan tag <img> atau elemen untuk pola background Anda -->
                    <!-- Contoh: <img src="/path/to/your/pattern.png" alt="Background Pattern" class="w-full h-full object-cover"> -->
                    <!-- Atau: <div style="background-image: url('https://placehold.co/1000x800/2980b9/ffffff?text=Right+Panel+Overlay'); background-size: cover; background-position: center;"></div> -->
                </div>
            </div>
        </div>
    </div>
</body>
</html>
