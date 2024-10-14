from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = "booking"
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('service/<int:service_id>/book/', views.book_service, name='book_service'),
    path('booking/<int:booking_id>/review/', views.review_service, name='review_service'),
    path('search/', views.search_services, name='search_services'),
    path('profile/', views.user_profile, name='user_profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
        # Login
    path('login/', views.sign_in, name="login"),
    
    # Logout
    path('logout/', views.sign_out, name="logout"),
    # Password Change
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='booking/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='booking/password_change_done.html'), name='password_change_done'),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='booking/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='booking/password_reset_done.html'), name='password_reset_done'),
    
    # Password Reset Confirm
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='booking/password_reset_confirm.html'), name='password_reset_confirm'),
    
    # Password Reset Complete
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='booking/password_reset_complete.html'), name='password_reset_complete'),
    ]
