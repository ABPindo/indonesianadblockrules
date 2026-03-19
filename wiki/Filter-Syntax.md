# Filter Syntax

ABPindo mendukung beberapa format sintaks filter tergantung pada software yang digunakan. Halaman ini menjelaskan masing-masing format dan kapan menggunakannya.

---

## Sintaks Adblock Plus (Browser Extension)

Digunakan untuk ekstensi browser seperti uBlock Origin, AdGuard, dan Adblock Plus. Ini adalah format utama ABPindo.

Referensi resmi:
- [How to Write Filters — Adblock Plus](https://help.eyeo.com/en/adblockplus/how-to-write-filters)
- [uBlock Static Filter Syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax)

### Contoh dasar

```adblock
! Komentar — baris yang diawali tanda seru diabaikan

! Blokir domain iklan pihak ketiga
domainiklam.id^$thirdparty

! Blokir URL spesifik
domainiklan.id/banner/iklan.jpg

! Sembunyikan elemen HTML (element hiding)
##.sidebar-ads
situs.com##div[class*="iklan"]

! Filter khusus uBlock Origin (scriptlet)
situs.com##+js(set-constant, adblock, false)

! Allowlist — putihkan elemen yang terblokir keliru
@@ikonbagus.jpg
@@situs.com^$document
```

### Modifier penting

| Modifier | Fungsi | Contoh |
|---|---|---|
| `$thirdparty` | Hanya blokir saat dimuat dari domain lain | `iklan.com^$thirdparty` |
| `$domain=` | Terapkan hanya di domain tertentu | `iklan.com^$domain=situs.com` |
| `$script` | Hanya cocokkan file JavaScript | `tracker.js$script` |
| `$image` | Hanya cocokkan gambar | `banner.png$image` |
| `@@` | Allowlist / whitelist | `@@elemen.jpg` |
| `##` | Element hiding | `##.ads-container` |
| `#@#` | Element hiding exception | `situs.com#@#.legit-element` |

---

## Sintaks Hosts File

Digunakan untuk AdAway, HostsMan, dan file hosts sistem operasi. Memblokir seluruh domain.

```
0.0.0.0 iklan.contoh.com
0.0.0.0 tracker.contoh.com
```

---

## Sintaks Domain (Plain List)

Digunakan untuk Pi-Hole, DNSCrypt, DNS66, Blokada. Format paling sederhana.

```
iklan.contoh.com
tracker.contoh.com
```

---

## Sintaks Adblocker-syntax Domains

Digunakan untuk AdGuard Home dan Pi-Hole (mode adblocker). Format `||domain^`.

```
||iklan.contoh.com^
||tracker.contoh.com^
```

---

## Sintaks Dnsmasq

Dua format tersedia:

```
# Format address (redirect ke 0.0.0.0)
address=/iklan.contoh.com/0.0.0.0

# Format server (kembalikan NXDOMAIN)
server=/iklan.contoh.com/
```

---

## Sintaks RPZ (BIND)

Digunakan untuk BIND DNS server dengan Response Policy Zone:

```
iklan.contoh.com CNAME .
```

---

## Sintaks Unbound

```
local-zone: "iklan.contoh.com" always_nxdomain
```

---

## Rekomendasi Format per Use Case

| Skenario | Format yang Digunakan |
|---|---|
| Pengguna desktop/laptop biasa | Adblock Plus (via ekstensi browser) |
| Pemblokiran seluruh jaringan rumah/kantor | AdGuard Home atau Pi-Hole |
| Android tanpa root | AdGuard / DNS66 / Blokada |
| Android dengan root | AdAway (Hosts) |
| Router atau server Linux | Dnsmasq |
| DNS server enterprise | BIND (RPZ) atau Unbound |
