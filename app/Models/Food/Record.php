<?php

namespace App\Models\Food;

use App\Enums\Food\RecordType;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Record extends Model
{
    use HasFactory;

    protected $table = 'food_records';

    protected $casts = [
        'type' => RecordType::class,
    ];

    public function meal(): BelongsTo
    {
        return $this->belongsTo(Meal::class);
    }

    public function item(): BelongsTo
    {
        return $this->belongsTo(Item::class);
    }
    
    public function mass(): Attribute
    {
        return Attribute::make(
            get: function () {
                switch ($this->type) {
                    case RecordType::Mass:
                        return $this->value;
                    case RecordType::Pieces:
                        return $this->value * $this->item->piece_mass;
                }
            }
        );
    }

    public function proteins(): Attribute
    {
        return Attribute::make(get: fn() => (float) $this->item->proteins * $this->mass / 100);
    }

    public function fats(): Attribute
    {
        return Attribute::make(get: fn() => (float) $this->item->fats * $this->mass / 100);
    }

    public function carbs(): Attribute
    {
        return Attribute::make(get: fn() => (float) $this->item->carbs * $this->mass / 100);
    }

    public function calories(): Attribute
    {
        return Attribute::make(get: fn() => (float) $this->item->calories * $this->mass / 100);
    }
}
