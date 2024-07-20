<?php

namespace Database\Seeders\Food;

use App\Models\Food\Group;
use App\Models\Food\Item;
use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class ItemSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $foodCsvPath = storage_path('app/csv/food.csv');
        $file = fopen($foodCsvPath, 'r');

        $user = User::find(1);

        $group_name = 'group_1';
        $group = Group::create([
            'name' => $group_name,
            'user_id' => $user->id,
        ]);
        while ($line = fgetcsv($file)) {
            if ($line[0] == null) {
                $group = Group::create([
                    'name' => ++$group_name,
                    'user_id' => $user->id,
                ]);
                continue;
            }

            $group->items()->create([
                'name' => $line[0],
                'proteins' => floatval(str_replace(',', '.', $line[1])),
                'fats' => floatval(str_replace(',', '.', $line[2])),
                'carbs' => floatval(str_replace(',', '.', $line[3])),
                'calories' => floatval(str_replace(',', '.', $line[4])),
                'piece_mass' => empty($line[5])
                    ? null
                    : floatval(str_replace(',', '.', $line[5])),
            ]);
        }

        fclose($file);
    }
}
