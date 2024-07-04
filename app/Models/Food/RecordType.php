<?php

namespace App\Models\Food;

enum RecordType: string {
    case Mass = 'mass';
    case Pieces = 'pieces';
}