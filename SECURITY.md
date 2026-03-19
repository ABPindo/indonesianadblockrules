# Security Policy

## Scope

ABPindo adalah proyek daftar filter iklan (filter list). Tidak ada server, API, atau kode yang dieksekusi di sisi pengguna secara langsung. Komponen yang relevan dari sisi keamanan:

- **Filter rules** di folder `src/` yang dapat mempengaruhi perilaku pemblokiran di browser atau DNS pengguna
- **False positive** yang memblokir situs atau layanan yang seharusnya dapat diakses
- **Filter berbahaya** yang secara tidak sengaja memblokir layanan keamanan, update OS, atau layanan kritis lainnya

## Melaporkan Masalah Keamanan

Jika Anda menemukan filter yang secara tidak sengaja memblokir layanan kritis (misalnya layanan kesehatan, keuangan, atau infrastruktur penting), atau menemukan pola filter yang berpotensi disalahgunakan:

1. **Jangan buat public issue** untuk masalah keamanan yang sensitif.
2. Hubungi maintainer melalui [GitHub Discussions](https://github.com/ABPindo/indonesianadblockrules/discussions) dengan label "Security".
3. Sertakan detail: filter yang bermasalah, dampak yang ditimbulkan, dan langkah reproduksi.

Untuk masalah umum seperti false positive biasa, silakan buat [GitHub Issue](https://github.com/ABPindo/indonesianadblockrules/issues) secara normal.

## False Positive (Blokir Salah Sasaran)

False positive bukan masalah keamanan, tetapi tetap kami prioritaskan. Laporkan melalui [GitHub Issues](https://github.com/ABPindo/indonesianadblockrules/issues) dengan format:

```
[False Positive] nama-situs.com - deskripsi singkat masalah
```

Sertakan URL halaman, tangkapan layar, dan ekstensi/software yang digunakan.
