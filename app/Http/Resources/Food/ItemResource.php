<?php

namespace App\Http\Resources\Food;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ItemResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'proteins' => $this->proteins,
            'fats' => $this->fats,
            'carbs' => $this->carbs,
            'calories' => $this->calories,
            'pieceMass' => $this->whenNotNull($this->piece_mass),
            'pieceProteins' => $this->whenNotNull($this->piece_proteins),
            'pieceFats' => $this->whenNotNull($this->piece_fats),
            'pieceCarbs' => $this->whenNotNull($this->piece_carbs),
            'pieceCalories' => $this->whenNotNull($this->piece_calories),
            'group' => new GroupResource($this->group),
        ];
    }
}
