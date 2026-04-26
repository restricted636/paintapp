# 🎨 ColorMix – Boya Karıştırma ve Renk Paleti Yönetim Sistemi

ColorMix, kullanıcıların kendi renklerini oluşturabildiği, karıştırabildiği ve paletler hâlinde yönetebildiği; ayrıca topluluk paylaşımlarıyla renk fikirlerini keşfedebildiği **offline–online hibrit** bir uygulama setidir.  
Bu repo Flutter mobil uygulamasını, React web panelini, React Native sürümünü ve PostgreSQL destekli API’yi kapsar.

---

## 🧱 Proje Bileşenleri

| Klasör              | Teknoloji                      | Açıklama                     |
| ------------------- | ------------------------------ | ---------------------------- |
| **/mobile-flutter** | Flutter (Dart)                 | Ana mobil uygulama           |
| **/backend**        | Node.js (Express) veya FastAPI | RESTful API + PostgreSQL     |
| **/web-react**      | React.js                       | Yönetici / keşif paneli      |
| **/mobile-react**   | React Native                   | Alternatif mobil sürüm       |
| **/docs**           | Markdown + Mermaid             | Dokümantasyon ve diyagramlar |

---

## ⚙️ Özellikler

- 🔒 Kullanıcı kaydı, giriş ve profil yönetimi
- 🎨 Renk oluşturma (RGB, HSL, CMYK, LAB dönüşümleri – offline)
- 🧪 Renk karıştırma (canlı veya butonla hesaplama)
- 🖼️ Görselden tek piksel renk alma (zoom destekli)
- 🪣 Palet oluşturma, tag ekleme, açıklama yazma
- 📤 Public palet paylaşımı, beğeni ve kopyalama
- 📶 Offline-first mimari, online senkronizasyon
- 🌗 Tema, görünüm ve varsayılan renk modeli ayarları

---

## 🗃️ Veritabanı Şeması (ERD)

![ERD Diagram](docs/erd_diagram.png)

---

## 🌐 API Akış Diyagramı

![API Flow Diagram](docs/api_flow_diagram.png)

---

## 🧭 Proje Dizini Yapısı
