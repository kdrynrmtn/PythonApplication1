from abc import ABC, abstractmethod

class Urun:
    def __init__(self, urunId, ad, tabanFiyat, kategori, agirlik, kirilganMi):
        self.urunId = urunId
        self.ad = ad
        self.tabanFiyat = tabanFiyat
        self.kategori = kategori
        self.agirlik = agirlik
        self.kirilganMi = kirilganMi

    def getTabanFiyat(self): return self.tabanFiyat
    def getKategori(self): return self.kategori
    def getAgirlik(self): return self.agirlik
    def kirilganMiKontrol(self): return self.kirilganMi
    def getAd(self): return self.ad

class Musteri:
    def __init__(self, isim, eposta, uyelikTipi, sadakatPuani):
        self.isim = isim
        self.eposta = eposta
        self.uyelikTipi = uyelikTipi
        self.sadakatPuani = sadakatPuani

    def getUyelikTipi(self): return self.uyelikTipi
    def getSadakatPuani(self): return self.sadakatPuani
    def getEposta(self): return self.eposta
    def getIsim(self): return self.isim


class Hesaplayici(ABC):
    @abstractmethod
    def islem_yap(self, **kwargs):
        pass

class IndirimHesaplayici(Hesaplayici):
    def islem_yap(self, sepetUrunleri, indirimKodu, aktifMusteri):
        araToplam = sum(u.getTabanFiyat() for u in sepetUrunleri)
        indirimMiktari = 0
        if indirimKodu == "VIZEHAFTASI": indirimMiktari = araToplam * 0.15
        elif indirimKodu == "HOSGELDIN50": indirimMiktari = 50.0
        elif indirimKodu == "TEKNOFEST_INDIRIMI":
            indirimMiktari = sum(u.getTabanFiyat() for u in sepetUrunleri if u.getKategori() == "ELEKTRONIK") * 0.20
        
        indirimliFiyat = araToplam - indirimMiktari
        if aktifMusteri.getUyelikTipi() == "ALTIN": indirimliFiyat *= 0.90
        elif aktifMusteri.getUyelikTipi() == "PLATIN": indirimliFiyat *= 0.80
        if aktifMusteri.getSadakatPuani() > 1000: indirimliFiyat -= 100
        return indirimliFiyat

class KargoHesaplayici(Hesaplayici):
    def islem_yap(self, sepetUrunleri, kargoSehri, aktifMusteri, indirimliFiyat):
        toplamAgirlik = sum(u.getAgirlik() for u in sepetUrunleri)
        kargoUcreti = toplamAgirlik * (2.5 if kargoSehri in ["ISTANBUL", "ANKARA"] else 5.0)
        if any(u.kirilganMiKontrol() for u in sepetUrunleri): kargoUcreti += 50.0
        if aktifMusteri.getUyelikTipi() == "PLATIN" and indirimliFiyat > 500: kargoUcreti = 0
        return kargoUcreti


class ServisFabrikasi:
    @staticmethod
    def servis_olustur(servis_tipi):
        if servis_tipi == "indirim": return IndirimHesaplayici()
        elif servis_tipi == "kargo": return KargoHesaplayici()
        return None



class OdemeIslemi:
    def odemeYap(self, odemeYontemi, sonTutar):
        print(f"Odeme Yontemi: {odemeYontemi}, Tutar: {sonTutar}")

class BildirimServisi:
    def bildirimGonder(self, aktifMusteri):
        print(f"E-posta gonderildi: {aktifMusteri.getEposta()}")

class ETicaretUygulamasi:
    def __init__(self, aktifMusteri, kargoSehri):
        self.sepetUrunleri = []
        self.aktifMusteri = aktifMusteri
        self.kargoSehri = kargoSehri
        self.indirimKodu = ""
        self.odemeYontemi = "KREDI_KARTI"
  
        self.indirimServisi = ServisFabrikasi.servis_olustur("indirim")
        self.kargoServisi = ServisFabrikasi.servis_olustur("kargo")
        self.odemeServisi = OdemeIslemi()
        self.bildirimServisi = BildirimServisi()

    def sepeteEkle(self, urun): self.sepetUrunleri.append(urun)
    def indirimKoduUygula(self, kod): self.indirimKodu = kod
    def odemeYontemiSec(self, yontem): self.odemeYontemi = yontem

    def siparisiTamamla(self):
        indirimliFiyat = self.indirimServisi.islem_yap(self.sepetUrunleri, self.indirimKodu, self.aktifMusteri)
        kargoUcreti = self.kargoServisi.islem_yap(self.sepetUrunleri, self.kargoSehri, self.aktifMusteri, indirimliFiyat)
        sonTutar = (indirimliFiyat + kargoUcreti) * 1.20 # %20 Vergi
        self.odemeServisi.odemeYap(self.odemeYontemi, sonTutar)
        self.bildirimServisi.bildirimGonder(self.aktifMusteri)
        print(f"Islem tamam. Toplam: {sonTutar}")


musteri = Musteri("Ali Yilmaz", "ali@mail.com", "PLATIN", 1500)
sepet = ETicaretUygulamasi(musteri, "ISTANBUL")
sepet.sepeteEkle(Urun("U01", "Arduino", 450.0, "ELEKTRONIK", 0.2, True))
sepet.indirimKoduUygula("TEKNOFEST_INDIRIMI")
sepet.siparisiTamamla()