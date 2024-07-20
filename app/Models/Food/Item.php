<?php

namespace App\Models\Food;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Item extends Model
{
    use HasFactory;

    protected $table = 'food_items';

    protected $casts = [
        'proteins' => 'float',
        'fats' => 'float',
        'carbs' => 'float',
        'calories' => 'float',
        'piece_mass' => 'int',
    ];

    public function group(): BelongsTo
    {
        return $this->belongsTo(Group::class);
    }

    public function pieceProteins(): Attribute
    {
        return Attribute::make(
            get: fn() => $this->piece_mass
                ? $this->proteins * $this->piece_mass / 100
                : null
        );
    }

    public function pieceFats(): Attribute
    {
        return Attribute::make(
            get: fn() => $this->piece_mass
                ? $this->fats * $this->piece_mass / 100
                : null
        );
    }

    public function pieceCarbs(): Attribute
    {
        return Attribute::make(
            get: fn() => $this->piece_mass
                ? $this->carbs * $this->piece_mass / 100
                : null
        );
    }

    public function pieceCalories(): Attribute
    {
        return Attribute::make(
            get: fn() => $this->piece_mass
                ? $this->calories * $this->piece_mass / 100
                : null
        );
    }
}
