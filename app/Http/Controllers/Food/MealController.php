<?php

namespace App\Http\Controllers\Food;

use App\Http\Controllers\Controller;
use App\Http\Resources\Food\MealResource;
use App\Models\Day;
use App\Models\Food\Meal;
use App\Models\User;
use Carbon\Carbon;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;

class MealController extends Controller
{
    public function store(Request $request, User $user, Day $day): MealResource
    {
        $request->validate([]);

        if ($day->isDirty()) {
            $day->save();
        }

        $maxPosition = $day->meals()->max('position');
        $position = isset($maxPosition) ? $maxPosition + 1 : 0;

        $meal = $day->meals()->create([
            'position' => $position,
        ]);

        return new MealResource($meal);
    }

    public function update(
        Request $request,
        User $user,
        Day $day,
        Meal $meal
    ): MealResource {
        ['position' => $position] = $request->validate([
            'position' => [
                'required',
                'integer',
                'gte:0',
                Rule::exists(Meal::class)
                    ->where('day_id', $day->id)
                    ->whereNot('id', $meal->id),
            ],
        ]);

        $otherMeal = $day->meals()->where('position', $position)->first();
        $otherMeal->position = $meal->position;
        $otherMeal->save();

        $meal->position = $position;
        $meal->save();

        return new MealResource($meal);
    }

    public function destroy($user, $day, Meal $meal) {
        $meal->delete();
        return response(null, 204);
    }
}
