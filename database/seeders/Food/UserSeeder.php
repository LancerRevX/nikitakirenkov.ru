<?php

namespace Database\Seeders\Food;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $client = User::find(1);
        $coach = User::find(2);
        $coach->clients()->save($client);
    }
}
