from django.contrib import admin
from recipe.models import Recipe, RecipeComment

admin.site.register((RecipeComment))


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    class Media:
        js= ('js/tinyInject.js')