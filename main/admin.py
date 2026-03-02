from django.contrib import admin
from .models import About, Project, Contact

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Shaxsiy malumotlar', {  # o'zgartirildi: ma'lumotlar -> malumotlar
            'fields': ('full_name', 'title', 'bio', 'profile_image', 'birth_date')
        }),
        ('Kontakt', {
            'fields': ('address', 'education', 'email', 'phone', 'github')
        }),
    )
    
    def has_add_permission(self, request):
        if About.objects.exists():
            return False
        return True

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'created_date')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'description')
    list_editable = ('featured',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_date', 'is_read')
    list_filter = ('is_read',)
    readonly_fields = ('created_date',)
    list_editable = ('is_read',)
