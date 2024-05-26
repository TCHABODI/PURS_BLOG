from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
import authentication

app_name = 'authentication'

urlpatterns = [
    path('', LoginView.as_view(template_name = 'authentication/login.html',redirect_authenticated_user =True), name='login'),
    #path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    #path('logout/', authentication.views.logout_user, name='logout'),
    path('change-password/', PasswordChangeView.as_view(template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
            template_name='authentication/password_change_done.html'),
             name='password_change_done'
             ),
    ]