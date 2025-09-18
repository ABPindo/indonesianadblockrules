<p align="center"><img src="https://github.com/ABPindo/indonesianadblockrules/raw/master/src/ABPindo%202.png" width="240"></p>

# NOTE: [baca wiki tentang jendela pop-up](https://github.com/ABPindo/indonesianadblockrules/wiki/Panduan-Memblokir-Popup)

# ABPindo

ABPindo adalah daftar penapis iklan untuk situs berbahasa Indonesia dan Malaysia, yang melengkapi penapis internasional seperti [EasyList](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easylist.txt&title=Easylist) dan [AdGuard Base filter](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt). ABPindo menggunakan sintaks [Adblock Plus](https://help.eyeo.com/en/adblockplus/how-to-write-filters) dan kompatibel dengan ekstensi seperti [Adblock Plus](https://adblockplus.org/), [uBlock Origin](https://github.com/gorhill/uBlock#installation), [uBlock Origin Lite (Chrome dan Chromium-Based)](https://chromewebstore.google.com/detail/ublock-origin-lite/ddkjiahejlhfcafbddmgiahcphecmpfh), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html), dan adblocker sejenis. Kini, ABPindo juga menyediakan penapis berbasis sintaks host dan domain, kompatibel dengan [AdAway](https://github.com/AdAway/AdAway), [Pi-Hole](https://github.com/pi-hole/pi-hole), [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome), dan penapis berbasis DNS lainnya.

## Keuntungan
- **Lebih Bersih**: Tanpa iklan promosi berlebihan, iklan judi, dan iklan dewasa
- **Terhindar dari Penipuan**: Tanpa iklan yang menyamar sebagai tombol update, stream atau download
- **Lebih Cepat**: Tanpa iklan, waktu membuka laman web menjadi lebih singkat

## Cara Menggunakan
1. Jalankan peramban web favorit Anda (Firefox, Chrome, Opera, Safari, dll).
2. Pasang ekstensi [uBlock Origin](https://github.com/gorhill/uBlock#installation), [uBlock Origin Lite (Chrome dan Chromium-Based)](https://chromewebstore.google.com/detail/ublock-origin-lite/ddkjiahejlhfcafbddmgiahcphecmpfh), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html), [Adblock Plus](https://adblockplus.org/en/), atau adblocker sejenis.
3. Nyalakan filter ABPindo dengan klik [subscribe ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo).
4. Atau, salin tautan dari kolom **Raw File** dan tambahkan secara manual melalui pengaturan filter di ekstensi.

**NOTE:** Apabila menggunakan uBlock origin Lite maka [setel default filtering mode ke complete](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/refs/heads/master/docs/455486093-4bc27a5b-6dcb-406d-b46e-13092ece89c8.png) untuk memastikan bahwa semua elemen iklan terblokir.

## Variasi filter ABPindo untuk Pemblokir browser
| Langganan|Raw File |Keterangan|
| ------------- | ----------------| -------------|
| [ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt)|Filter lengkap sebagai default [uBlock Origin](https://github.com/gorhill/uBlock#installation), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html), [Adblock Plus](https://adblockplus.org/en/) regional Indonesia dan Malaysia|
| [ABPindo - No Adult](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noadult.txt&title=ABPindo_noadult)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noadult.txt)|ABPindo tanpa filter adult (judi) |
| [ABPindo - No Element Hiding](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noelemhide.txt&title=ABPindo_noelementhide)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noelemhide.txt)|ABPindo tanpa filter element hide|
| [ABPindo - Annoyance](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_annoyances.txt&title=ABPindo_annoyance)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_annoyances.txt)|Filter annoyances (elemen UI yang menggangu seperti popup/overlay non iklan dan pemutar video otomatis) |
| [ABPindo - Extended](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_extended.txt&title=ABPindo_extended)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_extended.txt)|Filter ujicoba, dan filter residu hasil [PyFunceble](https://github.com/funilrys/PyFunceble) atau [DeadDomainsLinter](https://github.com/AdguardTeam/DeadDomainsLinter) yang masih mungkin muncul kembali |
---

## Variasi filter ABPindo untuk Pemblokir DNS
|Sintak|ABPindo*|ABPindo_adult**|Contoh|
| ------------- |-------------|-------------|-------------|
|Hosts (Hosts file, [AdAway](https://github.com/AdAway/AdAway), [DNS66](https://f-droid.org/id/packages/org.jak_linux.dns66/), [NetGuard](https://netguard.me/), [personalDNSfilter](https://play.google.com/store/apps/details?id=dnsfilter.android&hl=id))|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts_adult.txt)|`0.0.0.0 example.com`|
|Domain ([Pi-Hole](https://github.com/pi-hole/pi-hole), [DNSCrypt](https://dnscrypt.info/)) |[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain_adult.txt)|`example.com`|
|Adblocker-syntax domains ([AdGuard Home](https://github.com/AdguardTeam/AdGuardHome), [Pi-Hole](https://github.com/pi-hole/pi-hole)) |[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome_adult.txt)|`\|\|example.com^`|
|[Dnsmasq1](https://thekelleys.org.uk/gitweb/?p=dnsmasq.git)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_adult.txt)|`address=/example.com/0.0.0.0`|
|[Dnsmasq2](https://thekelleys.org.uk/gitweb/?p=dnsmasq.git)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_server.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_adult_server.txt)|`server=/example.com/`|
|RPZ (Response Policy Zone) [BIND](https://gitlab.isc.org/isc-projects/bind9.git)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/rpz.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/rpz_adult.txt)|`example.com CNAME .`|
|[UNBOUND](https://github.com/NLnetLabs/unbound)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/unbound.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/unbound_adult.txt)|`local-zone: "example.com" always_nxdomain`|

**Keterangan**:
- Sintaks penapis berbasis DNS memiliki cara kerja yang berbeda dari ekstensi, sehingga untuk menghindari kesalahan blokir, default ABPindo pada penapis berbasis DNS hanya terdiri dari `src/advert/adservers.txt` dan `src/advert/thirdparty.txt`.
- *Host ABPindo terdiri dari domain `src/advert/thirdparty.txt` dan `src/advert/thirdparty.txt`.
- **Host ABPindo_adult terdiri dari domain `src/advert/thirdparty.txt`, `src/advert/thirdparty.txt`, dan `src/adult/adult_thirdparty.txt`.

## Ingin Berkontribusi 🤝
Masih ada situs yang terlewat, entah karena situsnya telah diperbarui atau belum dijangkau ABPindo. Jika menemukan hal-hal tersebut, Anda bisa berkontribusi langsung melalui:
- [GitHub issue tracker](https://github.com/ABPindo/indonesianadblockrules/issues)
- [Submit a pull request](https://github.com/ABPindo/indonesianadblockrules/pulls)

## Pengaturan Standar ⚙️
Lingkungan pengujian kami sebagai berikut:
- Peramban [Firefox](https://www.mozilla.org/id/firefox/)
- Ekstensi [uBlock Origin](https://github.com/gorhill/uBlock#installation)
- Filter: [EasyList](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easylist.txt&title=Easylist), [EasyPrivacy](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easyprivacy.txt&title=EasyPrivacy), [ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo), dan [uBlock filters](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt&title=uBlock%20filters)

## Bagi Pengembang 🛠️
- [Kebijakan ABPindo tentang Iklan](https://easylist.to/pages/policy.html)
- [How to Write Filters | Adblock Plus Help Center](https://help.eyeo.com/en/adblockplus/how-to-write-filters)
- [uBlock Static Filter Syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax)
- [DNS Filtering Rules Syntax | AdGuard DNS Knowledge Base](https://adguard-dns.io/kb/general/dns-filtering-syntax/)
- [Python-abp: Utilitas untuk Rendering Filter ABPindo](https://github.com/adblockplus/python-abp)
- [PyFunceble: Utilitas untuk Cek Domain ABPindo](https://github.com/funilrys/PyFunceble)
- [Adblock-decoder: Utilitas untuk Konversi Filter ABPindo ke Format Hosts dan Plain Text](https://github.com/PyFunceble/adblock-decoder)
- Prasyarat: [Python](https://www.python.org/downloads/), [pip](https://pypi.org/project/pip/)

## Mirror 🔗
- [ABPindo GitLab](https://gitlab.com/ABPindo)
- [ABPindo GitLab Subscription](https://subscribe.adblockplus.org/?location=https://gitlab.com/ABPindo/indonesianadblockrules/raw/master/subscriptions/abpindo.txt&title=ABPindo)
