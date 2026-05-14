class Urun:
    def __init__(self, urunId, ad, tabanFiyat, kategori, agirlik, kirilganMi):
        self.urunId = urunId
        self.ad = ad
        self.tabanFiyat = tabanFiyat
        self.kategori = kategori
        self.agirlik = agirlik
        self.kirilganMi = kirilganMi

    def getTabanFiyat(self):
        return self.tabanFiyat

    def getKategori(self):
        return self.kategori

    def getAgirlik(self):
        return self.agirlik

    def kirilganMiKontrol(self):
        return self.kirilganMi

    def getAd(self):
        return self.ad

    def getUrunId(self):
        return self.urunId


class Musteri:
    def __init__(self, isim, eposta, uyelikTipi, sadakatPuani):
        self.isim = isim
        self.eposta = eposta
        self.uyelikTipi = uyelikTipi
        self.sadakatPuani = sadakatPuani

    def getUyelikTipi(self):
        return self.uyelikTipi

    def getSadakatPuani(self):
        return self.sadakatPuani

    def getEposta(self):
        return self.eposta

    def getIsim(self):
        return self.isim


class ETicaretUygulamasi:
    def __init__(self, aktifMusteri, kargoSehri):
        self.sepetUrunleri = []
        self.aktifMusteri = aktifMusteri
        self.kargoSehri = kargoSehri
        self.indirimKodu = ""
        self.odemeYontemi = "KREDI_KARTI"

    def sepeteEkle(self, urun):
        self.sepetUrunleri.append(urun)

    def indirimKoduUygula(self, kod):
        self.indirimKodu = kod

    def odemeYontemiSec(self, yontem):
        self.odemeYontemi = yontem

    def siparisiTamamla(self):
        araToplam = 0
        toplamAgirlik = 0
        kirilganVarMi = False

        for urun in self.sepetUrunleri:
            araToplam += urun.getTabanFiyat()
            toplamAgirlik += urun.getAgirlik()

            if urun.kirilganMiKontrol():
                kirilganVarMi = True

        indirimMiktari = 0

        if self.indirimKodu == "VIZEHAFTASI":
            indirimMiktari = araToplam * 0.15

        elif self.indirimKodu == "HOSGELDIN50":
            indirimMiktari = 50.0

        elif self.indirimKodu == "TEKNOFEST_INDIRIMI":
            teknolojiToplami = 0

            for urun in self.sepetUrunleri:
                if urun.getKategori() == "ELEKTRONIK":
                    teknolojiToplami += urun.getTabanFiyat()

            indirimMiktari = teknolojiToplami * 0.20

        indirimliFiyat = araToplam - indirimMiktari

        if self.aktifMusteri.getUyelikTipi() == "ALTIN":
            indirimliFiyat = indirimliFiyat * 0.90

        elif self.aktifMusteri.getUyelikTipi() == "PLATIN":
            indirimliFiyat = indirimliFiyat * 0.80

        if self.aktifMusteri.getSadakatPuani() > 1000:
            indirimliFiyat = indirimliFiyat - 100

        kargoUcreti = 0

        if self.kargoSehri == "ISTANBUL" or self.kargoSehri == "ANKARA":
            kargoUcreti = toplamAgirlik * 2.5

        else:
            kargoUcreti = toplamAgirlik * 5.0

        if kirilganVarMi:
            kargoUcreti += 50.0

        if self.aktifMusteri.getUyelikTipi() == "PLATIN" and indirimliFiyat > 500:
            kargoUcreti = 0

        vergiMiktari = indirimliFiyat * 0.20
        sonTutar = indirimliFiyat + kargoUcreti + vergiMiktari

        print("Siparis isleniyor... Musteri:", self.aktifMusteri.getIsim())

        if self.odemeYontemi == "KREDI_KARTI":
            print("Banka API'sine baglaniliyor...")
            print("Karttan cekilecek tutar:", sonTutar)

        elif self.odemeYontemi == "PAYPAL":
            print("PayPal sayfasina yonlendiriliyor...")
            print("Cekilecek tutar:", sonTutar)

        elif self.odemeYontemi == "KRIPTO":
            print("Blockchain onayi bekleniyor...")

        print("Siparis veritabani tablolarina insert ediliyor...")

        print("Onay e-postasi gonderiliyor:", self.aktifMusteri.getEposta())

        if self.aktifMusteri.getUyelikTipi() == "PLATIN":
            print("Platin uyeye ekstra SMS atiliyor...")

        print("Islem tamam. Odenecek toplam tutar:", sonTutar)


musteri = Musteri(
    "Ali Yilmaz",
    "ali.yilmaz@ogrenci.edu.tr",
    "PLATIN",
    1500
)

sepet = ETicaretUygulamasi(musteri, "ISTANBUL")

urun1 = Urun(
    "U01",
    "Arduino Mega 2560",
    450.0,
    "ELEKTRONIK",
    0.2,
    True
)

urun2 = Urun(
    "U02",
    "NEMA 23 Motor",
    850.0,
    "ELEKTRONIK",
    1.5,
    False
)

urun3 = Urun(
    "U03",
    "Lehim Teli",
    120.0,
    "HIRDAVAT",
    0.1,
    False
)

sepet.sepeteEkle(urun1)
sepet.sepeteEkle(urun2)
sepet.sepeteEkle(urun3)

sepet.indirimKoduUygula("TEKNOFEST_INDIRIMI")
sepet.odemeYontemiSec("KREDI_KARTI")

sepet.siparisiTamamla()