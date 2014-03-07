from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from recipes.models import Rating, Recipe, RecipeTag


class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'rated_by', 'vote')


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ['popularity', 'likes', 'dislikes', 'slug']
    formfield_overrides = {models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 
                                                                       'rows': 15})}}

 
admin.site.register(Rating, RatingAdmin)    
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag)
