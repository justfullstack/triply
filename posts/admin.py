from django.contrib import admin
from . import models


class CustomPostAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    #list_filter = ('is_active', 'is_admin', 'is_staff')

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'group'
            )
        }
        ),

        ('Content', {
            'fields': (
                'text',
            )
        }
        ),





    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None,
         {
             'fields': (
                 'user',
                 'text',
             )
         },
         ),
    )

    list_display = (
        "user",
        "text",
        "date_created",
        "date_last_edited",
    )

    search_fields = (
        "user",
    )

    ordering = ("date_created",)
    filter_horizontal = ()


admin.site.register(models.Post, CustomPostAdmin)
admin.site.register(models.Image)
admin.site.register(models.Comment)
admin.site.register(models.CommentReply)
