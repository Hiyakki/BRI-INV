<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        User::create([
            'name' => 'Super Admin',
            'password' => Hash::make('password'), 
            'role' => 'super_admin',
            'personal_number' => 'SA001',
        ]);

        User::create([
            'name' => 'Admin User',
            'password' => Hash::make('password'), 
            'role' => 'admin',
            'personal_number' => 'AD001',
        ]);
    }
}