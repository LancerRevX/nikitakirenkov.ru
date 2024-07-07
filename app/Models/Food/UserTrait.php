<?php

namespace App\Models\Food;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;

trait UserTrait
{
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
}
