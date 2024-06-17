from django.urls import path

from blog.views import BlogHome, BlogPostCreateView, BlogPostDetailView, BlogPostUpdateView, CategoryPostListView

#from blog.views import CoordinatorDetailView

app_name = 'blog'
urlpatterns = [

    # path('coordinator/', CoordinatorDetailView.as_view(), name='coordinator'),
    path('', BlogHome.as_view(), name='blog'),
    path('category/<int:category_id>/', CategoryPostListView.as_view(), name='category'),
    path('<str:slug>/', BlogPostDetailView.as_view(), name='post'),
    path('create/', BlogPostCreateView.as_view(), name='create'),
    path('edit/<str:slug>/', BlogPostUpdateView.as_view(), name='edit'),
]
