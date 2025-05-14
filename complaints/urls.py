from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import userviews
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path('',userviews.user, name='user'),
    path('create_complaint/', login_required(userviews.create_complaint), name='create_complaint'),


    

]+ static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static') + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
