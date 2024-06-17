from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView

from blog import models
from website.models import coordinator


# Create your views here.
def home(request):
    blogs = models.Blog.objects.all().order_by('-created_date')

    # pagination de la page d'accueil

    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'base/home.html', context=context)

class CurrentCoordinatorView(ListView):
    model = coordinator
    template_name = 'coordinator/current_coordinator.html'
    context_object_name = 'coordinator'

    def get_queryset(self):
        return coordinator.objects.filter(is_current=True)