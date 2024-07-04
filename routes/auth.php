<?php

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Route;

Route::prefix('auth')->group(function () {
    Route::middleware('guest')->group(function () {
        Route::post('log-in', function (Request $request) {
            error_log($request->session()->get('key'));
            Auth::login(User::find(1));
            return response('successfully logged in', 200)->cookie(
                cookie('name', 'value', 120)
            );
        });
    });
});
