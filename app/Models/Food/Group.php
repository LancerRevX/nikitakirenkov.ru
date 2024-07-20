<?php

namespace App\Models\Food;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Group extends Model
{
    use HasFactory;

    protected $table = 'food_groups';

    public function items(): HasMany
    {
        return $this->hasMany(Item::class);
    }

    public function color(): Attribute
    {
        return Attribute::make(get: fn(string $value) => '#' . $value);
    }
}
