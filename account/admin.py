"""account/admin.py"""

from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from .models import Account

admin.site.register(Account, SimpleHistoryAdmin)

# from django.contrib.auth.admin import UserAdmin

# fix it
# from .forms import AppUserCreationForm, AppUserChangeForm


# class AccountAdmin(UserAdmin):
#     """AppUserAdmin"""

#     # add_form = AppUserCreationForm # fix it
#     # form = AppUserChangeForm # fix it
#     model = Account
#     list_display = (
#         "username",
#         "email",
#         "phone",
#         "is_staff",
#         "is_active",
#     )
#     list_filter = (
#         "username",
#         "email",
#         "phone",
#         "is_staff",
#         "is_active",
#     )

#     # Edit form in admin panel
#     fieldsets = (
#         (None, {"fields": ("username", "email", "phone", "password")}),
#         (
#             "Permissions",
#             {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
#         ),
#     )
#     # Create form in admin panel
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "username",
#                     "email",
#                     "phone",
#                     "password1",
#                     "password2",
#                     "is_staff",
#                     "is_active",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#     )
#     search_fields = ("username",)
#     ordering = ("username",)
