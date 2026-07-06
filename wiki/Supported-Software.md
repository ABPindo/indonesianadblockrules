# Perangkat Lunak yang Didukung

Daftar lengkap ekstensi peramban, peramban, dan perangkat lunak DNS yang kompatibel dengan ABPindo.

---

## Ekstensi Peramban

Ekstensi yang menggunakan sintaks **Adblock Plus**:

| Ekstensi | Platform | Tautan |
|---|---|---|
| [uBlock Origin](https://github.com/gorhill/uBlock) | Firefox, Edge, Opera | [Pasang](https://github.com/gorhill/uBlock#installation) |
| [uBlock Origin Lite](https://chromewebstore.google.com/detail/ublock-origin-lite/ddkjiahejlhfcafbddmgiahcphecmpfh) | Chrome/Chromium-based, Firefox, Edge, Safari | [Pasang](https://chromewebstore.google.com/detail/ublock-origin-lite/ddkjiahejlhfcafbddmgiahcphecmpfh) |
| [AdGuard Browser Extension](https://adguard.com/en/adguard-browser-extension/overview.html) | Chrome/Chromium-based, Firefox, Edge, Opera, Safari | [Pasang](https://adguard.com/en/adguard-browser-extension/overview.html) |
| [Ghostery](https://www.ghostery.com/) | Chrome/Chromium-based, Firefox, Edge, Opera, Safari | [Pasang](https://www.ghostery.com/) |
| [Adblock Plus](https://adblockplus.org) | Chrome/Chromium-based, Firefox, Edge, Opera, Safari | [Pasang](https://adblockplus.org) |
| [AdBlock](https://getadblock.com) | Chrome/Chromium-based, Firefox, Edge, Safari | [Pasang](https://getadblock.com) |
| [AdBlocker Ultimate](https://adblockultimate.net/id/browsers) | Chrome/Chromium-based, Firefox, Edge | [Pasang](https://adblockultimate.net/id/browsers) |

#### Rekomendasi
- Untuk Chrome/Chromium, AdGuard memberikan filter paling up-to-date, dukungan sintaks yang lebih luas, dan custom filter. lihat instruksinya [disini](https://github.com/https://github.com/ABPindo/indonesianadblockrules/blob/master/wiki/chrome-adguard-setup.md)
- Untuk Firefox/Firefox-based, uBlock Origin memberikan performa terbaik dan dukungan sintaks filter paling lengkap

---

## Peramban dengan Pemblokir Iklan Bawaan

| Peramban | Dukungan ABPindo | Cara | Tautan |
|---|---|---|---|
| [Brave](https://brave.com) | ✅ Native | Tambah via `brave://adblock` — lihat bagian "Content filtering", klik "See Full Lists", dan centang ABPindo.| [Unduh](https://brave.com) |
| [Adblock Browser](https://adblockbrowser.org/) | ✅ Bawaan | ABPindo aktif otomatis saat bahasa Indonesia/Malaysia | [Unduh](https://adblockbrowser.org/) |
| [Opera](https://www.opera.com) | ⚠️ Terbatas | Hanya format EasyList basic; scriptlet ABPindo tidak didukung — gunakan ekstensi uBlock Origin | [Unduh](https://www.opera.com) |
| [Vivaldi](https://vivaldi.com) | ⚠️ Terbatas | Sama seperti Opera — gunakan ekstensi uBlock Origin untuk hasil terbaik | [Unduh](https://vivaldi.com) |

---

## Server DNS

Perangkat lunak server DNS yang mendukung format filter ABPindo:

| Perangkat Lunak | Format | Tautan |
|---|---|---|
| [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) | Adblocker-syntax (`\|\|example.com^`) | [GitHub](https://github.com/AdguardTeam/AdGuardHome) |
| [Pi-Hole](https://pi-hole.net) | Domain / Adblocker-syntax | [Situs](https://pi-hole.net) |
| [Dnsmasq](https://thekelleys.org.uk/dnsmasq/doc.html) | `address=/example.com/0.0.0.0` | [Dokumentasi](https://thekelleys.org.uk/dnsmasq/doc.html) |
| [BIND](https://www.isc.org/bind/) (RPZ) | Response Policy Zone | [Situs](https://www.isc.org/bind/) |
| [Unbound](https://github.com/NLnetLabs/unbound) | `local-zone` | [GitHub](https://github.com/NLnetLabs/unbound) |
| [DNSCrypt-proxy](https://dnscrypt.info) | Domain | [Situs](https://dnscrypt.info) |

---

## Aplikasi Seluler & Pemblokir Tingkat Jaringan

Perangkat lunak berbasis hosts file, DNS, atau VPN lokal untuk Android:

| Perangkat Lunak | Platform | Format | Keterangan | Tautan |
|---|---|---|---|---|
| [AdGuard](https://adguard.com) | Android, iOS | Adblocker-syntax | Pilihan terlengkap — blokir di level jaringan tanpa root | [Situs](https://adguard.com) |
| [AdAway](https://adaway.org) | Android (root) | Hosts | Klasik dan ringan, butuh akses root | [Situs](https://adaway.org) |
| [Blokada](https://blokada.org) | Android | Domain | Tanpa root, bekerja via VPN lokal | [Situs](https://blokada.org) |
| [DNS66](https://f-droid.org/packages/org.jak_linux.dns66/) | Android | Domain | Sumber terbuka, tersedia di F-Droid | [F-Droid](https://f-droid.org/packages/org.jak_linux.dns66/) |
| [personalDNSfilter](https://zenz-solutions.de/personaldnsfilter/) | Android | Domain | Ringan, berbasis VPN lokal, tersedia di F-Droid | [Situs](https://zenz-solutions.de/personaldnsfilter/) |

---

## URL Langganan

Lihat tabel lengkap URL filter untuk setiap format di halaman [Setup: DNS Blocker](Setup-DNS-Blocker).
