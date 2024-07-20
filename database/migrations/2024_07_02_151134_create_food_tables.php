<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

use App\Models\Food\RecordType;

return new class extends Migration {
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('food_diets', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->string('name');
            $table->double('min_proteins')->nullable();
            $table->double('min_fats')->nullable();
            $table->double('min_carbs')->nullable();
            $table->double('min_calories')->nullable();
            $table->double('max_proteins')->nullable();
            $table->double('max_fats')->nullable();
            $table->double('max_carbs')->nullable();
            $table->double('max_calories')->nullable();
        });

        Schema::table('days', function (Blueprint $table) {
            $table->foreignId('diet_id')->nullable()->constrained('diets');
        });

        // many-to-many pivot table
        Schema::create('food_coach_client', function (Blueprint $table) {
            $table->id();
            $table->foreignId('coach_id')->constrained('users');
            $table->foreignId('client_id')->constrained('users');   
        });

        // Examples: Bellini, Перцы, Овощи, Сладкое, Протеиновые батончики, Напитки
        Schema::create('food_groups', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained();
            $table->timestamps();
            $table->string('name');
            $table->string('color', 6)->default('ffffff');
        });

        // Example: Блинчики с творогом
        Schema::create('food_items', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->foreignId('group_id')->constrained('food_groups');
            $table->string('name');
            $table->double('proteins');
            $table->double('fats');
            $table->double('carbs');
            $table->double('calories');
            $table->double('piece_mass')->nullable();
        });

        // allows adding personal notes as well as disscussing the diet with a coach
        Schema::create('food_comments', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->foreignId('day_id')->constrained();
            $table->foreignId('user_id')->constrained();
            $table->text('text');
        });

        // Example: Обед
        Schema::create('food_meals', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->foreignId('day_id')->constrained();
            $table->integer('position');
        });

        // Example: Блинчики с творогом 1 шт.
        Schema::create('food_records', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->foreignId('meal_id')->constrained('food_meals');
            $table->foreignId('item_id')->constrained('food_items');
            $table->enum('type', array_column(RecordType::cases(), 'value'));
            $table->integer('value');
            $table->integer('position');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('food_tables');
    }
};
