import requests
import json

# Çekmek istediğin uygulamaların App Store ID'lerini liste olarak ekle
app_ids = [
    "1095698831"
]

# JSON dosyası adı
json_filename = "apple_reviews_filtered.json"

# Tüm uygulamalar için yorumları saklamak üzere bir liste oluştur
all_reviews = []

# Her uygulama için yorumları çek
for app_id in app_ids:
    print(f"{app_id} için yorumlar çekiliyor...")

    # App Store yorumlarını çekme URL'si
    url = f"https://itunes.apple.com/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"

    # API'ye isteği gönder
    response = requests.get(url)

    # JSON verisini al
    data = response.json()

    # Yorumları al (Bazı uygulamalarda yorum olmayabilir, kontrol ediyoruz)
    reviews = data.get("feed", {}).get("entry", [])

    # 1, 2, 3 yıldızlı yorumları filtrele
    filtered_reviews = [
        {
            "app_id": app_id,
            "content": review.get("content", {}).get("label", "Yorum yok"),
            "rating": review.get("im:rating", {}).get("label", "Bilinmiyor"),
            "date": review.get("updated", {}).get("label", "Tarih yok"),
            "author": review.get("author", {}).get("name", {}).get("label", "Bilinmiyor"),
            "version": review.get("im:version", {}).get("label", "Bilinmiyor")
        }
        for review in reviews if review.get("im:rating", {}).get("label") in ["1", "2", "3"]
    ]

    # Verileri genel listeye ekle
    all_reviews.extend(filtered_reviews)

    print(f"{app_id}: {len(filtered_reviews)} yorum kaydedildi.")

# JSON dosyasına kaydet
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(all_reviews, json_file, ensure_ascii=False, indent=4)

print(f"Toplam {len(all_reviews)} yorum kaydedildi: {json_filename}")
