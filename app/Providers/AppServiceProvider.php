<?php

namespace App\Providers;

use App\Models\Day;
use Carbon\Carbon;
use Carbon\Exceptions\InvalidFormatException;
use Illuminate\Auth\Middleware\RedirectIfAuthenticated;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        JsonResource::withoutWrapping();

        RedirectIfAuthenticated::redirectUsing(function () {
            return abort(409, 'Already authenticated.');
        });

        Route::bind('day', function ($date, $field) {
            Validator::make(
                ['day' => $date],
                ['day' => 'date_format:Y-m-d']
            )->validate();
            return Day::whereDate('date', $date)->first() ??
                new Day(['date' => $date]);
        });
    }
}
