<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        User::create([
            'id' => 1,
            'name' => 'Никита Киренков',
            'email' => 'nikitakirenkov@gmail.com',
            'password' => Hash::make('test'),
        ]);

        User::create([
            'id' => 2,
            'name' => 'Nord421Osten',
            'email' => '@Nord421Osten',
            'password' => Hash::make('test'),
        ]);
    }
}
