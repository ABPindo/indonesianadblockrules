# Setup: DNS Blocker

ABPindo menyediakan filter dalam format yang kompatibel dengan berbagai pemblokir berbasis DNS. Pilih software yang Anda gunakan, lalu salin URL filter yang sesuai.

---

## Daftar URL Filter per Software

| Software | Format | URL Filter |
|---|---|---|
| [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) | Adblocker-syntax | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome.txt` |
| [Pi-Hole](https://pi-hole.net) | Domain / Adblocker-syntax | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt` |
| [AdAway](https://adaway.org) | Hosts | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts.txt` |
| [AdGuard](https://adguard.com) (Android/iOS) | Adblocker-syntax | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome.txt` |
| [DNS66](https://f-droid.org/packages/org.jak_linux.dns66/) | Domain | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt` |
| [Blokada 4](https://blokada.org) | Domain | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt` |
| [personalDNSfilter](https://zenz-solutions.de/personaldnsfilter/) | Domain | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt` |
| [HostsMan](https://www.abelhadigital.com/hostsman/) | Hosts | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts.txt` |
| [Dnsmasq](https://thekelleys.org.uk/dnsmasq/doc.html) (address) | Dnsmasq | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq.txt` |
| [Dnsmasq](https://thekelleys.org.uk/dnsmasq/doc.html) (server) | Dnsmasq | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_server.txt` |
| [BIND RPZ](https://gitlab.isc.org/isc-projects/bind9.git) | RPZ | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/rpz.txt` |
| [Unbound](https://github.com/NLnetLabs/unbound) | Unbound | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/unbound.txt` |

### Versi + Adult (Judi & Konten Dewasa)

Untuk memblokir domain judi dan konten dewasa, gunakan URL berikut sebagai tambahan atau pengganti:

| Format | URL Filter |
|---|---|
| Hosts | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts_adult.txt` |
| Domain | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain_adult.txt` |
| Adblocker-syntax | `https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome_adult.txt` |

---

## Panduan Umum

### AdGuard Home

1. Buka dashboard AdGuard Home.
2. Masuk ke **Filters > DNS blocklists**.
3. Klik **Add blocklist > Add a custom list**.
4. Isi nama (misal: `ABPindo`) dan URL filter yang sesuai.
5. Klik **Save**.

### Pi-Hole

1. Buka dashboard Pi-Hole.
2. Masuk ke **Group Management > Adlists**.
3. Tempel URL filter di kolom **Address**.
4. Klik **Add**, lalu jalankan `pihole -g` di terminal untuk memperbarui.

### AdAway (Android)

1. Buka AdAway.
2. Masuk ke **Host sources**.
3. Klik tombol tambah (**+**) dan tempel URL filter hosts.
4. Klik **Apply ad blocking**.

---

## Catatan Penting

> Penapis berbasis DNS memblokir di level **domain**, bukan di level elemen halaman. Cara kerjanya berbeda dari ekstensi browser. Untuk pengalaman pemblokiran terlengkap, gunakan ABPindo bersamaan dengan ekstensi browser (uBlock Origin / AdGuard) jika memungkinkan.

Cakupan default filter DNS ABPindo lebih konservatif dibanding versi ekstensi, untuk menghindari *false positive* yang memutus akses ke situs yang tidak berhubungan dengan iklan.
