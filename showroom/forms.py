from django import forms
from .models import Mobil, Service
import random
import string

class FormMobil(forms.ModelForm):
    class Meta:
        model = Mobil
        fields = '__all__'
        widgets = {
            'id_mobil': forms.TextInput(attrs={'class': 'form-control'}),
            'merk': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'tahun': forms.NumberInput(attrs={'class': 'form-control'}),
            'harga_dasar': forms.NumberInput(attrs={'class': 'form-control'}),
            'tgl_pinjaman': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dana_pinjaman': forms.NumberInput(attrs={'class': 'form-control'}),
            'suku_bunga': forms.NumberInput(attrs={'class': 'form-control'}),
            'lama_pinjaman': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(FormMobil, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            jumlah = Mobil.objects.count() + 1
            huruf = ''.join(random.choices(string.ascii_uppercase, k=2))
            id_auto = f"M-{jumlah}-{huruf}"
            self.fields['id_mobil'].initial = id_auto

    def clean(self):
        cleaned = super().clean()
        dana = cleaned.get('dana_pinjaman')
        bunga = cleaned.get('suku_bunga')
        lama = cleaned.get('lama_pinjaman')
        tgl = cleaned.get('tgl_pinjaman')
        if dana:
            if not bunga or not lama or not tgl:
                raise forms.ValidationError("Jika menggunakan dana bank, informasi pinjaman harus diisi semua.")
        return cleaned


class FormService(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'mobil': forms.Select(attrs={'class': 'form-control'}),
            'tgl_service': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'biaya': forms.NumberInput(attrs={'class': 'form-control'}),
        }