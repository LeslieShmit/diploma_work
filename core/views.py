from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Feedback, TeamMember

class HomePageView(TemplateView):
    template_name = "core/home.html"

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        Feedback.objects.create(
            name=name,
            phone_number=phone,
            message=message,
        )

        send_mail(
            subject="Новое сообщение с сайта",
            message=f"""
        Имя: {name}
        Телефон: {phone}

        Сообщение:
        {message}
        """,
            from_email="noreply@restaurant.local",
            recipient_list=["restaurant@example.com"],
        )

        return HttpResponse(
            f'{name}, спасибо за сообщение!'
        )

class AboutUsView(ListView):
    model = TeamMember
    context_object_name = 'team_members'
    template_name = 'core/about_us.html'
    ordering = ['last_name']
    paginate_by = 5