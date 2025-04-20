from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('tambah/', views.tambah_mobil, name='tambah_mobil'),
    path('mobil/<str:id_mobil>/', views.detail_mobil, name='detail_mobil'),
    path('tambah_service/', views.tambah_service, name='tambah_service_hm'),
    path('mobil/<str:id_mobil>/tambah_service/', views.tambah_service, name='tambah_service_dt'),
    path('tandai_lunas/<str:id_mobil>/', views.tandai_lunas, name='tandai_lunas'),
    path('hapus_mobil/<str:id_mobil>/', views.hapus_mobil, name='hapus_mobil'),
    path('hapus_service/<int:id>/', views.hapus_service, name='hapus_service'),
]
