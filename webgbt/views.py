from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .models import JadwalIbadah, JadwalPelayanan, WartaGereja, Renungan, Komentar, Simpan, Suka, DataPelayanAltar, Baptis, PelayanAltar
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import textwrap

# Create your views here.
def home(request):
    context = {
        'renungan': Renungan.objects.all().order_by('-id')[:3],
        'wartagereja': WartaGereja.objects.all().order_by('-id')[:5],
        'jadwalibadah': JadwalIbadah.objects.all().order_by('-id')[:3],
        'jadwalpelayanan': JadwalPelayanan.objects.all().order_by('-id')[:3],
        'suka': Suka.objects.all(),
        'simpan': Simpan.objects.all(),
        'komentar': Komentar.objects.all(),
    }
    return render(request, 'dashboard.html', context)
 
 
 #lihat sejarah greja
@login_required(login_url='login')
def sejarah(request):
    return render(request, 'sejarah.html')
    
#views Renungan
@login_required(login_url='login')
def renungan(request, id):
    data = get_object_or_404(Renungan, id=id)
    content_type = ContentType.objects.get_for_model(Renungan)

    total_like = Suka.objects.filter(
        content_type=content_type,
        object_id=data.id
    ).count()

    user_sudah_like = False

    if request.user.is_authenticated:
        user_sudah_like = Suka.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=data.id
        ).exists()

    context = {
        'data': data,
        'total_like': total_like,
        'user_sudah_like': user_sudah_like,
        'komentar': Komentar.objects.filter(
            parent__isnull=True
        ).order_by('-dibuat_pada')
    }

    return render(request, 'renungan.html', context)

@login_required(login_url='login')
def renungan_list(request):
    data_renungan = Renungan.objects.all().order_by('-id')
    
    paginator = Paginator(data_renungan, 5)  # 5 konten per halaman

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'renungan_list.html', { 'page_obj': page_obj})

#Views JadwalIbadah
@login_required(login_url='login')
def jadwalibadah(request, id):
    data = get_object_or_404(JadwalIbadah, id=id)
    return render(request, 'jadwal_ibadah.html', {'data': data})

@login_required(login_url='login')
def jadwal_ibadahlist(request):
    data_jadwalibadah = JadwalIbadah.objects.all().order_by('-id')
    
    paginator = Paginator(data_jadwalibadah, 5)  # 5 konten per halaman

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'jadwal_ibadahlist.html', { 'page_obj': page_obj})

#Views JadwalPelayanan
@login_required(login_url='login')
def jadwalpelayanan(request, id):
    data = get_object_or_404(JadwalPelayanan, id=id)
    return render(request, 'jadwal_pelayanan.html', {'data': data})
 
@login_required(login_url='login') 
def jadwal_pelayananlist(request):
    data_jadwalpelayanan = JadwalPelayanan.objects.all().order_by('-id')
    
    paginator = Paginator(data_jadwalpelayanan, 5)  # 5 konten per halaman

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'jadwal_pelayananlist.html', { 'page_obj': page_obj})
    
#Views Warta Gereja
@login_required(login_url='login')
def wartagereja(request, id):
    data = get_object_or_404(WartaGereja, id=id)
    return render(request, 'warta_gereja.html', {'data': data})
    
@login_required(login_url='login')    
def warta_gerejalist(request):
    data_wartagereja = WartaGereja.objects.all().order_by('-id')
    
    paginator = Paginator(data_wartagereja, 5)  # 5 konten per halaman

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'warta_gerejalist.html', { 'page_obj': page_obj})
    
#LoginUsers
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            messages.success(
                request,
                'Selamat datang {user.username}, login berhasil!'
            )
            return redirect('dashboard')
        else:
            messages.error(
                request,
                'Username atau password salah!'
            )
    return render(request, 'login.html')
    
def dashboard(request):
    return render(request, 'dashboard.html')

#LogoutUsers
def logout_user(request):
    logout(request)
    messages.success(
        request,
        'Berhasil logout'
    )
    return redirect('login')

#Komentar
@login_required(login_url='login')
def komentar(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        isi = request.POST.get('isi')
        parent_id = request.POST.get('parent_id')

        parent = None

        if parent_id:
            parent = get_object_or_404(
                Komentar,
                id=parent_id
            )

        Komentar.objects.create(
            user=request.user,
            isi=isi,
            parent=parent
        )

    return redirect(
        request.META.get('HTTP_REFERER', '/')
    )
    
#Suka
@login_required(login_url='login')
def toggle_like(request, model_name, id):

    if not request.user.is_authenticated:
        return redirect('login')

    # Ambil model secara dinamis
    model = apps.get_model('webgbt', model_name)

    obj = get_object_or_404(model, id=id)

    content_type = ContentType.objects.get_for_model(model)

    like = Suka.objects.filter(
        user=request.user,
        content_type=content_type,
        object_id=obj.id
    ).first()

    # Toggle Like
    if like:
        like.delete()
    else:
        Suka.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=obj.id
        )

    return redirect(request.META.get('HTTP_REFERER'))

#baptis
@login_required(login_url='login')
def baptis(request):

    if request.method == 'POST':

        data = Baptis.objects.create(
            nama=request.POST['nama'],
            tempat_lahir=request.POST['tempat_lahir'],
            tanggal_lahir=request.POST['tanggal_lahir'],
            jenis_kelamin=request.POST['jenis_kelamin'],
            alamat=request.POST['alamat'],
            no_hp=request.POST['no_hp'],
            status=request.POST['status_baptis'],
        )

        return redirect(
            'jadwal_baptis',
        )

    # AMBIL DATA TERAKHIR
    data = Baptis.objects.order_by('-id').first()

    return render(
        request,
        'baptis.html',
        {
            'data': data
        }
    )

@login_required(login_url='login')
def download_baptis(request, id):

    data = get_object_or_404(Baptis, id=id)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        f'attachment; filename="form_baptis.pdf"'
    )

    p = canvas.Canvas(response)

# JUDUL
    p.setFont("Helvetica-Bold", 18)
    p.drawString(80, 800, "FORM PENDAFTARAN BAPTIS")
    p.setFont("Helvetica", 12)
    p.drawString(140, 780, "Gereja Bethel Elshaddai Solo")

# ISI
    p.setFont("Helvetica", 12)
    y = 740

    p.drawString(80, y, f"Nama : {data.nama}")
    y -= 30

    p.drawString(80, y, f"Tempat Lahir : {data.tempat_lahir}")
    y -= 30

    p.drawString(80, y, f"Tanggal Lahir : {data.tanggal_lahir}")
    y -= 30

    p.drawString(80, y, f"Jenis Kelamin : {data.jenis_kelamin}")
    y -= 30

    p.drawString(80, y, f"Alamat : {data.alamat}")
    y -= 30

    p.drawString(80, y, f"No HP : {data.no_hp}")
    y -= 30


# FOOTER AYAT
    footer = (
        "Matius 28:19-20 Karena itu pergilah, jadikanlah semua bangsa "
        "murid-Ku dan baptislah mereka dalam nama Bapa dan Anak dan Roh Kudus, "
        "dan ajarlah mereka melakukan segala sesuatu yang telah "
        "Kuperintahkan kepadamu. Dan ketahuilah, Aku menyertai kamu "
        "senantiasa sampai kepada akhir zaman."
    )

    text = p.beginText(40, 60)
    text.setFont("Helvetica-Oblique", 9)
    text.setLeading(12)

# otomatis pindah baris
    lines = textwrap.wrap(footer, width=95)

    for line in lines:
        text.textLine(line)

    p.drawText(text)

    p.save()

    return response
    
#Jadwal Baptis
def jadwal_baptis(request):
    data = Baptis.objects.all()

    return render(request, 'jadwal_baptis.html', {
        'data': data
    })
    
#daftar pelayan altar
@login_required(login_url='login')
def pelayan_altar(request):

    if request.method == 'POST':

        data = PelayanAltar.objects.create(
            nama=request.POST['nama'],
            tempat_lahir=request.POST['tempat_lahir'],
            tanggal_lahir=request.POST['tanggal_lahir'],
            jenis_kelamin=request.POST['jenis_kelamin'],
            alamat=request.POST['alamat'],
            no_hp=request.POST['no_hp'],
            bidang_pelayanan=request.POST['bidang_pelayanan'],
            pengalaman=request.POST.get('pengalaman'),
        )

        return redirect('download_pelayan', data.id)

    return render(request, 'joinpelayanan.html')

@login_required(login_url='login')
def download_pelayan(request, id):

    data = get_object_or_404(PelayanAltar, id=id)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        f'attachment; filename="form_pelayan_altar.pdf"'
    )

    p = canvas.Canvas(response)

    # JUDUL
    p.setFont("Helvetica-Bold", 18)
    p.drawString(150, 800, "FORM PENDAFTARAN PELAYAN ALTAR Gereja Bethel Tabernakel")

    # ISI
    p.setFont("Helvetica", 12)

    y = 740

    p.drawString(80, y, f"Nama : {data.nama}")
    y -= 30

    p.drawString(80, y, f"Tempat Lahir : {data.tempat_lahir}")
    y -= 30

    p.drawString(80, y, f"Tanggal Lahir : {data.tanggal_lahir}")
    y -= 30

    p.drawString(80, y, f"Jenis Kelamin : {data.jenis_kelamin}")
    y -= 30

    p.drawString(80, y, f"Alamat : {data.alamat}")
    y -= 30

    p.drawString(80, y, f"No HP : {data.no_hp}")
    y -= 30

    p.drawString(80, y, f"Bidang Pelayanan : {data.bidang_pelayanan}")
    y -= 30

    p.drawString(80, y, f"Pengalaman : {data.pengalaman}")
    y -= 30
    
    p.setFont("Helvetica-Bold", 18)
    p.drawString(150, 800, "FORM PENDAFTARAN PELAYAN ALTAR Gereja Bethel Tabernakel")

    p.save()

    return response
    
#Daftar akun 
def daftar(request):

    if request.method == 'POST':

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:

            messages.error(request, 'Password tidak sama!')
            return redirect('daftar')

        if User.objects.filter(username=username).exists():

            messages.error(request, 'Username sudah digunakan!')
            return redirect('daftar')

        User.objects.create_user(
            username=username,
            password=password1
        )

        messages.success(request, 'Akun berhasil dibuat!')
        return redirect('login')

    return render(request, 'daftar.html')

#Lupa Password
def lupa_password(request):

    if request.method == "POST":

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # cek username
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            messages.error(request, "Username tidak ditemukan")
            return redirect('lupa_password')

        # cek password sama
        if password1 != password2:
            messages.error(request, "Konfirmasi password tidak cocok")
            return redirect('lupa_password')

        # ganti password
        user.set_password(password1)
        user.save()

        messages.success(request, "Password berhasil diganti")
        return redirect('login')

    return render(request, 'lupa.html')

#Data Pelayan Altar
def data_pelayan(request):

    pelayanan = {}

    bidang_list = [
        'Worship Leader',
        'Pembawa Firman',
        'Singer',
        'Music',
        'Multimedia',
        'Usher',
        'Tamborin',
        'Sekolah Minggu'
    ]

    for bidang in bidang_list:

        pelayanan[bidang] = DataPelayanAltar.objects.filter(
            bidang_pelayanan=bidang
        )

    context = {
        'pelayanan': pelayanan
    }

    return render(request, 'data_pelayan.html', context)


