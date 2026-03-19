# Panduan Berkontribusi ke ABPindo 🤝

Terima kasih sudah meluangkan waktu untuk membantu ABPindo! Panduan ini menjelaskan cara melaporkan masalah dan mengirim perbaikan agar prosesnya berjalan lancar untuk semua pihak.

---

## Sebelum Mulai

- **Cek issue yang sudah ada** — pastikan masalah yang sama belum pernah dilaporkan di [GitHub Issues](https://github.com/ABPindo/indonesianadblockrules/issues).
- **Reproduksi masalah** — pastikan masalah konsisten terjadi, bukan hanya sekali.
- **Nonaktifkan ekstensi lain** — untuk memastikan masalahnya benar-benar dari ABPindo, bukan filter lain.

---

## Cara Melaporkan Masalah

### 🔴 Iklan tidak terblokir

Jika menemukan iklan yang lolos dari pemblokiran, buat issue baru dengan informasi berikut:

- **URL halaman** yang bermasalah (bukan URL iklannya, tapi halaman tempat iklan muncul)
- **Tangkapan layar** yang menunjukkan iklan yang dimaksud
- **Ekstensi** yang digunakan (uBlock Origin, AdGuard, dll.) beserta versinya
- **Filter aktif** selain ABPindo (EasyList, EasyPrivacy, dll.)
- **Peramban** dan versinya

Contoh judul issue yang baik:
```
[Iklan] detik.com - banner iklan di sidebar tidak terblokir
[Popup] kompas.com - overlay newsletter muncul terus
```

### 🟡 Blokir salah sasaran (*false positive*)

Jika ABPindo memblokir konten yang seharusnya tidak diblokir (gambar hilang, fitur situs rusak, halaman tidak bisa dibuka), laporkan dengan:

- **URL halaman** yang terdampak
- **Tangkapan layar** sebelum dan sesudah menonaktifkan ABPindo
- **Elemen yang terdampak** (gambar, tombol, video, dll.)
- **Ekstensi dan peramban** yang digunakan

Contoh judul issue yang baik:
```
[False Positive] tokopedia.com - gambar produk tidak muncul
[False Positive] youtube.com - tombol subscribe tidak berfungsi
```

---

## Cara Mengirim Pull Request

### Lingkungan Pengujian yang Direkomendasikan

Sebelum mengirim PR, uji filter menggunakan konfigurasi berikut agar konsisten dengan standar pengujian ABPindo:

| Komponen | Rekomendasi |
|---|---|
| Peramban | [Firefox](https://www.mozilla.org/id/firefox/) |
| Ekstensi | [uBlock Origin](https://github.com/gorhill/uBlock#installation) |
| Filter aktif | EasyList, EasyPrivacy, ABPindo, uBlock filters |

### Struktur File Sumber

Filter ABPindo diorganisasi dalam folder `src/`. Tambahkan filter ke file yang paling sesuai dengan jenisnya:

```
src/
├── advert/
│   ├── adservers.txt       # Domain server iklan pihak ketiga
│   └── thirdparty.txt      # Elemen iklan dari sumber eksternal
├── adult/
│   └── adult_thirdparty.txt  # Konten dewasa & judi
└── ...
```

### Panduan Penulisan Filter

Gunakan sintaks [Adblock Plus](https://help.eyeo.com/en/adblockplus/how-to-write-filters) dan [uBlock Origin](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax). Beberapa prinsip dasar:

- **Sespesifik mungkin** — hindari filter yang terlalu luas yang bisa menyebabkan false positive
- **Satu filter, satu tujuan** — jangan gabungkan beberapa aturan berbeda dalam satu baris
- **Tambahkan komentar** jika filter tidak langsung jelas tujuannya:
  ```
  ! Blokir banner iklan floating di sisi kanan detik.com
  detik.com##.float-ads-right
  ```
- **Uji filter** sebelum dikirim — pastikan iklan terblokir dan tidak ada false positive di halaman yang sama

### Langkah-langkah PR

1. Fork repositori ini
2. Buat branch baru dari `master`:
   ```bash
   git checkout -b fix/nama-situs-masalah
   ```
3. Tambahkan atau ubah filter di file `src/` yang sesuai
4. Uji perubahan di peramban
5. Commit dengan pesan yang jelas:
   ```
   Add: blokir banner iklan di situs contoh.com
   Fix: false positive pada gambar produk tokopedia.com
   Remove: filter domain yang sudah tidak aktif
   ```
6. Buat Pull Request dan jelaskan perubahan yang dilakukan

---

## Referensi Penulisan Filter

- [How to Write Filters — Adblock Plus](https://help.eyeo.com/en/adblockplus/how-to-write-filters)
- [uBlock Static Filter Syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax)
- [DNS Filtering Rules Syntax — AdGuard](https://adguard-dns.io/kb/general/dns-filtering-syntax/)
- [python-abp](https://github.com/adblockplus/python-abp) — utilitas rendering filter
- [PyFunceble](https://github.com/funilrys/PyFunceble) — utilitas cek status domain

---

Bersama-sama kita bisa membuat pengalaman browsing yang lebih bersih untuk pengguna Indonesia dan Malaysia. Setiap kontribusi, sekecil apapun, sangat berarti! 🙌
