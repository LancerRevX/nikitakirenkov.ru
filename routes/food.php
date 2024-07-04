<?php

use App\Http\Resources\Food\GroupResource;
use App\Models\Food\Group;
use App\Models\Food\User;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Route;

Route::prefix('food')->group(function () {
    Route::get('groups', function() {
        return GroupResource::collection(Group::with('items')->get());
    });

    Route::get('groups/{group}', function (Group $group) {
        $group->load('items');
        return new GroupResource($group);
    });

    Route::get('days', function () {
        Auth::login(User::find(1));
        error_log(session()->id());
        $user = Auth::user();
        return $user;
    });
});