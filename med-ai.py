import datetime
import random
import time

class SaglikAsistani:
    def __init__(self, ad):
        self.ad = ad
        self.saglik_verileri = {
            'kalp_atisi': [],
            'kan_basinci': [],
            'kilo': [],
            'boy': [],
            'egzersiz': [],
            'ilaclar': {}
        }

    def veri_al_ve_kaydet(self):
        print(f"Merhaba {self.ad}! Sağlık verilerinizi girmeye başlayalım.")
        
        # Kalp atışı
        kalp_atisi = self.sayi_al("Kalp atış hızınızı (bpm) girin: ", float)
        self.saglik_verileri['kalp_atisi'].append((datetime.datetime.now(), kalp_atisi))
        self.kalp_atisi_uyari(kalp_atisi)
        
        # Kan basıncı
        while True:
            kan_basinci = input("Kan basıncınızı 'sistolik/diastolik' formatında girin (örnek: 120/80): ").strip()
            if self.kan_basinci_format_kontrol(kan_basinci):
                self.saglik_verileri['kan_basinci'].append((datetime.datetime.now(), kan_basinci))
                self.kan_basinci_uyari(kan_basinci)
                break
            else:
                print("Hatalı format. Lütfen 'sistolik/diastolik' şeklinde tekrar girin.")
        
        # Boy
        boy = self.sayi_al("Boyunuzu cm cinsinden girin: ", float)
        self.saglik_verileri['boy'].append((datetime.datetime.now(), boy))
        
        # Kilo
        kilo = self.sayi_al("Kilonuzu kg cinsinden girin: ", float)
        self.saglik_verileri['kilo'].append((datetime.datetime.now(), kilo))
        self.kilo_ve_bmi_uyari(kilo, boy)
        
        # Egzersiz
        egzersiz = self.sayi_al("Günlük egzersiz sürenizi dakika cinsinden girin: ", int)
        self.saglik_verileri['egzersiz'].append((datetime.datetime.now(), egzersiz))
        self.egzersiz_ve_diyet_onerisi()
        
        # İlaç takibi
        self.ilaclari_yonet()
        
        print("\nTüm sağlık verileriniz başarıyla kaydedildi ve değerlendirildi.")
    
    def sayi_al(self, mesaj, tip):
        while True:
            try:
                deger = tip(input(mesaj).strip())
                return deger
            except ValueError:
                print("Geçersiz giriş, lütfen tekrar deneyin.")
    
    def kan_basinci_format_kontrol(self, deger):
        parcalar = deger.split('/')
        if len(parcalar) != 2:
            return False
        try:
            sys = int(parcalar[0])
            dia = int(parcalar[1])
            return True
        except:
            return False
    
    def kalp_atisi_uyari(self, kalp_atisi):
        if kalp_atisi < 60:
            print("Uyarı: Kalp atış hızınız normalin altında.")
        elif kalp_atisi <= 100:
            print("Kalp atış hızınız normal seviyede.")
        else:
            print("Uyarı: Kalp atış hızınız normalin üzerinde.")
    
    def kan_basinci_uyari(self, kan_basinci):
        sistolik, diastolik = map(int, kan_basinci.split('/'))
        if sistolik < 90 or diastolik < 60:
            print("Uyarı: Kan basıncınız normalin altında.")
        elif sistolik > 140 or diastolik > 90:
            print("Uyarı: Kan basıncınız normalin üzerinde.")
        else:
            print("Kan basıncınız normal seviyede.")
    
    def kilo_ve_bmi_uyari(self, kilo, boy):
        bmi = kilo / ((boy / 100) ** 2)
        print(f"Vücut Kitle İndeksiniz (BMI): {bmi:.2f}")
        if bmi < 18.5:
            print("Uyarı: Vücut kitle endeksiniz normalin altında.")
        elif bmi >= 25:
            print("Uyarı: Vücut kitle endeksiniz normalin üzerinde.")
        else:
            print("Vücut kitle endeksiniz normal seviyede.")
    
    def egzersiz_ve_diyet_onerisi(self):
        kilo_verisi = self.saglik_verileri['kilo'][-1][1] if self.saglik_verileri['kilo'] else None
        boy_verisi = self.saglik_verileri['boy'][-1][1] if self.saglik_verileri['boy'] else None
        
        if kilo_verisi and boy_verisi:
            bmi = kilo_verisi / ((boy_verisi / 100) ** 2)
            if bmi < 18.5:
                print("Daha fazla karbonhidrat ve protein alımı için beslenmenizi gözden geçirin.")
                print("Egzersiz önerisi: Ağırlık antrenmanları ve direnç egzersizleri yaparak kas kütlenizi artırabilirsiniz.")
            elif bmi >= 25:
                print("Daha fazla meyve, sebze ve lifli gıdalar tüketin.")
                print("Egzersiz önerisi: Kardiyo aktiviteleri (koşu, yürüyüş, bisiklet sürme) yaparak kalori yakımını artırabilirsiniz.")
            else:
                print("Sağlıklı beslenmeye devam edin ve düzenli egzersiz yapın.")
        else:
            print("Boy ve kilo verileri eksik olduğu için egzersiz ve diyet önerisi verilemiyor.")
    
    def ilaclari_yonet(self):
        cevap = input("İlaç kullanıyor musunuz? (Evet/Hayır): ").strip().lower()
        if cevap == "evet":
            while True:
                ilac_adi = input("İlaç adını girin (bitirmek için boş bırakın): ").strip()
                if ilac_adi == "":
                    break
                dozaj = input(f"{ilac_adi} ilacının dozajını girin: ").strip()
                while True:
                    try:
                        siklik = int(input(f"{ilac_adi} ilacını kaç saatte bir alıyorsunuz?: ").strip())
                        break
                    except ValueError:
                        print("Lütfen geçerli bir sayı girin.")
                self.saglik_verileri['ilaclar'][ilac_adi] = {'dozaj': dozaj, 'siklik': siklik}
                print(f"{ilac_adi} ilacı eklendi.")
        else:
            print("İlaç ekleme işlemi iptal edildi.")
    
    def ilac_hatirlatici(self):
        print("\nİlaç hatırlatıcı kontrol ediliyor...")
        simdi = datetime.datetime.now()
        for ilac, bilgiler in self.saglik_verileri['ilaclar'].items():
            siklik = bilgiler['siklik']
            dozaj = bilgiler['dozaj']
            # Basit mantık: şimdiki saatin mod siklik sıfırsa ilaç zamanı
            if simdi.hour % siklik == 0 and simdi.minute == 0:
                print(f"İlaç hatırlatma: {ilac} ilacını {dozaj} dozda alma zamanı!")
        print("İlaç hatırlatma kontrolü tamamlandı.\n")
    
    def diyet_plani_olustur(self, hedef_kilo):
        print(f"{self.ad} için hedef kilo: {hedef_kilo} kg. Diyet planı hazırlanıyor...")
        plan = {
            'Kahvaltı': ['Yumurta', 'Tam buğday ekmeği', 'Domates', 'Yeşil çay'],
            'Ara Öğün': ['Yoğurt', 'Meyve', 'Badem'],
            'Öğle Yemeği': ['Izgara tavuk', 'Kahverengi pirinç', 'Brokoli', 'Su'],
            'İkindi Ara Öğün': ['Havuç', 'Meyve dilimleri', 'Bulgur pilavı'],
            'Akşam Yemeği': ['Balık', 'Salata', 'Zeytinyağlı bulgur', 'Su']
        }
        print("Diyet planınız hazır!")
        for oge, yiyecekler in plan.items():
            print(f"{oge}: {', '.join(yiyecekler)}")
        return plan

# Yardımcı fonksiyonlar: Yiyecek sınıfı ve yemek planı oluşturma
class Yiyecek:
    def __init__(self, isim, kalori, protein, karbonhidrat, yag):
        self.isim = isim
        self.kalori = kalori
        self.protein = protein
        self.karbonhidrat = karbonhidrat
        self.yag = yag

def ortalama_bireyin_protein_kaynaklari():
    return [
        Yiyecek("Tavuk göğsü", 120, 20, 0, 3),
        Yiyecek("Yumurta", 70, 6, 0, 5),
        Yiyecek("Somon", 200, 25, 0, 12),
        Yiyecek("Yoğurt", 100, 10, 10, 5),
        Yiyecek("Fasulye", 100, 8, 15, 1)
    ]

def yemek_plani_olustur(hedef):
    hedefler = {
        'protein': ortalama_bireyin_protein_kaynaklari(),
        # istersen buraya karbonhidrat, yağ vs. ekleyebilirsin
    }
    if hedef not in hedefler:
        print("Geçersiz hedef türü.")
        return
    secilen_yiyecekler = random.sample(hedefler[hedef], 3)
    print(f"\n{hedef.capitalize()} hedefi için yemek planı:")
    for yiyecek in secilen_yiyecekler:
        print(f"- {yiyecek.isim}: {yiyecek.kalori} kalori, {yiyecek.protein}g protein, "
              f"{yiyecek.karbonhidrat}g karbonhidrat, {yiyecek.yag}g yağ")

# Ana program akışı
def main():
    isim = input("İsminizi girin: ").strip()
    asistan = SaglikAsistani(isim)
    
    asistan.veri_al_ve_kaydet()
    
    asistan.ilac_hatirlatici()
    
    hedef_kilo = float(input("Hedef kilonuzu kg cinsinden girin: "))
    asistan.diyet_plani_olustur(hedef_kilo)
    
    yemek_hedefi = input("Yemek planı hedefiniz nedir? (protein/karbonhidrat/yag): ").strip().lower()
    if yemek_hedefi in ['protein', 'karbonhidrat', 'yag']:
        yemek_plani_olustur(yemek_hedefi)
    else:
        print("Geçersiz seçim. Program sonlandırılıyor.")

if __name__ == "__main__":
    main()
