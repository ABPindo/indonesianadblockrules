# Manajemen Domain Mati

ABPindo menggunakan [`@adguard/dead-domains-linter`](https://github.com/AdguardTeam/DeadDomainsLinter) untuk mendeteksi domain mati dengan **alur kerja dua fase**.

---

## Cara Kerja

```
Tanggal 1:     Ekspor domain mati → File hasil dibuat
Tanggal 1–14:  Review dan hapus false positive
Tanggal 15:    Impor otomatis (jika belum direview)
```

---

## Alur Kerja

| Workflow | Jadwal | Aksi |
|----------|--------|------|
| `dead-domain-export.yml` | Tanggal 1 setiap bulan | Ekspor domain mati ke file |
| `dead-domain-import.yml` | Tanggal 15 setiap bulan | Impor otomatis (jika belum direview) |

---

## File Ekspor

| File | Sumber |
|------|--------|
| `src/advert/dead_advert.txt` | Domain mati dari filter iklan |
| `src/adult/dead_adult.txt` | Domain mati dari filter dewasa |

---

## Review Manual (Opsional)

Jika ingin melakukan review sebelum impor otomatis:

```bash
# 1. Buka dan review dead_advert.txt
#    - Hapus baris yang merupakan false positive (domain yang masih aktif)

# 2. Impor daftar yang sudah direview
dead-domains-linter -i "src/advert/*.txt" --import=src/advert/dead_advert.txt --auto

# 3. Buka dan review dead_adult.txt

# 4. Impor daftar yang sudah direview
dead-domains-linter -i "src/adult/*.txt" --import=src/adult/dead_adult.txt --auto

# 5. Commit
git add src/ && git commit -m "chore: remove reviewed dead domains"
```

---

## Perintah Manual

```bash
# Ekspor domain mati (scan saja, tanpa modifikasi)
dead-domains-linter -i "src/advert/*.txt" --export src/advert/dead_advert.txt
dead-domains-linter -i "src/adult/*.txt" --export src/adult/dead_adult.txt

# Impor dan hapus (setelah review)
dead-domains-linter -i "src/advert/*.txt" --import=src/advert/dead_advert.txt --auto
dead-domains-linter -i "src/adult/*.txt" --import=src/adult/dead_adult.txt --auto
```

---

## Linimasa

| Tanggal | Keterangan |
|---------|-----------|
| Tanggal 1 | Ekspor berjalan, commit dibuat |
| Tanggal 1–14 | Jendela review |
| Tanggal 15 | Impor otomatis berjalan (jika file berisi konten) |

---

## Praktik Terbaik

- Review `dead_advert.txt` dan `dead_adult.txt` ketika melihat commit ekspor
- Hapus false positive sebelum tanggal 15
- Jika mengimpor secara manual lebih awal, impor otomatis tidak akan menemukan apa pun
