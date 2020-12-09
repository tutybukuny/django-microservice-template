from django.contrib import admin

from apps.users.models import User


class AppUserAdmin(admin.ModelAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    list_display = [
        "id",
        "username",
        "fullname",
        "phone",
        "ascii_name",
    ]
    list_filter = ["is_superuser"]
    filter_horizontal = []



admin.site.register(User, AppUserAdmin)
