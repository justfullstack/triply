from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as django_group, User as django_user
from django.utils.html import format_html
from .models import CustomUser


class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'password'
            )
        }
        ),

        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
            )
        }
        ),

        ('Photos', {
            'fields': (
                'avatar',
                'cover',
            )
        }
        ),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_superuser',
                'is_admin',
            )
        }
        ),

        ('Important Dates', {
            'fields': (
                'last_login',


            )
        }
        ),


    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None,
         {'classes': ('wide',),
          'fields': (
             'username',
             'email',
             'password1',
             'password2',
             'first_name',
             'last_name'
         )
         },
         ),
    )

    list_display = (
        'username',
        "email",
        "first_name",
        "last_name",
        'avatar',
        'cover',
        'is_active',
        'is_admin'
    )

    list_editable = ('avatar',  'cover')

    list_filter = ('is_active', 'is_admin', )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name"
    )

    filter_horizontal = []

    ordering = ("username", "email",)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug"]

    # This is required for get_readonly_fields to work

    def get_prepopulated_fields(self, request, obj):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}

    def avatar_tag(self, obj):
        """
        this function returns HTML for the first column defined
        in the list_display property above

        """

        if obj.avatar:
            return format_html(f"<img src='{obj.avatar.url}'  width='300px'  height='300px' style='border-radius: 50%;'   / >")

        return "-"

    def cover_tag(self, obj):
        """
        this function returns HTML for the first column defined
        in the list_display property above

        """

        if obj.cover:
            return format_html(f"<img src='{obj.cover.url}' width='300px'  height='300px' style='border-radius: 50%;'   / >")

        return "-"


admin.site.register(django_user)
# admin.site.unregister(django_user)
admin.site.unregister(django_group)
admin.site.register(CustomUser, CustomUserAdmin)
