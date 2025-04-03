import csv
from google_play_scraper import reviews_all

# İncelemek istediğiniz uygulama paket adlarını liste halinde girin, paylaşa bastığınızda şu linkteki com.tft.android kısmı https://play.google.com/store/apps/details?id=com.tft.android&pcampaignid=web_share
package_names = [
    "com.app",
    "com.appname",
    "co.appname"
]

# CSV dosyası adı
csv_filename = "multiple_reviews.csv"

# CSV dosyasını oluştur ve başlık satırını yaz
with open(csv_filename, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Uygulama", "Yorum", "Puan", "Tarih", "Yazar", "Dil", "Ülke"])

    # Her uygulama için yorumları çek
    for package_name in package_names:
        print(f"{package_name} için yorumlar çekiliyor...")

        # Uygulamaya ait tüm yorumları çek (Tüm diller ve ülkeler)
        all_reviews = reviews_all(package_name)

        # 1, 2, 3 yıldızlı yorumları filtrele, siz tüm yorumları alabilirsiniz.
        filtered_reviews = [review for review in all_reviews if review["score"] in [1, 2, 3]]

        # CSV dosyasına ekle
        for review in filtered_reviews:
            writer.writerow([
                package_name,
                review["content"],
                review["score"],
                review["at"],
                review["userName"],
                review.get("reviewCreatedVersion", "Bilinmiyor"),  # Yorumu hangi sürümde yazdığı
                review.get("userCountry", "Bilinmiyor")  # Kullanıcının ülkesi (varsa)
            ])

        print(f"{package_name}: {len(filtered_reviews)} yorum kaydedildi.")

print(f"Toplam yorumlar kaydedildi: {csv_filename}")