from django.contrib import admin

from .models import Mark, Model, Part


class MarkAdmin(admin.ModelAdmin):
    """Модель марки автомобиля в админ панели"""

    list_display = ("id", "name", "producer_country_name", "is_visible")
    list_display_links = ("id", "name")
    list_editable = ("is_visible",)
    list_filter = ("name", "producer_country_name", "is_visible")
    search_fields = ("name", "producer_country_name")


class ModelAdmin(admin.ModelAdmin):
    """Модель модели автомобиля в админ панели"""

    list_display = ("id", "name", "mark", "is_visible")
    list_display_links = ("id", "name")
    list_editable = ("is_visible",)
    list_filter = ("name", "mark", "is_visible")
    search_fields = ("name", "mark")


class PartAdmin(admin.ModelAdmin):
    """Модель запчасти автомобиля в админ панели"""

    list_display = ("id", "name", "mark", "model", "price", "is_visible")
    list_display_links = ("id", "name")
    list_editable = ("is_visible",)
    list_filter = ("name", "mark", "model", "is_visible")
    search_fields = ("name", "mark", "model")


admin.site.register(Mark, MarkAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Part, PartAdmin)
