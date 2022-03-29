| Nama File | Keterangan | Contoh|
| --------- | ---------- | ----- |
| abpindo_adservers.txt | Domain penyedia layanan iklan pihak ketiga | `domainikan.id^$thirdparty` |
| abpindo_general_block.txt | Filter blokir umum, gunakan dengan bijak agar memfilter iklan saja | `.id/ikan/` |
| abpindo_general_hide.txt | Filter penyembunyi umum, gunakan dengan bijak agar menyembunyikan iklan saja| `##.ikan` |
| abpindo_specific_block.txt | Filter spesifik iklan, sampai tuntas ektensi file yang diblokir | `domainikan.id/ikan.jpg` |
| abpindo_specific_hide.txt | Filter penyembunyi spesifik dengan domain dan class | `domainikan##.ikan` |
| abpindo_specific_ublock.txt | Filter sintak khusus pengguna [uBlock Origin](https://github.com/https://github.com/gorhill/uBlock/wiki/Static-filter-syntax) | `domainikan##+js(defuser.js)` |
| abpindo_thirdparty.txt | Filter domain penyedia iklan, tidak mesti domain khusus iklan saja | `domaingambar.id^$thirdparty` |
| abpindo_whitelist.txt | Memperbaiki kesalahan filter agar fitur situs bisa digunakan secara normal | `@@ikanlele.jpg` |
| abpindo_annoyance_general_block.txt | Filter blokir umum untuk situs judi | - |
| abpindo_annoyance_general_hide.txt | Filter penyembunyi umum untuk situs judi | - |
| abpindo_annoyance_thirdparty.txt | Filter domain penyedia layanan judi pihak ketiga | - |
| abpindo_annoyance_prank.txt |Filter khusus prank, mengagetkan, diluar nalar | `killerjo` |
