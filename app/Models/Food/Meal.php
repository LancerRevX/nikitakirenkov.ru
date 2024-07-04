<?php

namespace App\Models\Food;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Meal extends Model
{
    use HasFactory;

    protected $table = 'food_meals';

    public function records(): HasMany
    {
        return $this->hasMany(Record::class);
    }
}
