# Setup: Browser Extension & Browser

Panduan ini menjelaskan cara mengaktifkan ABPindo di berbagai browser dan ekstensi. Sebagian browser sudah mendukung ABPindo secara native tanpa perlu ekstensi tambahan.

---

## Brave Browser (Native — Tanpa Ekstensi)

Brave mendukung custom filter list secara native melalui mesin pemblokir bawaannya. ABPindo dapat ditambahkan langsung tanpa ekstensi tambahan.

**Desktop & Android:**

1. Buka `brave://adblock` di address bar.
2. Gulir ke bagian **Add custom filter lists**.
3. Klik **Add filter list via URL**.
4. Masukkan URL berikut, lalu klik **Add**:

```
https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt
```

5. Filter akan diperbarui otomatis setiap minggu.

> **Catatan:** Pastikan Trackers & ads blocking di `brave://settings/shields` tidak dalam kondisi **Disabled**. Setel ke **Standard** atau **Aggressive** agar filter aktif bekerja.

> **Ingin kontrol lebih penuh?** Pasang ekstensi [uBlock Origin](https://github.com/gorhill/uBlock#installation) dan ikuti panduan di bawah. uBlock Origin memberikan dukungan sintaks filter yang lebih lengkap termasuk scriptlet.

---

## uBlock Origin

1. Klik ikon **uBlock Origin** di toolbar browser.
2. Klik ikon ⚙ (*Open the dashboard*).
3. Buka tab **Filter Lists**.
4. Gulir ke bagian **Regions, languages**, lalu klik **+** untuk memperluas.
5. Cari **ID, MYS: ABPindo** dan centang kotaknya.

   ![Contoh tampilan filter list uBlock Origin](https://github.com/user-attachments/assets/96a58dd6-980f-49dd-834a-f6892641e44f)

6. Klik **Apply changes** di bagian atas untuk menyimpan.

> **uBlock Origin Lite:** Setel *default filtering mode* ke **Complete** agar semua elemen terblokir. Tanpa ini, sebagian filter mungkin tidak aktif.

---

## AdGuard (Desktop / Extension)

1. Buka **Settings** AdGuard.
2. Pilih tab **Filters**.
3. Masuk ke bagian **Language-specific**.
4. Temukan **ABPindo** dan aktifkan toggle-nya.
5. Klik **Apply** untuk memperbarui.

Atau tambahkan secara manual via **User Rules** dengan URL berikut:

```
https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt
```

---

## Adblock Plus (ABP)

1. Klik ikon **Adblock Plus** di browser.
2. Pilih **Options**.
3. Buka tab **Filter Lists**.
4. Di bagian *Language-specific filters*, cari **ABPindo**.
5. Centang dan klik **Apply**.

Jika tidak ditemukan, tambahkan manual via tombol **Add a filter list** dengan URL:

```
https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt
```

---

## Troubleshooting

**ABPindo tidak muncul di daftar filter:**
- Pastikan bahasa browser sudah diatur ke **Indonesia** atau **Malaysia** (`Settings > Language`).
- Klik **Update now** di dashboard untuk memperbarui daftar filter.

**Masih ada iklan yang lolos:**
- Pastikan filter lain seperti EasyList dan EasyPrivacy juga aktif — ABPindo dirancang sebagai pelengkap, bukan pengganti.
- Laporkan melalui [GitHub Issues](https://github.com/ABPindo/indonesianadblockrules/issues) dengan menyertakan URL halaman dan tangkapan layar.

**Fitur situs rusak / gambar hilang:**
- Ini kemungkinan *false positive*. Nonaktifkan ABPindo sementara untuk konfirmasi, lalu laporkan di [GitHub Issues](https://github.com/ABPindo/indonesianadblockrules/issues).
