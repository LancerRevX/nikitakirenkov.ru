<?php

namespace App\Http\Resources\Food;

use App\Http\Resources\Food\MealResource;
use App\Models\Day;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\App;
use Illuminate\Support\Facades\Request as FacadesRequest;

class DayCollection extends ResourceCollection
{
    protected ?Carbon $from = null;
    protected ?Carbon $to = null;

    /**
     * Transform the resource collection into an array.
     *
     * @return array<int|string, mixed>
     */
    public function toArray(Request $request): array
    {
        $this->from ??= $this->collection->min('date');
        $this->to ??= $this->collection->max('date');

        $date = $this->from->copy();
        $result = new Collection();

        while ($date <= $this->to) {
            $day = $this->collection->where('date', $date)->first();
            if (is_null($day)) {
                $day = new Day(['date' => $date->copy()]);
            }
            $result->push($day);
            $date->addDay();
        }

        return DayResource::collection($result)->toArray($request);
    }

    public function from(Carbon $from): static
    {
        $this->from = $from;
        return $this;
    }

    public function to(Carbon $to): static
    {
        $this->to = $to;
        return $this;
    }

    protected function dateToArray(Carbon $date): array
    {
        return [
            'date' => $date->toDateString(),
            'prettyDate' => $date->toFormattedDateString(),
            'weekDay' => $date->format('l'),
        ];
    }
}
