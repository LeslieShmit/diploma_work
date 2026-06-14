
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import PermissionDenied

from django.urls import reverse_lazy

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
