from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import request
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from blog.forms import BlogPostForm
from blog.models import Blog, Category


class BlogHome(ListView):
    model = Blog
    context_object_name = 'posts'
    template_name = 'blog/blogpost_list.html'  # Chemin du template pour afficher la liste des articles
    paginate_by = 6
    def get_queryset(self):
        queryset = super().get_queryset()
        page_number = self.request.GET.get("page", None)
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Blog.objects.filter(published=True).order_by('-created_on')[:3]
        context['categories'] = Category.objects.all()
        return context

# Vue pour le détail d'un article
class BlogPostDetailView(DetailView):
    model = Blog
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context

class BlogPostUpdateView(UpdateView):
    model = Blog
    template_name = 'posts/blogpost_edit.html'
    fields = ['title', 'content', 'published','main_image']


class BlogPostImageFormSet:
    pass


class BlogPostCreateView(CreateView):
    model = Blog
    form_class = BlogPostForm
    template_name = 'posts/blogpost_create.html'
    success_url = reverse_lazy('blogpost_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['images'] = BlogPostImageFormSet(self.request.POST, self.request.FILES)
        else:
            data['images'] = BlogPostImageFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        self.object = form.save()
        if images.is_valid():
            images.instance = self.object
            images.save()
        return super().form_valid(form)


# class CoordinatorDetailView(DetailView):
#     model = coordinator
#     context_object_name = 'coordinator'

class CategoryPostListView(ListView):
    model = Blog
    context_object_name = 'posts'
    template_name = 'blog/category_post_list.html'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        queryset = Blog.objects.filter(category=self.category, published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context