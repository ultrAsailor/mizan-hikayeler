# mizan-hikayeler

Mizan / eda uygulamasının "Dini Hikayeler" bölümü için uzaktan eklenebilen hikaye deposu.
Buraya eklenen hikayeler, uygulama güncellemesi olmadan uygulamada görünür.

## Yeni hikaye ekleme

1. `stories/<slug>.json` dosyasını oluştur (`slug` küçük harf, tire ile; dosya adıyla **aynı** olmalı):

```json
{
  "slug": "ornek-hikaye",
  "title": "Örnek Hikaye",
  "category": "sahabe",
  "body": "Birinci paragraf.\n\nİkinci paragraf.\n\nSon cümle: tek bir ders.",
  "attribution": "Felak içerik ekibi — özgün anlatım",
  "references": ["Buhârî, Bed'ü'l-vahy, 1"]
}
```

   - `category`: `kuran-kissalari`, `siyer`, `sahabe` veya `ahlak`
   - `body`: düz metin, paragraflar `\n\n` ile ayrılır
   - `references`: ayet/hadis/siyer dayanakları (string listesi)

2. Kapağı `covers/<slug>.webp` olarak ekle (16:9, önerilen 800x450, ~50 KB; `.jpg`/`.png` de kabul).
3. `main` dalına push et. GitHub Action `index.json`'u otomatik günceller; uygulama bir sonraki açılışta yeni hikayeyi alır.

`index.json`'u elle düzenleme. Doğrulama hatası olursa Action başarısız olur ve mesajda hangi dosyanın sorunlu olduğu yazar.

Mevcut bir `slug` ile hikaye eklenirse uygulamadaki gömülü hikayenin metnini ezer (düzeltme için kullanılabilir).
