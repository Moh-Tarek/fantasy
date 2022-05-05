from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout as lo
from django.shortcuts import render, redirect

def logout(request):
    lo(request)
    return redirect("/")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Fantasy.urls')),
    # path('signup/',user_views.register, name='register'),
    # path('profile/',user_views.profile, name='profile'),
    # path('login/',auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout, name='logout'),
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


