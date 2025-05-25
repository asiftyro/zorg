"""account/filters.py"""

import django_filters
from . import models


class AccountFilter(django_filters.FilterSet):
    """Account filter"""

    username = django_filters.CharFilter(lookup_expr="icontains", label="Username")
    full_name = django_filters.CharFilter(lookup_expr="icontains", label="Full Name")
    email = django_filters.CharFilter(lookup_expr="icontains", label="Email")
    phone = django_filters.CharFilter(lookup_expr="icontains", label="Phone")
    designation = django_filters.CharFilter(lookup_expr="icontains", label="Designation")

    is_active = django_filters.ChoiceFilter(
        choices=[
            (True, "TRUE"),
            (False, "FALSE"),
        ],
        label="Active",
    )

    last_login = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.DateRangeWidget(attrs={"type": "date"}),
        label="Last Signed In",
    )

    class Meta:
        """Meta for AccountFilter"""

        model = models.Account
        fields = [
            "username",
            "full_name",
            "email",
            "phone",
            "designation",
            "last_login",
            "is_active",
        ]
