<?php

use App\Http\Controllers\Food\DayController;
use App\Http\Controllers\Food\MealController;
use App\Http\Controllers\Food\RecordController;
use App\Http\Resources\Food\DayResource;
use App\Http\Resources\Food\GroupResource;
use App\Http\Resources\Food\DayCollection;
use App\Models\Day;
use App\Models\Food\Group;
use App\Models\Food\Meal;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::prefix('users/{user}/food')
    ->middleware('auth')
    ->scopeBindings()
    ->namespace('food.')
    ->group(function () {
        Route::get('groups', function () {
            return GroupResource::collection(Group::with('items')->get());
        });

        Route::get('groups/{group}', function (Group $group) {
            $group->load('items');
            return new GroupResource($group);
        });

        Route::controller(DayController::class)->group(function () {
            Route::get('days', 'index');
            Route::get('days/{day}', 'show');
        });

        Route::controller(MealController::class)
            ->prefix('days/{day}/meals')
            ->group(function () {
                Route::post('', 'store');
                Route::patch('{meal}', 'update');
                Route::delete('{meal}', 'destroy');
            });

        Route::controller(RecordController::class)
            ->prefix('days/{day}/meals/{meal}/records')
            ->group(function () {
                Route::post('', 'store');
                Route::get('{record}', 'show');
                Route::patch('{record}', 'update');
                Route::delete('{record}', 'destroy');
            });
    });
