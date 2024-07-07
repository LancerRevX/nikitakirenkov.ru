<?php

namespace App\Models\Food;

use Illuminate\Database\Eloquent\Casts\Attribute;
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

    public function mass(): Attribute
    {
        return Attribute::make(get: fn() => $this->records->sum('mass'));
    }

    public function proteins(): Attribute
    {
        return Attribute::make(get: fn() => $this->records->sum('proteins'));
    }

    public function fats(): Attribute
    {
        return Attribute::make(get: fn() => $this->records->sum('fats'));
    }

    public function carbs(): Attribute
    {
        return Attribute::make(get: fn() => $this->records->sum('carbs'));
    }

    public function calories(): Attribute
    {
        return Attribute::make(get: fn() => $this->records->sum('calories'));
    }
}
