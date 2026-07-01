# Validasi Filter

ABPindo menggunakan [AGLint](https://github.com/AdguardTeam/AGLint) untuk validasi sintaks filter secara otomatis.

---

## Gambaran Umum

AGLint memeriksa:

- **Modifier tidak valid** — opsi filter yang tidak dikenal atau salah posisi
- **Sintaks CSS tidak valid** — selector element hiding yang salah format
- **Domain tidak valid** — pola domain yang salah dalam aturan
- **Modifier duplikat** — modifier yang digunakan lebih dari sekali
- **Direktif preprocessor tidak valid** — penggunaan `!#if`, `!#endif` yang salah

---

## Penggunaan

### Command Line

```bash
# Install dependencies (pertama kali saja)
npm install

# Validasi semua filter
npm run lint

# Validasi direktori tertentu
npx aglint src/advert/*.txt

# Auto-fix masalah (hati-hati: overwrite file)
npx aglint 'src/**/*.txt' --fix
```

### Perintah Lainnya

```bash
# Full check: lint + build
npm run check

# Format source files
npm run format

# Cek duplikat lintas file
npm run check:duplicates
```

### CI/CD

Validasi berjalan otomatis:

- **Saat PR** — Memvalidasi semua file filter, gagal jika ada error
- **Saat push ke master** — Memvalidasi sebelum build

---

## Konfigurasi

AGLint dikonfigurasi melalui `.aglintrc.yaml`:

```yaml
root: true
extends:
  - aglint:recommended
syntax:
  - AdblockPlus
rules:
  invalid-modifiers: error
  no-invalid-css-syntax: error
  invalid-domain-list: warn
```

---

## Tingkat Kesalahan

| Level | Keterangan | Tindakan |
|-------|-----------|----------|
| **error** | Kesalahan sintaks yang akan merusak filter | Harus diperbaiki sebelum merge |
| **warning** | Potensi masalah atau sintaks usang | Disarankan untuk diperbaiki |

---

## Konfigurasi Inline

Anda dapat menonaktifkan AGLint untuk aturan tertentu:

```bash
# Nonaktifkan untuk baris berikutnya
! aglint-disable-next-line
example.com##.ad

# Nonaktifkan untuk blok
! aglint-disable
example.com##.ad
example.net##.ad
! aglint-enable
```

---

## Pipeline CI

```
File Sumber → FOP → AGLint → Build → Output
```
