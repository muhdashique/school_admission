from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Parent

admin.site.register(Student)
admin.site.register(Parent)







from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import SchoolInfo

class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'affiliation', 'edit_link']

    def edit_link(self, obj):
        url = reverse("add_school_info")
        return format_html('<a href="{}">Edit School Info</a>', url)

    edit_link.short_description = "Edit"

# Unregister first if already registered
if SchoolInfo in admin.site._registry:
    admin.site.unregister(SchoolInfo)

admin.site.register(SchoolInfo, SchoolInfoAdmin)

