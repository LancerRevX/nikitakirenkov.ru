<?php

namespace App\Models\Food;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    use HasFactory;

    protected $table = 'food_comments';

    public function day(): BelongsTo
    {
        return $this->belongsTo(Day::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
