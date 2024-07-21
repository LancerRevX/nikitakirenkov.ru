<?php

namespace App\Http\Controllers\Food;

use App\Http\Controllers\Controller;
use App\Http\Resources\Food\DayCollection;
use App\Http\Resources\Food\DayResource;
use App\Models\Day;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Http\Request;

class DayController extends Controller
{
    public function index(Request $request, User $user): DayCollection
    {
        $request->validate([
            'from' => ['required', 'date_format:Y-m-d'],
            'to' => ['required', 'date_format:Y-m-d'],
        ]);
        $from = new Carbon($request->from);
        $to = new Carbon($request->to);

        if ($from->diffInDays($to) > 31) {
            abort(413, 'The time span is too large');
        }

        $days = $user
            ->days()
            ->whereDate('date', '>=', $from)
            ->whereDate('date', '<=', $to)
            ->get();

        return DayCollection::make($days)->from($from)->to($to);
    }

    public function show(User $user, Day $day): DayResource
    {
        return new DayResource($day);
    }
}
