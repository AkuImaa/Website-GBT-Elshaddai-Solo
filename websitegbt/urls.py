from django.contrib import admin
from django.urls import path
from webgbt import views
from django.conf import settings
from django.conf.urls.static import static
from webgbt.views import login_user
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', views.JadwalIbadah, name='jadwalibadah'),
    path('', views.JadwalPelayanan, name='jadwalpelayanan'),
    path('', views.Renungan, name='renungan'),
    path('', views.WartaGereja, name='wartagereja'),
    path('sejarah/', views.sejarah, name='sejarah'),
        path('renungan/<int:id>/', views.renungan, name='renungan'),
        path('renungan/', views.renungan_list, name='renungan_list'),
        
        path('jadwalibadah/<int:id>/', views.jadwalibadah, name='jadwalibadah'),
        path('jadwalibadah/', views.jadwal_ibadahlist, name='jadwal_ibadahlist'),
        
        path('jadwalpelayanan/<int:id>/', views.jadwalpelayanan, name='jadwalpelayanan'),
        path('jadwalpelayanan/', views.jadwal_pelayananlist, name='jadwal_pelayananlist'),
        
        path('wartagereja/<int:id>/', views.wartagereja, name='wartagereja'),
        path('wartagereja/', views.warta_gerejalist, name='warta_gerejalist'),
        
        path('dashboard/', views.dashboard, name='dashboard'),
        path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
        path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
        
        path('komentar/', views.komentar, name='komentar'),
        path('like/<str:model_name>/<int:id>/',views.toggle_like,name='toggle_like'),
        
        path('baptis/', views.baptis, name='baptis'),
        path('download-baptis/<int:id>/', views.download_baptis, name='download_baptis'),
        path('jadwal-baptis/', views.jadwal_baptis, name='jadwal_baptis'),
        
        path('pelayan-altar/', views.pelayan_altar, name='pelayan_altar'),
        path('download-pelayan/<int:id>/',views.download_pelayan, name='download_pelayan'),
        path('data-pelayan/',views.data_pelayan,name='data_pelayan'),

        path('daftar/', views.daftar, name='daftar'),
        path('lupa-password/', views.lupa_password, name='lupa_password'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)