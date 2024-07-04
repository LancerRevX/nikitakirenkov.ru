<?php

namespace App\Models\Food;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Item extends Model
{
    use HasFactory;

    protected $table = 'food_items';

    public function groups(): BelongsToMany
    {
        return $this->belongsToMany(Group::class, $this->prefix . 'food_group_item');
    }
}
