<?php

use App\Http\Controllers\Food\DayController;
use App\Http\Controllers\Food\MealController;
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
    ->group(function () {
        Route::get('groups', function () {
            return GroupResource::collection(Group::with('items')->get());
        });

        Route::get('groups/{group}', function (Group $group) {
            $group->load('items');
            return new GroupResource($group);
        });

        Route::controller(DayController::class)->group(function () {
            Route::get('days', 'index')->name('days.index');
            Route::get('days/{day}', 'show')->name('days.show');
        });

        Route::controller(MealController::class)->group(function () {
            Route::post('days/{day}/meals', 'store')->name('meals.store');
            Route::patch('days/{day}/meals/{meal}', 'update')->name(
                'meals.update'
            );
            Route::delete('days/{day}/meals/{meal}', 'destroy')->name(
                'meals.destroy'
            );
        });

        
    });
