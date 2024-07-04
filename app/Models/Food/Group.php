<?php

namespace App\Models\Food;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Group extends Model
{
    use HasFactory;

    protected $table = 'food_groups';

    public function items(): BelongsToMany
    {
        return $this->belongsToMany(Item::class, 'food_group_item');
    }

    public function color(): Attribute
    {
        return Attribute::make(get: fn(string $value) => '#' . $value);
    }
}
