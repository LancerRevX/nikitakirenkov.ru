<?php

use App\Http\Controllers\AuthController;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Str;
use Illuminate\Validation\ValidationException;

Route::prefix('auth')->controller(AuthController::class)->group(function () {
    Route::middleware('guest')->group(function () {
        Route::post('log-in', 'logIn');
    });
    Route::middleware('auth')->group(function () {
        Route::post('log-out', 'logOut');
    });
});
