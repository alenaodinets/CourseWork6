from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from blog.models import Blog


# Create your views here.
class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    fields = ('title', 'content', 'image',)
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'content', 'image', 'is_published',)
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def get_success_url(self):
        return reverse_lazy('blog:blog_list')


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"
