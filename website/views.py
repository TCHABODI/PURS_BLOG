from django.shortcuts import render
from django.core.paginator import Paginator
from blog import models


# Create your views here.
def home(request):
    blogs = models.Blog.objects.all().order_by('-created_date')

    # pagination de la page d'accueil

    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'base/home.html', context=context)