from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from user_interface.views import create_admin

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('flavors/', views.flavors, name='flavors'),
    path('service/', views.service, name='service'),
    path('products/', views.products, name='products'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('login_registration/', views.login_registration, name='login_registration'),
    path('post_content/', views.post_content, name='post_content'),
    path('logout/', views.user_logout, name='logout'),
    path('create-admin/', create_admin),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)