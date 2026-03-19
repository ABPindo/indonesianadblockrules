# Supported Software

Daftar lengkap ekstensi browser, browser, dan software DNS yang kompatibel dengan ABPindo.

---

## Browser Extension

Ekstensi yang menggunakan sintaks **Adblock Plus**:

| Ekstensi | Platform | Link |
|---|---|---|
| [uBlock Origin](https://github.com/gorhill/uBlock) | Firefox, Chrome, Edge | [Install](https://github.com/gorhill/uBlock#installation) |
| [uBlock Origin Lite](https://chromewebstore.google.com/detail/ublock-origin-lite/ddkjiahejlhfcafbddmgiahcphecmpfh) | Chrome, Chromium-based | [Install](https://chromewebstore.google.com/detail/ublock-origin-lite/ddkjiahejlhfcafbddmgiahcphecmpfh) |
| [AdGuard Browser Extension](https://adguard.com/en/adguard-browser-extension/overview.html) | Firefox, Chrome, Edge, Safari | [Install](https://adguard.com/en/adguard-browser-extension/overview.html) |
| [Adblock Plus](https://adblockplus.org) | Firefox, Chrome, Edge, Safari | [Install](https://adblockplus.org) |
| [AdBlock](https://getadblock.com) | Firefox, Chrome, Edge | [Install](https://getadblock.com) |

> **Rekomendasi:** uBlock Origin memberikan performa terbaik dan dukungan sintaks filter paling lengkap.

---

## Browser dengan Built-in Ad Blocker

| Browser | Dukungan ABPindo | Cara | Link |
|---|---|---|---|
| [Brave](https://brave.com) | ✅ Native | Tambah via `brave://adblock` — lihat [panduan lengkap](Setup-Browser-Extension#brave-browser-native--tanpa-ekstensi) | [Download](https://brave.com) |
| [Adblock Browser](https://adblockbrowser.org/) | ✅ Bawaan | ABPindo aktif otomatis saat bahasa Indonesia/Malaysia | [Download](https://adblockbrowser.org/) |
| [Opera](https://www.opera.com) | ⚠️ Terbatas | Hanya format EasyList basic; scriptlet ABPindo tidak didukung — gunakan ekstensi uBlock Origin | [Download](https://www.opera.com) |
| [Vivaldi](https://vivaldi.com) | ⚠️ Terbatas | Sama seperti Opera — gunakan ekstensi uBlock Origin untuk hasil terbaik | [Download](https://vivaldi.com) |

---

## DNS Server

Software server DNS yang mendukung format filter ABPindo:

| Software | Format | Link |
|---|---|---|
| [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) | Adblocker-syntax (`\|\|example.com^`) | [GitHub](https://github.com/AdguardTeam/AdGuardHome) |
| [Pi-Hole](https://pi-hole.net) | Domain / Adblocker-syntax | [Website](https://pi-hole.net) |
| [Dnsmasq](https://thekelleys.org.uk/dnsmasq/doc.html) | `address=/example.com/0.0.0.0` | [Docs](https://thekelleys.org.uk/dnsmasq/doc.html) |
| [BIND](https://www.isc.org/bind/) (RPZ) | Response Policy Zone | [Website](https://www.isc.org/bind/) |
| [Unbound](https://github.com/NLnetLabs/unbound) | `local-zone` | [GitHub](https://github.com/NLnetLabs/unbound) |
| [DNSCrypt-proxy](https://dnscrypt.info) | Domain | [Website](https://dnscrypt.info) |

---

## Aplikasi Mobile & Network-level Blocker

Software berbasis hosts file, DNS, atau VPN lokal untuk Android:

| Software | Platform | Format | Keterangan | Link |
|---|---|---|---|---|
| [AdGuard](https://adguard.com) | Android, iOS | Adblocker-syntax | Pilihan terlengkap — blokir di level jaringan tanpa root | [Website](https://adguard.com) |
| [AdAway](https://adaway.org) | Android (root) | Hosts | Klasik dan ringan, butuh akses root | [Website](https://adaway.org) |
| [Blokada](https://blokada.org) | Android | Domain | Tanpa root, bekerja via VPN lokal | [Website](https://blokada.org) |
| [DNS66](https://f-droid.org/packages/org.jak_linux.dns66/) | Android | Domain | Open source, tersedia di F-Droid | [F-Droid](https://f-droid.org/packages/org.jak_linux.dns66/) |

---

## Format URL Langganan

Lihat tabel lengkap URL filter untuk setiap format di halaman [Setup: DNS Blocker](Setup-DNS-Blocker).
