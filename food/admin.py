from django.contrib import admin

from .models import Diet, Day


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    pass


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    pass
