<?php

namespace App\Models;

// use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

use App\Models\Food;

class User extends Authenticatable
{
    use HasFactory, Notifiable;

    public function foodUser(): HasOne
    {
        return $this->hasOne(Food\User::class, 'base_user_id');
    }
}
