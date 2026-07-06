# Setup khusus Google Chrome

Masalah utama yang sering dihadapi user Google Chrome adalah keterlambatan update filter yang terjadi pada uBlock Origin Lite karena [Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3) yang [membatasi semua ekstensi pemblokir iklan](https://adblock-tester.com/ad-blockers/manifest-v3-ad-blocker-impact/) di browser berbasis chromium (tidak termasuk pemblokir iklan bawaan seperti Brave, Opera, Vivaldi, juga model ekstensi Samsung Internet Android). yang mengharuskan uBlock Origin Lite untuk mem-bundle semua filter yang tersedia didalamnya ke paket ekstensi (Baik EasyList dan ABPindo) sehingga update filter tidak bisa dilakukan serta-merta dari repositori ini, melalui harus menunggu update ekstensi.

Tetapi kami telah menemukan bahwa AdGuard for Chrome [telah mengakali hal ini](https://adguard.com/en/blog/review-issues-in-chrome-web-store.html) supaya pengguna dapat menambahkan filter sendiri (custom filter ini ditetapkan sebagai dynamic rules), dan juga memiliki [frekuensi update ekstensi + filter bawaan (pre-bundled seperti AdGuard Base filter) yang lebih sering](https://github.com/AdguardTeam/AdguardBrowserExtension#auto-update-cycle) (filter pre-bundled ini ditetapkan sebagai static rules). Berikut langkah-langkah instalasi dan konfigurasi AdGuard for Chrome

- 1. Install AdGuard for Chrome dari Chrome Webstore melalui [link ini](https://chromewebstore.google.com/detail/adguard-adblocker/bgnkhhnnamicmpeenaelnjfhikgbkllg)

![](assets/chrome-adguard-setup/fig1.png)

- 2. Begitu terinstal ekstensi akan memuat halaman setup pertama

![](assets/chrome-adguard-setup/fig2.png)

- 3. Skip halaman ini

![](assets/chrome-adguard-setup/fig3.png)

- 4. Pin ekstensi ke toolbar untuk akses yang lebih mudah

![](assets/chrome-adguard-setup/fig4.png)

- 5. (Direkomendasikan) Nyalakan filter pemblokir pelacak

![](assets/chrome-adguard-setup/fig5.png)

- 6. (Opsional) Nyalakan filter social widgets dan self-promotion

![](assets/chrome-adguard-setup/fig6.png)
![](assets/chrome-adguard-setup/fig7.png)

- 7. (PENTING) Hidupkan izin "Allow User Scripts" untuk menghidupkan opsi custom filter. Ikuti petunjuk di gambar

![](assets/chrome-adguard-setup/fig8.png)
![](assets/chrome-adguard-setup/fig9.png)
![](assets/chrome-adguard-setup/fig10.png)
![](assets/chrome-adguard-setup/fig11.png)

- 8. Pergi ke [halaman utama ABPindo](https://github.com/ABPindo/indonesianadblockrules) dan klik Subscribe ABPindo. Ikuti petunjuk di gambar

![](assets/chrome-adguard-setup/fig12.png)
![](assets/chrome-adguard-setup/fig13.png)
![](assets/chrome-adguard-setup/fig14.png)
![](assets/chrome-adguard-setup/fig15.png)

- 8. Anda juga dapat subscribe ke ABPindo Annoyances. Pergi ke [Variasi filter ABPindo](https://github.com/ABPindo/indonesianadblockrules#variasi-filter) dan klik Subscribe ABPindo - Annoyance. Ikuti petunjuk di gambar

![](assets/chrome-adguard-setup/fig16.png)
![](assets/chrome-adguard-setup/fig17.png)
![](assets/chrome-adguard-setup/fig18.png)
![](assets/chrome-adguard-setup/fig19.png)

# Limitasi

AdGuard sendiri memiliki limitasi terhadap jumlah custom filter yang ditambahkan untuk mengikuti kompatibilitas Manifest V3. anda dapat melihat sisa limit anda [di sini](chrome-extension://bgnkhhnnamicmpeenaelnjfhikgbkllg/pages/options.html#/rule-limits) dengan contoh seperti ini:

![](assets/chrome-adguard-setup/fig20.png)
