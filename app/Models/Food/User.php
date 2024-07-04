<?php

namespace App\Models\Food;

use App\Models\User as BaseUser;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends BaseUser
{
    use HasFactory;

    public function coaches(): BelongsToMany
    {
        return $this->belongsToMany(
            self::class,
            'food_coach_client',
            'client_id',
            'coach_id'
        );
    }

    public function clients(): BelongsToMany
    {
        return $this->belongsToMany(
            self::class,
            'food_coach_client',
            'coach_id',
            'client_id'
        );
    }

    public function days(): HasMany
    {
        return $this->hasMany(Day::class);
    }
}
