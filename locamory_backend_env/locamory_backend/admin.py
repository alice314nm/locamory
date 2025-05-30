from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Memory, MemoryImage
from django.utils.safestring import mark_safe

class MemoryImageInline(admin.TabularInline):
    model = MemoryImage
    extra = 1
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;" />')
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'description', 'date', 'location_coordinates')
    inlines = [MemoryImageInline]
    list_filter = ('date',)
    search_fields = ('title', 'description')
    readonly_fields = ('user',)


    def location_coordinates(self, obj):
        return f"{obj.latitude}, {obj.longitude}"
    location_coordinates.short_description = 'Location'

    def save_model(self, request, obj, form, change):
        if not change:  # only set user on creation
            obj.user = request.user
        obj.save()


@admin.register(MemoryImage)
class MemoryImageAdmin(admin.ModelAdmin):
    list_display = ('memory', 'image_preview')
    readonly_fields = ('image_preview',)
    list_select_related = ('memory',)
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;" />')
        return "No Image"
    image_preview.short_description = 'Preview'