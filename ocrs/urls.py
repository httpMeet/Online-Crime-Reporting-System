from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import settings
from . import views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('index/', views.index, name='index'),
    path('administrator/', views.administrator, name='administrator'),
    path('user/', include('complaints.urls'), name='user'),
    path('police/', views.police, name='police'),
    path('test/', views.test, name='test'),
    path('get_district/', views.get_districts, name='get_districts'),
    path('get_police_stations/', views.get_police_stations, name='get_police_stations'),
    path('get_districts_register/', views.get_districts_register, name='get_districts_register'),
    path('police_incharge_home/', views.police_incharge_home, name='police_incharge_home'),

    path('view_announcements/', views.view_announcements, name='view_announcements'),
    path('view_announcement/<int:id>/', views.view_announcement, name='view_announcement'),

    path('user_announcements/', views.user_announcements, name='user_announcements'),
    path('user_announcement/<int:id>/', views.user_announcement, name='user_announcement'),

    path('police_announcements/', views.police_announcements, name='police_announcements'),
    path('police_announcement/<int:id>/', views.police_announcement, name='police_announcement'),
    

    path('manage_complaint/<int:complaint_id>/', views.manage_complaint, name='manage_complaint'),
    path('police_incharge_view_complaint/', views.police_incharge_view_complaint, name='police_incharge_view_complaint'),
    path('register_fir_csr/', views.register_fir_csr, name='register_fir_csr'),
    path('view_fir/', views.view_fir, name='view_fir'),
    path('manage_fir/<int:fir_id>/', views.manage_fir, name='manage_fir'),
    path('view_csr/', views.view_csr, name='view_csr'),
    path('manage_csr/<int:csr_id>/', views.manage_csr, name='manage_csr'),
    path('view_only_fir/<int:fir_id>/', views.view_only_fir, name='view_only_fir'),
    path('view_only_csr/<int:csr_id>/', views.view_only_csr, name='view_only_csr'),
    path('view_only_firs/', views.view_only_firs, name='view_only_firs'),
    path('view_only_csrs/', views.view_only_csrs, name='view_only_csrs'),
    path('user_view_complaints/', views.user_view_complaints, name='user_view_complaints'),
    path('user_view_complaint/<int:complaint_id>/', views.user_view_complaint, name='user_view_complaint'),
    path('user_view_firs/', views.user_view_firs, name='user_view_firs'),
    path('user_view_fir/<int:fir_id>/', views.user_view_fir, name='user_view_fir'),
    path('user_view_csrs/', views.user_view_csrs, name='user_view_csrs'),
    path('user_view_csr/<int:csr_id>/', views.user_view_csr, name='user_view_csr'),

    path('police_view_only_firs/', views.police_view_only_firs, name='police_view_only_firs'),
    path('police_view_only_fir/<int:fir_id>/', views.police_view_only_fir, name='police_view_only_fir'),
    path('police_manage_firs/', views.police_manage_firs, name='police_manage_firs'),
    path('police_manage_fir/<int:fir_id>/', views.police_manage_fir, name='police_manage_fir'),

    path('police_view_only_csrs/', views.police_view_only_csrs, name='police_view_only_csrs'),
    path('police_view_only_csr/<int:csr_id>/', views.police_view_only_csr, name='police_view_only_csr'),
    path('police_manage_csrs/', views.police_manage_csrs, name='police_manage_csrs'),
    path('police_manage_csr/<int:csr_id>/', views.police_manage_csr, name='police_manage_csr'),
    path('user_manage_profile/', views.user_manage_profile, name='user_manage_profile'),
    path('police_incharge_manage_profile/', views.police_incharge_manage_profile, name='police_incharge_manage_profile'),
    path('police_manage_profile/', views.police_manage_profile, name='police_manage_profile'),


    path('view_complaints_for_feedbacks/', views.view_complaints_for_feedbacks, name='view_complaints_for_feedbacks'),
    path('feedback/<int:id>/<str:type>/', views.feedback, name='feedback')


] + static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static') + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)