from django.db import models
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal

class Mobil(models.Model):
    id_mobil = models.CharField(max_length=20, primary_key=True)
    merk = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    tahun = models.PositiveIntegerField()
    harga_dasar = models.DecimalField(max_digits=15, decimal_places=2)
    tgl_pinjaman = models.DateField(null=True, blank=True)
    dana_pinjaman = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    suku_bunga = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lama_pinjaman = models.PositiveIntegerField(null=True, blank=True)
    pinjaman_lunas = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"ID {self.id_mobil}: {self.merk} {self.model}, tahun {self.tahun}"
    
    def save(self, *args, **kwargs):
        if self.dana_pinjaman:
            if self.pinjaman_lunas is None:
                self.pinjaman_lunas = False
        super().save(*args, **kwargs)

    def total_bunga(self):
        pinjaman = self.dana_pinjaman
        bunga = self.suku_bunga
        lama = self.lama_pinjaman
        if pinjaman and bunga and lama:
            lamathn = Decimal(lama) / Decimal(12)
            return (pinjaman * bunga * lamathn) / Decimal(100)
        return Decimal(0)
    
    def cicilan_perbulan(self):
        pinjaman = self.dana_pinjaman
        bunga = self.suku_bunga
        lama = self.lama_pinjaman
        if pinjaman and bunga and lama:
            total = self.total_bunga() + pinjaman
            return total / Decimal(lama)
        return Decimal(0)
    
    def hpp(self):
        dasar = self.harga_dasar
        tbunga = self.total_bunga()
        tservice = sum((service.biaya for service in self.daftar_service.all()), Decimal())
        return dasar + tbunga + tservice
    
    def akhir_pinjaman(self):
        awal = self.tgl_pinjaman
        lama = self.lama_pinjaman
        if awal and lama:
            return awal + relativedelta(months=lama)
        return None

    def status_pinjaman(self):
        akhir = self.akhir_pinjaman()
        if akhir:
            today = date.today()
            if akhir < today:
                return "Masa pinjaman berakhir"
            selisih = relativedelta(akhir, today)
            return f"{selisih.years} tahun {selisih.months} bulan {selisih.days} hari"
        return "Tidak pakai dana bank"
    
    def cek_lunas_auto(self):
        akhir = self.akhir_pinjaman()
        today = date.today()
        if akhir and not self.pinjaman_lunas and (akhir < today):
            self.pinjaman_lunas = True
            self.save()


class Service(models.Model):
    mobil = models.ForeignKey(Mobil, on_delete=models.CASCADE, related_name='daftar_service')
    tgl_service = models.DateField(default=timezone.now)
    deskripsi = models.TextField()
    biaya = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.mobil} diservice pada {self.tgl_service}, biaya Rp {self.biaya}"
