# 🎨 Boya Karıştırma ve Renk Paleti Yönetim Sistemi (ColorMix)
**Sürüm:** v1.0  
**Tarih:** 26 Nisan 2026  
**Hazırlayan:** [Senin Adın]

---

## 🧱 Proje Tanımı

ColorMix, ressamlar, tasarımcılar ve renklerle ilgilenen kullanıcılar için geliştirilmiş bir uygulama serisidir.  
Kullanıcılar kendi renklerini oluşturabilir, karıştırabilir, paletler haline getirebilir ve bunları toplulukla paylaşabilir.  
Proje üç ana parça halinde geliştirilir: **mobil uygulama (Flutter)**, **web paneli (React)**, **backend (Express/FastAPI + PostgreSQL)**.

---

## ⚙️ Mimari Yaklaşım

### Offline-first yapı
- Kullanıcı renk ve palet verilerini cihazında saklar (Isar / Sqflite).  
- İnternete bağlandığında yalnızca public içeriklerin senkronizasyonu yapılır.  
- PostgreSQL yalnızca merkezî veri deposu olarak görev yapar.

### Senkronizasyon Mantığı
- Her kullanıcıya ait kayıtlar `local_id` ile etiketlenir.  
- Online modda `/sync` endpoint’i aracılığıyla PostgreSQL verisiyle eşitlenir.

---

## 🧩 Ana Özellikler

### Renk Yönetimi
- Bağımsız renk kaydı oluşturma  
- Renk değerleri: HEX, RGB, CMYK, LAB, HSL  
- Dönüşümler uygulama içinde (lokal) yapılır  
- Not ve isim eklenebilir  

### Palet Yönetimi
- İsim, açıklama ve tag ekleme  
- Tag’ler `TEXT[]`, **büyük–küçük harf duyarsız**
- Kullanıcı istediği kadar tag girebilir (`doğa`, `soğuk_tonlar` vb.)
- Public paletler tamamen açık, giriş gerekmez  
- Palet işlemleri: oluştur, düzenle, sil, public et  
- Görsel gösterim: patch formatında (renk blokları)

### Renk Karıştırma
- Kullanıcı 2–5 renk seçer  
- Her biri için artı–eksi butonlu sayı alanı ve slider bulunur  
- Slider yalnızca ilgili rengin oranını değiştirir  
- Sonuç karışımı canlı güncellenir  
- Hedef renk (ters karışım) hesaplaması butonla yapılır  

### Resimden Renk Seçimi
- Tek piksel seçimi  
- Görüntü yakınlaştırma / kaydırma destekli (`InteractiveViewer`)  
- Seçilen renk “Renk oluştur” ekranına eklenir  

### Topluluk Modu
- Public paletler herkes tarafından görülebilir  
- Kullanıcı:
  - 👍 beğenebilir  
  - 📂 kendi hesabına kopyalayabilir  
  - 🔗 paylaşabilir  
- İstatistik: beğeni ve kopya sayıları  

### Yardım Sayfası
- Statik metin ve örnek görseller  
- Konular: uygulama kullanımı, renk teorisi, modellerin farkı, karışım mantığı  
- Basit geçiş animasyonları (Lottie/AnimatedContainer)  

### Ayarlar
- Tema: açık / koyu (varsayılan koyu)  
- Görünüm: liste / grid (varsayılan liste)  
- Karışım modu: canlı / manuel hesaplama  
- Varsayılan renk modeli: RGB, HSL, LAB  
- Cloud senkronizasyon: aç/kapa  

---

## 🗃️ Veritabanı Şeması

```plaintext
users
 ├─ id
 ├─ username
 ├─ email
 ├─ password_hash
 ├─ avatar_url
 └─ created_at

colors
 ├─ id
 ├─ user_id → users.id
 ├─ hex_code
 ├─ rgb_r, rgb_g, rgb_b
 ├─ cmyk_c, cmyk_m, cmyk_y, cmyk_k
 ├─ lab_l, lab_a, lab_b
 ├─ h, s, l
 ├─ name
 ├─ note
 └─ created_at

palettes
 ├─ id
 ├─ user_id → users.id
 ├─ name
 ├─ description
 ├─ is_public
 ├─ tags[]
 └─ created_at

palette_colors
 ├─ id
 ├─ palette_id → palettes.id
 ├─ color_id → colors.id
 └─ ratio

mix_results
 ├─ id
 ├─ palette_id → palettes.id
 ├─ result_color_id → colors.id
 ├─ target_color_id → colors.id
 ├─ accuracy
 └─ created_at

likes
 ├─ id
 ├─ user_id → users.id
 └─ palette_id → palettes.id
