<?php

namespace App\Http\Resources\Food;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class RecordResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'item' => new ItemResource($this->item),
            'type' => $this->type,
            'value' => $this->value,
            'mass' => $this->mass,
            'proteins' => $this->proteins,
            'fats' => $this->fats,
            'carbs' => $this->carbs,
            'calories' => $this->calories,
        ];
    }
}
