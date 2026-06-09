from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from .models import JadwalIbadah, JadwalPelayanan, WartaGereja, Renungan, Komentar, Simpan, Suka, DataPelayanAltar, Baptis, PelayanAltar

admin.site.register(JadwalIbadah)
admin.site.register(JadwalPelayanan)
admin.site.register(WartaGereja)
admin.site.register(Renungan)
admin.site.register(Komentar) 
admin.site.register(Simpan) 
admin.site.register(Suka)
admin.site.unregister(Group)
admin.site.register(Baptis)
admin.site.register(PelayanAltar)
admin.site.register(DataPelayanAltar)