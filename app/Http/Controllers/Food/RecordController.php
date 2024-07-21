<?php

namespace App\Http\Controllers\Food;

use App\Http\Controllers\Controller;
use App\Http\Resources\Food\RecordResource;
use App\Models\Food\Record;
use Illuminate\Http\Request;

class RecordController extends Controller
{
    public function show($user, $day, $meal, Record $record): RecordResource
    {
        return new RecordResource($record);
    }

    public function store($user, $day, Meal $meal): RecordResource
    {
        $maxPosition = $meal->records()->max('position');
        $position = isset($maxPosition) ? $maxPosition + 1 : 0;
        $record = $meal->records()->create([]);
    }
}
