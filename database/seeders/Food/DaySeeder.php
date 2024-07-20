<?php

namespace Database\Seeders\Food;

use App\Models\Food\Comment;
use App\Models\Day;
use App\Models\Food\Meal;
use App\Models\Food\Record;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Database\Seeder;

class DaySeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $user = User::find(1);

        for ($i = fake()->numberBetween(5, 7); $i > 0; $i--) {
            $day = $user->days()->create(['date' => new Carbon("-$i days")]);

            for ($j = 0; $j < fake()->numberBetween(3, 5); $j++) {
                $meal = $day->meals()->create([
                    'position' => $j,
                ]);
                Record::factory()
                    ->count(fake()->numberBetween(1, 5))
                    ->for($meal)
                    ->create();
            }

            Comment::factory()
                ->count(fake()->numberBetween(0, 7))
                ->for($day)
                ->for(User::inRandomOrder()->first())
                ->create();
        }
    }
}
