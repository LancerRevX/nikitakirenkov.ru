<?php

namespace Database\Factories\Food;

use App\Models\Food\Item;
use App\Enums\Food\RecordType;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Food\Record>
 */
class RecordFactory extends Factory
{
    private $position = 0;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $item = Item::inRandomOrder()->first();

        if ($item->piece_mass != null) {
            $type = RecordType::Pieces;
            $value = fake()->numberBetween(1, 5);
        } else {
            $type = RecordType::Mass;
            $value = fake()->numberBetween(20, 300);
        }

        return [
            'item_id' => $item->id,
            'type' => $type,
            'value' => $value,
            'position' => $this->position++,
        ];
    }
}
