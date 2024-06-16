import random

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from main.forms import SendingForm, MessageForm, ClientForm, SendingModerationForm
from main.models import Sending, Client, Attempt, Message


# Create your views here.
class HomeView(ListView):
    model = Sending
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['sendings_count'] = Sending.objects.all().count()
        context_data['active_sendings_count'] = Sending.objects.filter(is_active=True).count()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        context_data['clients_count'] = Client.objects.all().count()
        return context_data


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = 'sending_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = 'attempt_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        attempts = Attempt.objects.all()
        context_data['attempts'] = attempts
        return context_data


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class SendingDetailView(DetailView):
    model = Sending
    template_name = 'sending_detail.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['clients'] = list(self.object.clients.all())
        return context_data


class MessageDetailView(DetailView):
    model = Message
    template_name = 'message_detail.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client_detail.html'


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy('sending_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy('main:sending_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class SendingDeleteView(LoginRequiredMixin, DeleteView):
    model = Sending
    success_url = reverse_lazy('main:sending_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class SendingModerationView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingModerationForm
    template_name = 'sending_form.html'
    permission_required = ('main.set_active',)

    def get_success_url(self):
        return reverse_lazy('sending_detail', kwargs={'pk': self.object.pk})
