<?php

namespace App\Models\Food;

use App\Models\Day;
use App\Models\User;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

class Meal extends Model
{
    use HasFactory;
    use SoftDeletes;

    protected $table = 'food_meals';

    protected $casts = [
        'position' => 'int',
    ];

    public function getRouteKeyName()
    {
        return 'position';
    }

    public function day(): BelongsTo
    {
        return $this->belongsTo(Day::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

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
