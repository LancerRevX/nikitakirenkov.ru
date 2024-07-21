<?php

namespace App\Models;

use App\Models\Food\Meal;
use App\Traits\Food\DayTrait;
use Carbon\Carbon;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Facades\Validator;

class Day extends Model
{
    use HasFactory;
    use DayTrait;

    protected $fillable = ['date'];

    public $casts = [
        'date' => 'date',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    // public function resolveRouteBinding($date, $field = null)
    // {
    //     Validator::make(
    //         ['day' => $date],
    //         ['day' => 'date_format:Y-m-d']
    //     )->validate();
    //     return self::whereDate('date', $date)->first() ??
    //         new self(['date' => $date]);
    // }

    // public function resolveChildRouteBinding($childType, $value, $field)
    // {
    //     if ($childType != Meal::class) {
    //         return parent::resolveChildRouteBinding($childType, $value, $field);
    //     }

    //     Validator::make(['mealPosition' => $value], ['mealPosition' => 'integer'])->validate();
    //     return $this->meals()->where('position', $value)->first();
    // }
}
