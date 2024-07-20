<?php

namespace App\Http\Resources\Food;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class DayResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        $date = $this->date;
        $userLocale = $request->getPreferredLanguage();
        if (isset($userLocale)) {
            $date->setLocale($userLocale);
        }
        return [
            // 'id' => $this->id,
            'date' => $date,
            'prettyDate' => $date->isoFormat('L'),
            'weekDay' => $date->dayName,
            'meals' => MealResource::collection(
                $this->meals->sortBy('position')
            ),
            'mass' => $this->mass,
            'proteins' => $this->proteins,
            'fats' => $this->fats,
            'carbs' => $this->carbs,
            'calories' => $this->calories,
        ];
    }
}
