from django.urls import include, path
from classroom import views
from django.contrib import admin
from classroom import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('pay/<int:pk>', views.Pay, name='pay'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('save_vehicle/', views.save_vehicle, name='save_vehicle'),
    path('logout/', views.logout_view, name='logout'),
    path('vehicle/', views.Vehicle.as_view(), name='vehicle'),
    path('users/', views.UserView.as_view(), name='users'),
    path('listvehicle/', views.ListVehicle.as_view(), name='listvehicle'),
    path('view_vehicle/<int:pk>', views.VehicleReadView.as_view(), name='view_vehicle'),
    path('view_car/<int:pk>', views.CarReadView.as_view(), name='view_car'),
    path('view_user/<int:pk>', views.UserReadView.as_view(), name='view_user'),
    path('update_vehicle/<int:pk>', views.VehicleUpdateView.as_view(), name='update_vehicle'),
    path('update_vehicle2/<int:pk>', views.CarUpdateView.as_view(), name='update_car'),
    path('delete_vehicle/<int:pk>', views.VehicleDeleteView.as_view(), name='delete_vehicle'),
    path('delete_vehicle2/<int:pk>', views.CarDeleteView.as_view(), name='delete_car'),
    path('invoice/<int:pk>', views.GeneratePdf.as_view(), name='invoice'),
    path('user_update/<int:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('delete_user/<int:pk>', views.DeleteUser.as_view(), name='delete_user'),
    path('create/create', views.create, name='create'),
    path('vehicle_pdf/', views.ViewPdf.as_view(), name='vehicle_pdf'),
    path('pending_pdf/', views.PendingPdf.as_view(), name='pending_pdf'),
    path('search_item', views.search_item, name='search_item'),
    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name='dashboard/password_reset.html'), 
        name= 'reset_password'),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name='dashboard/password_reset_sent.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'),
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='dashboard/password_reset_done.html'), 
        name='password_reset_complete'),
]
