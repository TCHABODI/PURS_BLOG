from django.urls import path

from website.views import CurrentCoordinatorView

app_name = 'website'
urlpatterns = [
    path('current-coordinator/', CurrentCoordinatorView.as_view(), name='current_coordinator'),

]
