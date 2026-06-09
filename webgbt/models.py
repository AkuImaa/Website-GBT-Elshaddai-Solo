from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Class JadwalIbadah    
class JadwalIbadah(models.Model):
    nama= models.CharField(max_length=100)
    class Meta:
       verbose_name = "Jadwal Ibadah"
       verbose_name_plural = "Jadwal Ibadah"
    JENIS_IBADAH = [
        ('minggu', 'Ibadah Minggu'),
        ('komsel', 'komsel'),
        ('pondok daud', 'Pondok Daud'),
        ('hari besar', 'Ibadah Hari Besar'),
        ('ibadah anak', 'Ibadah Anak'),
    ]

    nama= models.CharField(max_length=100)

    jenis_ibadah = models.CharField(
        max_length=20,
        choices=JENIS_IBADAH,
        default='minggu'
    )
    gambar = models.ImageField(upload_to='galeri/', null=True, blank=True)
    tanggal = models.DateTimeField()
    tempat = models.CharField(max_length=100)
      
    def __str__(self):
     	return "{}".format(self.nama)

# Class JadwalPelayanan        
class JadwalPelayanan(models.Model):
    JENIS_IBADAH = [
        ('minggu', 'Ibadah Minggu'),
        ('komsel', 'komsel'),
        ('pondok daud', 'Pondok Daud'),
        ('hari besar', 'Ibadah Hari Besar'),
        ('ibadah anak', 'Ibadah Anak'),
    ]

    nama= models.CharField(max_length=100)
    
    class Meta:
       verbose_name = "Jadwal Pelayanan"
       verbose_name_plural = "Jadwal Pelayanan"

    jenis_ibadah = models.CharField(
        max_length=20,
        choices=JENIS_IBADAH,
        default='minggu'
    )
    tanggal = models.DateTimeField()
    pembawa_firman = models.CharField(max_length=50, default= 'belum ditentukan')
    worship_leader = models.CharField(max_length=50, default= 'belum ditentukan')
    singer = models.CharField(max_length=100, default= 'belum ditentukan')
    keyboardis = models.CharField(max_length=50, default= 'belum ditentukan')
    gitaris = models.CharField(max_length=50, default= 'belum ditentukan')
    bassist = models.CharField(max_length=50, default= 'belum ditentukan')
    kajon_atau_drum = models.CharField(max_length=50, default= 'belum ditentukan')
    multimedia = models.CharField(max_length=50, default= 'belum ditentukan')
    
    def __str__(self):
       return "{}".format(self.nama)

# Class WartaGereja
class WartaGereja(models.Model):
    judul = models.CharField(max_length=200)
    class Meta:
       verbose_name = "Warta Gereja"
       verbose_name_plural = "Warta Gereja"
    tanggal = models.DateTimeField(auto_now_add=True)
    isi = models.TextField()
    
    
    def __str__(self):
       return "{}".format(self.judul)

# Class Renungan
class Renungan(models.Model):
    judul = models.CharField(max_length=200)
    gambar = models.ImageField(upload_to='galeri/', null=True, blank=True)
    class Meta:
       verbose_name = "Renungan"
       verbose_name_plural = "Renungan"
    perikop = models.CharField(max_length=200, default= 'belum ditentukan')
    isi = models.TextField()
    
    def __str__(self):
        return "{}".format(self.judul)

#Class Komentar
class Komentar(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    isi = models.TextField()

    dibuat_pada = models.DateTimeField(
        auto_now_add=True
    )

    # untuk balasan komentar
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='balasan'
    )

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"
        ordering = ['-dibuat_pada']

    def __str__(self):
        if self.parent:
            return f"Balasan {self.user.username}"
        return f"{self.user.username} - {self.isi[:20]}"

# Class Suka       
class Suka(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Suka"
        verbose_name_plural = "Suka"
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    konten_object = GenericForeignKey('content_type', 'object_id')

    suka_pada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} menyukai {self.konten_object}"

# Class Simpan        
class Simpan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Simpan"
        verbose_name_plural = "Simpan"
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    konten_object = GenericForeignKey('content_type', 'object_id')

    disimpan_pada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} menyimpan {self.konten_object}"
        
from django.db import models

#class baptis
class Baptis(models.Model):

    JENIS_KELAMIN = (
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    )

    STATUS = (
        ('draft', 'Draft'),
        ('diterima', 'Diterima'),
    )

    nama = models.CharField(max_length=100)

    tempat_lahir = models.CharField(max_length=100)

    tanggal_lahir = models.DateField()

    jenis_kelamin = models.CharField(
        max_length=20,
        choices=JENIS_KELAMIN
    )

    alamat = models.TextField()

    no_hp = models.CharField(max_length=15)

    # JADWAL BAPTIS
    jadwal_baptis = models.DateField(
        null=True,
        blank=True
    )

    # LOKASI
    lokasi_baptis = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='draft'
    )

    def __str__(self):
        return self.nama

#JoinPelayanan
class PelayanAltar(models.Model):

    JENIS_KELAMIN = (
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    )
    BIDANG_PELAYANAN = (
        ('Worship Leader', 'Worship Leader'),
        ('Singer', 'Singer'),
        ('Music', 'Music'),
        ('Multimedia', 'Multimedia'),
        ('Usher', 'Usher'),
        ('Doa', 'Doa'),
        ('Tamborin', 'Tamborin'),
        ('Sekolah Minggu', 'Sekolah Minggu'),
    )
    nama = models.CharField(max_length=100)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(
        max_length=20,
        choices=JENIS_KELAMIN
    )

    alamat = models.TextField()

    no_hp = models.CharField(max_length=15)

    bidang_pelayanan = models.CharField(
        max_length=50,
        choices=BIDANG_PELAYANAN
    )
    pengalaman = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

class DataPelayanAltar(models.Model):

    BIDANG_PELAYANAN = (
        ('Worship Leader', 'Worship Leader'),
        ('Pembawa Firman', 'Pembawa Firman'),
        ('Singer', 'Singer'),
        ('Music', 'Music'),
        ('Multimedia', 'Multimedia'),
        ('Usher', 'Usher'),
        ('Tamborin', 'Tamborin'),
        ('Sekolah Minggu', 'Sekolah Minggu'),
    )

    nama = models.CharField(max_length=100)

    bidang_pelayanan = models.CharField(
        max_length=50,
        choices=BIDANG_PELAYANAN
    )

    def __str__(self):
        return self.nama

