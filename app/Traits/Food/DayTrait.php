<?php

namespace App\Traits\Food;

use App\Models\Food\Comment;
use App\Models\Food\Meal;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

trait DayTrait
{
    public function meals(): HasMany
    {
        return $this->hasMany(Meal::class);
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }

    public function mass(): Attribute
    {
        return Attribute::make(get: fn() => $this->meals->sum('mass'));
    }

    public function proteins(): Attribute
    {
        return Attribute::make(get: fn() => $this->meals->sum('proteins'));
    }

    public function fats(): Attribute
    {
        return Attribute::make(get: fn() => $this->meals->sum('fats'));
    }

    public function carbs(): Attribute
    {
        return Attribute::make(get: fn() => $this->meals->sum('carbs'));
    }

    public function calories(): Attribute
    {
        return Attribute::make(get: fn() => $this->meals->sum('calories'));
    }
}