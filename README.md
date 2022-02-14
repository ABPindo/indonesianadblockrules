<p align="center"><img src="https://github.com/ABPindo/indonesianadblockrules/raw/master/src/ABPindo%202.png" width="240"></p>

# ABPindo
ABPindo merupakan filter tambahan untuk melengkapi [EasyList](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easylist.txt&title=Easylist) memblokir iklan mengganggu di situs berbahasa Indonesia dan Malaysia. ABPindo menggunakan sintak: 

[Adblock Plus](https://help.eyeo.com/en/adblockplus/how-to-write-filters)

[Domain, Hosts, Adblocker-syntax domains](https://kb.adguard.com/en/general/dns-filtering-syntax)

[Dnsmasq](https://github.com/imp/dnsmasq/blob/master/dnsmasq.conf.example)

[BIND](https://www.isc.org/docs/BIND_RPZ.pdf) 

Dan kompatibel dengan:

Pengaya/ekstensi browser (mis. [Adblock Plus](https://adblockplus.org), [uBlock Origin](https://github.com/gorhill/uBlock#installation), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html))

Software pemblokir iklan berbasis DNS maupun Jaringan (mis. [AdGuard](https://adguard.com/id/welcome.html), [personalDNSfilter](https://zenz-solutions.de/personaldnsfilter/), [AdAway](https://adaway.org))

Software server DNS (mis. [Pi-Hole](https://pi-hole.net), [AdGuard Home](https://adguard.com/en/adguard-home/overview.html), [Dnsmasq](https://thekelleys.org.uk/dnsmasq/doc.html), [BIND](https://www.isc.org/bind/))
## Keuntungan
- Tampilan lebih bersih </br>
Kita bisa lebih fokus terhadap konten website, tanpa risih atau terganggu oleh iklan.
- Terjaga dari penipuan </br>
Banyak iklan yang membaur bahkan menyamar menjadi tombol pembaruan program/ tombol download, setidaknya kita dapat terhindar dari penipuan.
- Lebih cepat </br>
Iklan animasi/video menjadi masalah bagi pengguna internet dengan akses terbatas. Tanpa iklan tersebut waktu membuka laman web menjadi lebih singkat.

## Cara Menggunakan
# Dengan Ekstensi
- Jalankan peramban web favoritmu (Firefox, Chrome, Opera, Safari, Samsung Internet ...).
- Pasang pengaya/ekstensi yang mendukung sintak sintak Adblock Plus/Hosts/Domain/Adblocker-syntax domains (mis. [uBlock Origin](https://github.com/gorhill/uBlock#installation), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html), [Adblock Plus](https://adblockplus.org/))
- Klik [subscribe ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo) atau pilih variasi sesuai kebutuhan.
# Dengan Software 
- Pasang software pemblokir iklan yang mendukung sintak Adblock Plus/Hosts/Domain/Adblocker-syntax domains (mis. [AdGuard](https://adguard.com/id/welcome.html), [personalDNSfilter](https://zenz-solutions.de/personaldnsfilter/) [AdAway](https://adaway.org)
- Copy link filter sesuai dengan sintak yang kompatibel dengan software
- Tambahkan filter sesuai dengan sintak yang kompatibel dengan software,(AdGuard:Adblock Plus/Hosts/Domain/Adblocker-syntax domains, personalDNSfilter: Hosts/Domain, AdAway:Hosts)
## Langganan Filter utama (sintak Adblock Plus)
| Langganan|Keterangan|
| ------------- |-------------|
| [ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo)|Filter lengkap sebagai default [uBlock Origin](https://github.com/gorhill/uBlock#installation), [Adblock Plus](https://adblockplus.org/en/), [AdGuard](https://adguard.com/en/adguard-browser-extension/overview.html) regional Indonesia dan Malaysia|
| [ABPindo_noannoyance](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noannoyance.txt&title=ABPindo_noannoyance)|ABPindo tanpa filter annoyance (judi) |
| [ABPindo_noelementhide](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo_noelemhide.txt&title=ABPindo_noelementhide)|ABPindo tanpa filter element hide|

## Variasi filter ABPindo untuk software pemblokir berbasis DNS dan software server DNS
|Sintak|ABPindo*|ABPindo_annoyance**|Contoh|
| ---------------- |-------------|-------------|-------------|
|Hosts [(AdAway)](https://github.com/AdAway/AdAway) |[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts.txt)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts_annoyance.txt)|`0.0.0.0 example.com`|
|Domain [(Pi-Hole)](https://github.com/pi-hole/pi-hole) |[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain_annoyance.txt)|`example.com`|
|Adblocker-syntax domains [(AdGuard Home)](https://github.com/AdguardTeam/AdGuardHome)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome.txt)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/aghome_annoyance.txt)|`\|\|example.com^`|
|[Dnsmasq1](http://thekelleys.org.uk/gitweb/?p=dnsmasq.git)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq.txt)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_annoyance.txt)|`address=/example.com/0.0.0.0`|
|[Dnsmasq2](http://thekelleys.org.uk/gitweb/?p=dnsmasq.git)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_server.txt)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/dnsmasq_annoyance_server.txt)|`server=/example.com/`|
|RPZ (Respone Policy Zone) [(BIND)](https://gitlab.isc.org/isc-projects/bind9.git)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/rpz.txt)|[link](https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/rpz_annoyance.txt)|`example.com CNAME .`|

Keterangan:
- *Filter default yang terdiri dari domain ABPindo_adserver dan ABPindo_third-party
- **Filter default ditambah ABPindo_annoyance (judi)
- Sintak DNS blocker memiliki kemampuan pemblokiran yang berbeda dengan versi sintak Adblock Plus, sehingga untuk menghindari kesalahan blokir terdiri dari ABPindo_adserver dan ABPindo_third-party

## Ingin berkontribusi
Masih ada situs yang terlewat, entah karena situsnya telah diperbarui atau karena situsnya belum terjangkau oleh ABPindo. Jika menemukan hal-hal tersebut bisa berkontribusi langsung melalui:
- [GitHub issue tracker](https://github.com/ABPindo/indonesianadblockrules/issues)
- [Submit a pull request](https://github.com/ABPindo/indonesianadblockrules/pulls)

## Pengaturan standar
Lingkungan pengujian Kami sebagai berikut:
- Peramban [Firefox](https://www.mozilla.org/id/firefox/).
- Pengaya [uBlock Origin](https://github.com/gorhill/uBlock#installation).
- Filter : [EasyList](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easylist.txt&title=Easylist), [EasyPrivacy](https://subscribe.adblockplus.org/?location=https://easylist.to/easylist/easyprivacy.txt&title=EasyPrivacy), [ABPindo](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt&title=ABPindo) dan [uBlock filters](https://subscribe.adblockplus.org/?location=https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt&title=uBlock%20filters).

## Bagi pengembang
- [Kebijakan ABPindo tentang iklan](https://easylist.to/pages/policy.html)
- [Adblock Plus filters explained](https://adblockplus.org/filter-cheatsheet)
- [uBlock Origin Static filter syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax)
- [DNS filtering rules syntax | AdGuard Knowledgebase](https://kb.adguard.com/en/general/dns-filtering-syntax)
- [dnsmasq/dnsmasq.conf.example at master · imp/dnsmasq](https://github.com/imp/dnsmasq/blob/master/dnsmasq.conf.example)
- [Tutorial on Configuring BIND to use Response Policy Zones](https://www.isc.org/docs/BIND_RPZ.pdf)
- [Python-abp : utilities untuk rendering filter ABPindo](https://github.com/adblockplus/python-abp)
- Prasyarat: [Python](https://www.python.org/downloads/), [pip](https://pypi.org/project/pip/)

## Mirror
- [ABPindo GitLab](https://gitlab.com/ABPindo)
- [ABPindo GitLab Subscription](https://subscribe.adblockplus.org/?location=https://gitlab.com/ABPindo/indonesianadblockrules/raw/master/subscriptions/abpindo.txt&title=ABPindo)
