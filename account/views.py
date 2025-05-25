"""account/views.py"""

import datetime
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.http import JsonResponse
from altcha import ChallengeOptions, create_challenge
from .models import Account
from .forms import AccountCreateForm, AccountUpdateForm, AccountSelfUpdateForm, AccountLoginForm
from .tables import AccountTable
from .filters import AccountFilter


class AccountListView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    """Account filter view."""

    permission_required = ("account.view_account",)
    model = Account
    table_class = AccountTable
    filterset_class = AccountFilter


class AccountDetailView(PermissionRequiredMixin, DetailView):
    """Account detail view."""

    permission_required = ("account.view_account",)
    model = Account


class AccountCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Account create view."""

    permission_required = ("account.add_account",)
    model = Account
    form_class = AccountCreateForm
    success_message = "User Account created."

    def get_success_url(self):
        return reverse_lazy("account:detail", kwargs={"pk": self.object.pk})


class AccountUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Account update View."""

    permission_required = ("account.change_account",)
    model = Account
    form_class = AccountUpdateForm
    success_message = "User Account updated."

    def get_success_url(self):
        return reverse_lazy("account:detail", kwargs={"pk": self.object.pk})


def captcha_challange(request):
    """Captcha challage endpoint"""
    options = ChallengeOptions(
        expires=datetime.datetime.now() + datetime.timedelta(minutes=settings.ALTCHA_EXPIRE),
        max_number=settings.ALTCHA_MAX_NUMBER,
        hmac_key=settings.ALTCHA_HMAC_KEY,
    )
    challenge = create_challenge(options)
    return JsonResponse(challenge.__dict__)


class AccountLoginView(LoginView):
    form_class = AccountLoginForm
    # redirect_authenticated_user = True

    # def get_success_url(self):
    #     return reverse_lazy("demo")

    # def form_invalid(self, form):
    #     messages.error(self.request, "Invalid username or password")
    #     return self.render_to_response(self.get_context_data(form=form))


class AccountSelfUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Account self-update view."""

    model = Account
    form_class = AccountSelfUpdateForm
    template_name = "account/account_form.html"
    success_url = reverse_lazy("account:selfupdate")
    permission_required = ("account.selfupdate_account",)
    success_message = "User Account updated."

    def get_object(self, queryset=None):
        return self.request.user  # Return the logged-in user

    def form_valid(self, form):
        response = super().form_valid(form)
        # Keep logged in
        update_session_auth_hash(self.request, self.object)
        return response
