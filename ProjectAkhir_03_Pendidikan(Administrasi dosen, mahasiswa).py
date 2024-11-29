import random
data_mahasiswa = []
data_dosen = {}
data_matakuliah = {}

def login():
    while True:
        email = input("Masukkan Email: ")
        password = input("Masukkan Password: ")
        for mahasiswa in data_mahasiswa:
            if mahasiswa["email"] == email and mahasiswa["password"] == password:
                print(f"Selamat datang, {mahasiswa['nama']}.")
                menu_utama(mahasiswa)
                return
        print("Email atau password salah.")
        if input("Apakah ingin daftar dahulu? (ya/tidak) ") == "ya":
            daftar_mahasiswa()
def daftar_mahasiswa():
    while True:
        print("=== Menu Daftar ===")
        nim = input("Masukkan NIM: ")
        if not nim:
            print("NIM tidak boleh kosong.") 
            continue
        nama = input("Masukkan Nama: ")
        if not nama:
            print("Nama tidak boleh kosong.")
            continue
        email = input("Masukkan Email: ")
        if not email:
            print("Email tidak boleh kosong.")
            continue
        password = input("Masukkan Password: ")
        if not password:
            print("Password tidak boleh kosong.")
            continue
        mahasiswa = {
            "nim": nim,
            "nama": nama,
            "email": email,
            "password": password,
            "dosen_wali": None,
            "krs": set()
            }
        data_mahasiswa.append(mahasiswa)
        print(f"Akun berhasil terdaftar...")
        menu_utama(mahasiswa)
        break
def menu_utama(mahasiswa):
    while True:
        print("\n=== Menu Mahasiswa ===")
        print("1. Perwalian Mahasiswa")
        print("2. Lihat Data Saya")
        print("3. Keluar")
        pilihan = input("Pilih opsi (1-3): ")
        if pilihan == "1":
            perwalian(mahasiswa)
        elif pilihan == "2":
            lihat_data_pribadi(mahasiswa)
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid.")
def perwalian(mahasiswa):
    if not mahasiswa["dosen_wali"]:
        print("=== Perwalian ===")
        if data_dosen:
            dosen_terpilih = random.choice(list(data_dosen.keys()))
            mahasiswa["dosen_wali"] = dosen_terpilih
            print(f"Dosen wali Anda telah dipilih secara acak: {data_dosen[dosen_terpilih]['nama']}")
        else:
            print("Tidak ada dosen yang tersedia saat ini.")
            return
    while True:
        print("=== Daftar Mata Kuliah ===")
        if not data_matakuliah:
            print("Belum ada mata kuliah yang terdaftar. Mohon tambahkan mata kuliah terlebih dahulu.")
            break
        else:
            for kode, matkul in data_matakuliah.items():
                print(f"Kode matkul: {kode}, {matkul['nama']}, {matkul['sks']} SKS, Ruangan: {matkul['ruang']}, Max Kursi: {matkul['max_kursi']}, Jadwal: {matkul['jadwal']}")
            kode_matkul = input("Masukkan Kode Mata Kuliah untuk KRS (klik enter untuk kembali): ")
            if kode_matkul == "":
                break
            if kode_matkul in data_matakuliah:
                if not cek_konflik_jadwal(mahasiswa, kode_matkul):
                    mahasiswa["krs"].add(kode_matkul)
                    data_matakuliah[kode_matkul]["peserta"] += 1
                    print(f"{data_matakuliah[kode_matkul]['nama']} berhasil ditambahkan ke KRS.") 
                else:
                    print("Mata kuliah tidak ditambahkan karena konflik jadwal.") 
            else:
                print("Kode mata kuliah tidak valid.") 
def cek_konflik_jadwal(mahasiswa, kode_matakuliah):
    matkul_baru = data_matakuliah[kode_matakuliah]
    if "peserta" not in matkul_baru:
        matkul_baru["peserta"] = 0
    if matkul_baru["peserta"] >= matkul_baru["max_kursi"]:
        print(f"Maaf, mata kuliah {matkul_baru['nama']} sudah penuh. Maks kursi: {matkul_baru['max_kursi']}.")
        return True
    for kode in mahasiswa["krs"]:
        matkul_lama = data_matakuliah[kode]
        if matkul_baru["jadwal"] == matkul_lama["jadwal"]:
            print(f"Konflik jadwal dengan {matkul_lama['nama']} ({matkul_lama['jadwal']}).")
            return True
    return False
def lihat_data_pribadi(mahasiswa):
    print("=== Data Pribadi Mahasiswa ===")
    print(f"NIM         : {mahasiswa['nim']}")
    print(f"Nama        : {mahasiswa['nama']}")
    print(f"Email       : {mahasiswa['email']}")
    dosen_wali = mahasiswa["dosen_wali"]
    if dosen_wali:
        print(f"Dosen Wali  : {data_dosen[dosen_wali]['nama']}")
    else:
        print("Dosen Wali  : Belum dipilih")
    print("\nMata Kuliah yang telah diambil:")
    if mahasiswa["krs"]:
        for kode in mahasiswa["krs"]:
            matkul = data_matakuliah[kode]
            print(f"- {matkul['nama']} ({matkul['sks']} SKS), Jadwal: {matkul['jadwal']}")
    else:
        print("Belum ada mata kuliah yang diambil.")
    input("\nTekan enter untuk kembali...")
def menu_mahasiswa():
    while True:
        print("=== Sistem Mahasiswa ===")
        print("1. Login")
        print("2. Daftar")
        print("nb: Tekan enter jika ingin kembali")
        pilihan = input("Pilih cara masuk Anda? (1/2): ")
        if pilihan == "1":
            login()
        elif pilihan == "2":
            daftar_mahasiswa()
        else:
            print("Terima kasih telah menggunakan sistem ini!")
            break
def tambah_dosen():
    while True:
        print("=== Tambah Dosen ===")
        kode_dosen = input("Masukkan Kode Dosen: ")
        if not kode_dosen:
            print("Kode dosen tidak boleh kosong. Ulangi.")
            continue
        nama_dosen = input("Masukkan Nama Dosen: ")
        if not nama_dosen:
            print("Nama dosen tidak boleh kosong. Ulangi.")
            continue
        data_dosen[kode_dosen] = {"nama": nama_dosen}
        print(f"Dosen {nama_dosen} berhasil ditambahkan.")
        if input("Tambah dosen lagi? (ya/tidak): ") != "ya":
            break
def tambah_matkul():
    while True:
        print("=== Tambah Mata Kuliah ===")
        if not data_dosen:
            print("Belum ada dosen terdaftar. Harap tambahkan dosen terlebih dahulu.")
            break
        else:
            dosen_terpilih = random.choice(list(data_dosen.values()))["nama"]   
        kode_matkul = input("Masukkan Kode Mata Kuliah: ")
        if not kode_matkul:
            print("Kode mata kuliah tidak boleh kosong.")
            continue
        nama_matkul = input("Masukkan Nama Mata Kuliah: ")
        if not nama_matkul:
            print("Nama mata kuliah tidak boleh kosong.")
            continue
        sks = (input("Masukkan Jumlah SKS: "))
        if not sks:
            print("Jumlah SKS tidak boleh kosong.")
            continue
        if not sks.isdigit() or int(sks) <= 0:
            print("Jumlah SKS harus berupa angka dan harus lebih dari 0.")
            continue
        sks = int(sks)
        ruang = input("Masukkan Ruangan: ")
        if not ruang:
            print("Ruangan tidak boleh kosong.")
            continue
        max_kursi = (input("Masukkan Maksimal Kursi: "))
        if not max_kursi:
            print("Maksimal kursi tidak boleh kosong.")
            continue
        if not max_kursi.isdigit() or int(max_kursi) <= 0:
            print("Maksimal kursi harus berupa angka dan harus lebih dari 0.")
            continue
        max_kursi = int(max_kursi)
        jadwal = input(f"Masukkan Jadwal {nama_matkul} (contoh: Senin 08:00-10:00): ")
        if not jadwal:
            print("Jadwal tidak boleh kosong.")
            continue
        data_matakuliah[kode_matkul] = {"nama": nama_matkul,"sks": sks,
            "ruang": ruang,"max_kursi": max_kursi,
            "jadwal": jadwal,"dosen" : dosen_terpilih,"peserta" : 0}
        print(f"Mata kuliah {nama_matkul} berhasil ditambahkan dengan dosen {dosen_terpilih}.")
        break
def tampilkan_dosen():
    while True:
        print("=== Daftar Dosen ===")
        if not data_dosen:
            print("Belum ada dosen yang terdaftar.")
            break
        else:
            for kode, dosen in data_dosen.items():
                print(f"Kode dosen: {kode}, nama: {dosen['nama']}")
            tanya = input("\ntekan enter jika ingin keluar ")
            if tanya == "":
                break
def tampilkan_matkul():
    while True:
        print("=== Daftar Mata Kuliah ===")
        if not data_matakuliah:
            print("Belum ada mata kuliah yang terdaftar.")
            break
        else:
            for kode, matkul in data_matakuliah.items():
                peserta = matkul["peserta"]
                sisa_kursi = matkul["max_kursi"] - peserta
                print(f"Kode matkul: {kode}, {matkul['nama']}, {matkul['sks']} SKS, Ruangan: {matkul['ruang']}, "
                    f"Max Kursi: {matkul['max_kursi']}, Sisa Kursi: {sisa_kursi}, Jadwal: {matkul['jadwal']}")
            tanya = input("\nTekan enter jika ingin keluar ")
            if tanya == '':
                break
def edit_matkul():
    while True:
        print("=== Daftar Mata Kuliah ===")
        if not data_matakuliah:
            print("Belum ada Mata kuliah yang ditambahkan.")
            break
        else:
            for kode, matkul in data_matakuliah.items():
                print(f"Kode matkul: {kode}, {matkul['nama']}, {matkul['sks']} SKS, Ruangan: {matkul['ruang']}, Max Kursi: {matkul['max_kursi']}, Jadwal: {matkul['jadwal']}")
            kode_matkul = input("\nMasukkan Kode mata kuliah yang ingin diedit: ")
            if kode_matkul in data_matakuliah.keys():
                while True:
                    print("Pilih atribut yang ingin diedit:")
                    print("1. Nama Matkul")
                    print("2. Jumlah SKS")
                    print("3. Ruangan")
                    print("4. Maksimal Kursi")
                    print("5. Jadwal")
                    pilihan = input("Pilih atribut yang ingin diedit (1-5): ")
                    if pilihan == "1":
                        nama_matkul_baru = input("Masukkan Nama matkul Baru: ")
                        data_matakuliah[kode_matkul]["nama"] = nama_matkul_baru
                        print(f"berhasil diubah menjadi {nama_matkul_baru}.")
                        return
                    elif pilihan == "2":
                        sks_baru = input("Masukkan Jumlah SKS Baru: ")
                        if sks_baru.isdigit() and int(sks_baru) > 0:
                            data_matakuliah[kode_matkul]["sks"] = int(sks_baru)
                            print(f"Jumlah SKS berhasil diubah menjadi {sks_baru}.")
                            return
                        else:
                            print("Jumlah SKS harus berupa angka positif.")
                    elif pilihan == "3":
                        ruang_baru = input("Masukkan Ruangan Baru: ")
                        data_matakuliah[kode_matkul]["ruang"] = ruang_baru
                        print(f"Ruangan berhasil diubah menjadi {ruang_baru}.")
                        return
                    elif pilihan == "4":
                        max_kursi_baru = input("Masukkan Maksimal Kursi Baru: ")
                        if max_kursi_baru.isdigit() and int(max_kursi_baru) > 0:
                            data_matakuliah[kode_matkul]["max_kursi"] = int(max_kursi_baru)
                            print(f"Maksimal kursi berhasil diubah menjadi {max_kursi_baru}.")
                            return
                        else:
                            print("Maksimal kursi harus berupa angka positif.")
                    elif pilihan == "5":
                        jadwal_baru = input("Masukkan Jadwal Baru: ")
                        data_matakuliah[kode_matkul]["jadwal"] = jadwal_baru
                        print(f"Jadwal berhasil diubah menjadi {jadwal_baru}.")
                        return
                    else:
                        print("Pilihan tidak valid. Mohon masukkan pilihan yang benar")
            else:
                print("Kode mata kuliah tidak ditemukan. Mohon masukkan kode yang valid.")
def hapus_matkul():
    while True:
        print("=== Daftar Mata Kuliah ===")
        if not data_matakuliah:
            print("Belum ada Mata kuliah yang ditambahkan.")
            break
        else:
            for kode, matkul in data_matakuliah.items():
                print(f"Kode matkul: {kode}, {matkul['nama']}, {matkul['sks']} SKS, Ruangan: {matkul['ruang']}, Max Kursi: {matkul['max_kursi']}, Jadwal: {matkul['jadwal']}")
            kode_matkul = input("Masukkan Kode matkul yang ingin dihapus: ")
            if kode_matkul in data_matakuliah:
                del data_matakuliah[kode_matkul]
                print(f"Matkul dengan kode {kode_matkul} berhasil dihapus.")
                break
            else:
                print("Kode matkul tidak ditemukan. Mohon masukkan kode yang valid.")
def menu_dosen_matkul():
    while True:
        print("\n=== Menu Dosen dan Mata Kuliah ===")
        print("1. Tambah Dosen")
        print("2. Tambah Mata Kuliah")
        print("3. Tampilkan Dosen")
        print("4. Tampilkan Mata Kuliah")
        print("5. Edit Mata Kuliah")
        print("6. Hapus Mata Kuliah")
        print("7. Keluar")
        pilihan = input("Pilih opsi (1-7): ")
        if pilihan == "1":
            tambah_dosen()
        elif pilihan == "2":
            tambah_matkul()
        elif pilihan == "3":
            tampilkan_dosen()
        elif pilihan == "4":
            tampilkan_matkul()
        elif pilihan == "5":
            edit_matkul()
        elif pilihan == "6":
            hapus_matkul()
        elif pilihan == "7":
            break
        else:
            print("Pilihan tidak valid.")

print("Selamat datang di Sistem Manajemen Mahasiswa, Dosen, dan Mata Kuliah!")
while True:
    print("\n=== Menu Utama ===")
    print("1. Sistem Dosen")
    print("2. Sistem Mahasiswa")
    print("3. Keluar")
    pilihan = input("Pilih opsi (1-3): ")
    if pilihan == "1":
        menu_dosen_matkul()
    elif pilihan == "2":
        menu_mahasiswa()
    elif pilihan == "3":
        print("Terima kasih telah menggunakan sistem ini!")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
