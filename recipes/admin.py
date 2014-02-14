from aloha.widgets import AlohaWidget
from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from recipes.models import Recipe, RecipeTag


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ['popularity', 'slug']
    formfield_overrides = {models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 
                                                                       'rows': 15})}}


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag)