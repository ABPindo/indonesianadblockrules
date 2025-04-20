| Nama File                     | Keterangan                                                                 | Contoh                                   |
|-------------------------------|---------------------------------------------------------------------------|------------------------------------------|
| `adservers.txt`              | Domain penyedia layanan iklan pihak ketiga                               | `domainikan.id^$thirdparty`             |
| `general_block.txt`          | Filter blokir umum; gunakan dengan bijak agar hanya memfilter iklan      | `.id/ikan/`                              |
| `general_hide.txt`           | Filter penyembunyi umum; gunakan dengan bijak agar hanya menyembunyikan iklan | `##.ikan`                               |
| `specific_block.txt`         | Filter spesifik iklan; blokir hingga tuntas ekstensi file yang diblokir  | `domainikan.id/ikan.jpg`                |
| `specific_hide.txt`          | Filter penyembunyi spesifik dengan domain dan class                      | `domainikan##.ikan`                      |
| `specific_ublock.txt`        | Filter sintaks khusus pengguna [uBlock Origin](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax) | `domainikan##+js(defuser.js)`           |
| `thirdparty.txt`             | Filter domain penyedia iklan; tidak mesti domain khusus iklan saja       | `domaingambar.id^$thirdparty`           |
| `allowlist.txt`              | Memperbaiki kesalahan filter agar fitur/fungsi situs tetap bisa digunakan secara normal | `@@ikanlele.jpg`                         |
| `adult_general_block.txt`    | Filter blokir umum untuk iklan judi/dewasa                                 | -                                        |
| `adult_general_hide.txt`     | Filter penyembunyi umum untuk iklan judi/dewasa                            | -                                        |
| `adult_thirdparty.txt`       | Filter domain penyedia layanan judi/dewasa pihak ketiga                    | -                                        |
| `adult_prank.txt`            | Filter khusus prank; mengagetkan, di luar nalar                         | `killerjo`                               |
