from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView


from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("core:home")



class EditUserView(LoginRequiredMixin, UpdateView):
    template_name = "users/update.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("core:home")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.instance != self.request.user:
            raise PermissionDenied("Вы не можете редактировать другого пользователя")
        return super().form_valid(form)



class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "users/user_details.html"

    def get_object(self, queryset=None):
        return self.request.user
