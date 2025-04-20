from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mobil, Service
from .forms import FormMobil, FormService

# Create your views here.
def homepage(request):
    daftar_mobil = Mobil.objects.all()
    return render(request, 'showroom/homepage.html', {'daftar_mobil': daftar_mobil})

def tambah_mobil(request):
    if request.method == 'POST':
        form = FormMobil(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data mobil berhasil ditambahkan!")
            return redirect('homepage')
        else:
            messages.error(request, "Gagal menyimpan data. Periksa kembali data input!")
    else:
        form = FormMobil()
    return render(request, 'showroom/formmobil.html', {'form': form})

def detail_mobil(request, id_mobil):
    mobil = get_object_or_404(Mobil, id_mobil=id_mobil)
    mobil.cek_lunas_auto()
    services = Service.objects.filter(mobil=mobil).order_by('-tgl_service')
    return render(request, 'showroom/detailmobil.html', {'mobil': mobil, 'services': services})

def tandai_lunas(request, id_mobil):
    mobil = get_object_or_404(Mobil, id_mobil=id_mobil)
    mobil.pinjaman_lunas = True
    mobil.save()
    messages.success(request, f'Pinjaman ditandai lunas!')
    return redirect('detail_mobil', id_mobil=id_mobil)

def hapus_mobil(request, id_mobil):
    mobil = get_object_or_404(Mobil, id_mobil=id_mobil)
    if request.method == 'POST':
        mobil.delete()
        messages.success(request, f'Mobil {id_mobil} berhasil dihapus!')
    return redirect('homepage')

def tambah_service(request, id_mobil=None):
    referer = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        form = FormService(request.POST)
        if form.is_valid():
            service = form.save()
            messages.success(request, "Data service berhasil ditambahkan!")
            if id_mobil:
                return redirect('detail_mobil', id_mobil=id_mobil)
            elif service.mobil:
                return redirect('detail_mobil', id_mobil=service.mobil.id_mobil)                
            else:
                return redirect('homepage')
        else:
            messages.error(request, "Gagal menyimpan data. Periksa kembali data input!")
    else:
        if id_mobil:
            form = FormService(initial={'mobil': id_mobil})
        else:
            form = FormService()
    return render(request, 'showroom/service.html', {'form': form, 'referer': referer})

def hapus_service(request, id):
    service = get_object_or_404(Service, id=id)
    id_mobil = service.mobil.id_mobil
    if request.method =='POST':
        service.delete()
        messages.success(request, 'Data service berhasil dihapus!')
    return redirect('detail_mobil', id_mobil=id_mobil)
