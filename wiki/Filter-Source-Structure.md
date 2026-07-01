# Struktur File Sumber Filter

Halaman ini menjelaskan struktur folder `src/` di repositori ABPindo dan fungsi setiap file filter. Berguna bagi kontributor yang ingin menambahkan atau mengubah filter.

---

## Gambaran Umum Repositori

```
indonesianadblockrules/
├── src/                    # File sumber filter (diedit manual)
│   ├── advert/             # Filter iklan utama
│   └── adult/              # Filter konten dewasa & judi
├── subscriptions/          # File filter hasil build (jangan diedit langsung)
├── tools/                  # Script build dan utilitas
├── .github/                # Issue templates dan GitHub Actions
├── build.sh                # Script untuk generate subscriptions/ dari src/
└── *.template              # Template untuk setiap variasi filter output
```

> **Penting:** File di folder `subscriptions/` di-generate otomatis dari `src/` menggunakan `build.sh`. Jangan edit file di `subscriptions/` secara langsung — perubahan akan hilang saat build berikutnya.

---

## Struktur `src/advert/`

Filter iklan utama, digunakan di semua variasi ABPindo.

| File | Fungsi | Contoh |
|---|---|---|
| `adservers.txt` | Domain server iklan pihak ketiga yang murni khusus iklan | `domainiklan.id^$thirdparty` |
| `thirdparty.txt` | Domain penyedia iklan yang bukan murni ad server (bisa juga domain CDN ganda) | `domaingambar.id^$thirdparty` |
| `general_block.txt` | Filter blokir berdasarkan pola URL umum — **gunakan dengan hati-hati** untuk menghindari false positive | `.id/iklan/` |
| `general_hide.txt` | Element hiding berdasarkan pola class/ID umum — **gunakan dengan hati-hati** | `##.iklan` |
| `specific_block.txt` | Blokir spesifik per domain termasuk ekstensi file yang tepat | `domainiklan.id/banner.jpg` |
| `specific_hide.txt` | Element hiding spesifik per domain dengan class yang tepat | `situs.com##.banner-iklan` |
| `scriptlet_ublock.txt` | Filter sintaks khusus uBlock Origin (scriptlet, extended syntax) | `situs.com##+js(set-constant, adblock, false)` |
| `allowlist.txt` | Memperbaiki false positive agar fitur/elemen situs tetap berfungsi normal | `@@ikonlegitim.jpg` |

---

## Struktur `src/adult/`

Filter konten dewasa, judi, dan sejenisnya. Hanya masuk ke variasi `abpindo.txt` dan `hosts_adult.txt`, tidak ke `abpindo_noadult.txt`.

| File | Fungsi |
|---|---|
| `adult_general_block.txt` | Filter blokir umum untuk konten dewasa/judi |
| `adult_general_hide.txt` | Element hiding umum untuk konten dewasa/judi |
| `adult_thirdparty.txt` | Domain penyedia layanan judi/dewasa pihak ketiga |
| `adult_specific_block.txt` | Blokir URL spesifik untuk konten dewasa/judi di situs tertentu |
| `adult_specific_hide.txt` | Element hiding spesifik untuk konten dewasa/judi di situs tertentu |
| `adult_allowlist.txt` | Memperbaiki false positive pada filter konten dewasa |
| `adult_prank.txt` | Filter konten mengejutkan atau tidak pantas di luar kategori dewasa |

---

## Template Files

File `*.template` di root repositori mendefinisikan **komposisi** setiap variasi filter output:

### Variasi Browser Extension (Sintaks Adblock Plus)

| Template | Output | Isi |
|---|---|---|
| `abpindo.template` | `subscriptions/abpindo.txt` | Semua filter termasuk adult |
| `abpindo_noadult.template` | `subscriptions/abpindo_noadult.txt` | Filter tanpa adult |
| `abpindo_noelemhide.template` | `subscriptions/abpindo_noelemhide.txt` | Filter tanpa element hiding |
| `abpindo_annoyances.template` | `subscriptions/abpindo_annoyances.txt` | Filter khusus annoyances |
| `abpindo_extended.template` | `subscriptions/abpindo_extended.txt` | Filter eksperimental / residu |

### Variasi DNS (Hosts, Domain, Dnsmasq, dll.)

| Template | Output | Isi |
|---|---|---|
| `abpindo_hosts.template` | `subscriptions/abpindo_hosts.txt` | Filter domain adservers + thirdparty (intermediate, untuk dikonversi ke DNS) |
| `abpindo_hosts_adult.template` | `subscriptions/abpindo_hosts_adult.txt` | Sama + adult thirdparty |

Variasi DNS lainnya (hosts, domain, aghome, dnsmasq, rpz, unbound) di-generate dari file `subscriptions/abpindo_hosts.txt` menggunakan `tools/dns_converter.py`, bukan dari template. Lihat tahapan build di `tools/build.sh`.

---

## Panduan: Di Mana Menaruh Filter Baru?

Ikuti alur berikut untuk menentukan file yang tepat:

```
Filter baru
│
├── Apakah domain MURNI digunakan untuk iklan?
│   ├── Ya  → src/advert/adservers.txt
│   └── Tidak (domain umum yang juga menampilkan iklan)
│           → src/advert/thirdparty.txt
│
├── Apakah filter berdasarkan POLA URL (bukan domain penuh)?
│   ├── Blokir  → src/advert/general_block.txt (hati-hati)
│   └── Hide    → src/advert/general_hide.txt  (hati-hati)
│
├── Apakah filter SPESIFIK untuk satu situs?
│   ├── Blokir URL  → src/advert/specific_block.txt
│   ├── Hide elemen → src/advert/specific_hide.txt
│   └── uBlock-only → src/advert/scriptlet_ublock.txt
│
├── Apakah memperbaiki false positive?
│   └── → src/advert/allowlist.txt
│
└── Apakah konten dewasa / judi?
    └── → src/adult/ (file yang sesuai)
```
