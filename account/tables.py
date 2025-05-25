"""account/tables.py"""

import django_tables2
from . import models


class AccountTable(django_tables2.Table):
    """Account table"""

    actions = django_tables2.TemplateColumn(
        template_code="""
            {% autoescape off %}
            <div class="btn-group btn-group btn-group-xs">
                <a class='btn btn-xs btn-outline-primary' title='Detail'
                   href="{% url 'account:detail' record.id %}"><i class='bi bi-tv'></i></a>
                <a class='btn btn-xs btn-outline-info' title='Update'
                   href="{% url 'account:update' record.id %}"><i class='bi bi-pencil-square'></i></a>
            </div>
            {% endautoescape %}
            """,
        orderable=False,
        verbose_name="Actions",
        attrs={
            "td": {
                "class": "text-center",
            },
        },
    )

    class Meta:
        """Meta for AccountTable"""

        model = models.Account
        fields = (
            "username",
            "full_name",
            "email",
            "phone",
            "designation",
            "is_active",
            "last_login",
        )
        per_page = 100
        template_name = "django_tables2/bootstrap5-responsive.html"
