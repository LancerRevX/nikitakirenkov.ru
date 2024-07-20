<?php

use App\Http\Resources\Food\DayResource;
use App\Http\Resources\Food\GroupResource;
use App\Http\Resources\Food\DayCollection;
use App\Models\Day;
use App\Models\Food\Group;
use App\Models\Food\Meal;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Route;
use Illuminate\Validation\Rule;

Route::prefix('users/{user}/food')
    ->middleware('auth')
    ->group(function () {
        Route::get('groups', function () {
            return GroupResource::collection(Group::with('items')->get());
        });

        Route::get('groups/{group}', function (Group $group) {
            $group->load('items');
            return new GroupResource($group);
        });

        Route::get('days', function (Request $request, User $user) {
            $request->validate([
                'from' => ['required', 'date'],
                'to' => ['required', 'date'],
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
        })->name('days.index');

        Route::post('days/{date}/meals', function (User $user, string $date) {
            $day = $user->days()->whereDate('date', $date)->first();
            if (is_null($day)) {
                $day = $user->days()->create(['date' => $date]);
            }


        });

        Route::patch('days/{day}/meals/{meal}', function (Meal $meal) {
        });
    });
