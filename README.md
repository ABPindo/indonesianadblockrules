<p align="center"><img src="https://github.com/ABPindo/indonesianadblockrules/raw/master/src/ABPindo%202.png" width="240"></p>

# ABPindo
ABPindo merupakan daftar penapis/penyaring iklan di situs berbahasa Indonesia dan Malaysia, guna melengkapi penapis internasional seperti [EasyList](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easylist.txt&title=Easylist) atau [AdGuard Base filter](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_English/filter.txt). ABPindo menggunakan sintak [Adblock Plus](https://help.eyeo.com/en/adblockplus/how-to-write-filters), dan kompatibel dengan pengaya/ekstensi [Adblock Plus](https://adblockplus.org/), [uBlock Origin](https://github.com/gorhill/uBlock#installation), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html), atau adblocker sejenisnya. Kini ABPindo juga menyediakan dukungan dengan sintak host dan domain, yang kompatibel dengan [AdAway](https://github.com/AdAway/AdAway), [Pi-Hole](https://github.com/pi-hole/pi-hole), [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome), dan penapis berbasis DNS lainnya.

## Keuntungan
- Tampilan lebih bersih </br>
Tak perlu risih dengan iklan promosi, iklan judi, dan iklan dewasa
- Terjaga dari penipuan </br>
Lupakan iklan yang membaur/menyamar menjadi tombol update atau tombol download
- Lebih cepat </br>
Tanpa iklan waktu membuka laman web menjadi lebih singkat

## Cara Menggunakan
- Jalankan peramban web favoritmu (Firefox, Chrome, Opera, Safari, ...).
- Pasang pengaya/ekstensi [uBlock Origin](https://github.com/gorhill/uBlock#installation), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html), [Adblock Plus](https://adblockplus.org/en/), atau adblocker sejenisnya.
- Nyalakan filter ABPindo atau klik [subscribe ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo).

## Langganan Filter utama untuk browser
| Langganan|Raw File |Keterangan|
| ------------- | ----------------| -------------|
| [ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt)|Filter lengkap sebagai default [uBlock Origin](https://github.com/gorhill/uBlock#installation), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html), [Adblock Plus](https://adblockplus.org/en/) regional Indonesia dan Malaysia|
| [ABPindo_noadult](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noadult.txt&title=ABPindo_noadult)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noadult.txt)|ABPindo tanpa filter adult (judi) |
| [ABPindo_noelementhide](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noelemhide.txt&title=ABPindo_noelementhide)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noelemhide.txt)|ABPindo tanpa filter element hide|

## Variasi filter ABPindo untuk Pemblokir DNS
|Sintak|ABPindo*|ABPindo_adult**|Contoh|
| ------------- |-------------|-------------|-------------|
|Hosts [(AdAway)](https://github.com/AdAway/AdAway) |[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts_adult.txt)|`0.0.0.0 example.com`|
|Domain [(Pi-Hole)](https://github.com/pi-hole/pi-hole) |[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain_adult.txt)|`example.com`|
|Adblocker-syntax domains [(AdGuard Home)](https://github.com/AdguardTeam/AdGuardHome)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome_adult.txt)|`\|\|example.com^`|
|[Dnsmasq1](https://thekelleys.org.uk/gitweb/?p=dnsmasq.git)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_adult.txt)|`address=/example.com/0.0.0.0`|
|[Dnsmasq2](https://thekelleys.org.uk/gitweb/?p=dnsmasq.git)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_server.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_adult_server.txt)|`server=/example.com/`|
|RPZ (Response Policy Zone) [BIND](https://gitlab.isc.org/isc-projects/bind9.git)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/rpz.txt)|[Raw File](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/rpz_adult.txt)|`example.com CNAME .`|

Keterangan:
- Sintak penapis berbasis DNS memiliki cara kerja pemblokiran yang berbeda dari pengaya/ekstensi, sehingga untuk menghindari kesalahan blokir, default ABPindo pada penapis berbasis DNS hanya terdiri dari ABPindo_adserver dan ABPindo_third-party.
- *ABPindo terdiri dari domain ABPindo_adserver dan ABPindo_third-party.
- **ABPindo_adult terdiri dari domain ABPindo_adserver, ABPindo_third-party dan ABPindo_adult (iklan judi dan dewasa).

## Ingin berkontribusi
Masih ada situs yang terlewat, entah karena situsnya telah diperbarui atau karena situsnya belum dijangkau ABPindo. Jika menemukan hal-hal tersebut bisa berkontribusi langsung melalui:
- [GitHub issue tracker](https://github.com/ABPindo/indonesianadblockrules/issues)
- [Submit a pull request](https://github.com/ABPindo/indonesianadblockrules/pulls)

## Pengaturan standar
Lingkungan pengujian Kami sebagai berikut:
- Peramban [Firefox](https://www.mozilla.org/id/firefox/).
- Pengaya [uBlock Origin](https://github.com/gorhill/uBlock#installation).
- Filter : [EasyList](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easylist.txt&title=Easylist), [EasyPrivacy](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easyprivacy.txt&title=EasyPrivacy), [ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo) dan [uBlock filters](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt&title=uBlock%20filters).

## Bagi pengembang
- [Kebijakan ABPindo tentang iklan](https://easylist.to/pages/policy.html)
- [How to write filters | Adblock Plus Help Center](https://help.eyeo.com/en/adblockplus/how-to-write-filters)
- [uBlock Static filter syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax)
- [DNS filtering rules syntax | AdGuard DNS Knowledge Base](https://adguard-dns.io/kb/general/dns-filtering-syntax/)
- [Python-abp : utilitas untuk rendering filter ABPindo](https://github.com/adblockplus/python-abp)
- Prasyarat: [Python](https://www.python.org/downloads/), [pip](https://pypi.org/project/pip/)

## Mirror
- [ABPindo GitLab](https://gitlab.com/ABPindo)
- [ABPindo GitLab Subscription](https://subscribe.adblockplus.org/?location=https://gitlab.com/ABPindo/indonesianadblockrules/raw/master/subscriptions/abpindo.txt&title=ABPindo)
