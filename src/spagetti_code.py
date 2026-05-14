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
    def islem_yap(self, **kwargs): pass

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

class OdemeArayuzu(ABC):
    @abstractmethod
    def odeme_al(self, miktar, musteri): pass

class IyzicoDisSistem:
    def iyzico_ile_ode(self, email, miktar):
        print(f"[IYZICO API] {email} hesabindan {miktar:.2f} TL basariyla cekildi.")

class IyzicoAdapter(OdemeArayuzu):
    def __init__(self):
        self.iyzico = IyzicoDisSistem()
    def odeme_al(self, miktar, musteri):
        self.iyzico.iyzico_ile_ode(musteri.getEposta(), miktar)

class OdemeKontrolProxy(OdemeArayuzu):
    def __init__(self, gercek_odeme: OdemeArayuzu):
        self.gercek_odeme = gercek_odeme
    def odeme_al(self, miktar, musteri):
        if miktar > 15000:
            print("[PROXY UYARISI] Guvenlik siniri asildi! Manuel onay gerekiyor.")
        else:
            print("[PROXY] Odeme guvenlik kontrolunden gecti.")
            self.gercek_odeme.odeme_al(miktar, musteri)

class SepetBileseni(ABC):
    @abstractmethod
    def get_toplam(self): pass
    @abstractmethod
    def get_detay(self): pass

class StandartSepet(SepetBileseni):
    def __init__(self, tutar):
        self.tutar = tutar
    def get_toplam(self): return self.tutar
    def get_detay(self): return "Standart Sepet Tutari"

class SepetDecorator(SepetBileseni):
    def __init__(self, bilesen: SepetBileseni):
        self.bilesen = bilesen
    def get_toplam(self): return self.bilesen.get_toplam()
    def get_detay(self): return self.bilesen.get_detay()

class HediyePaketiDecorator(SepetDecorator):
    def get_toplam(self): return self.bilesen.get_toplam() + 50.0
    def get_detay(self): return self.bilesen.get_detay() + " + Hediye Paketi (+50 TL)"

class SigortaDecorator(SepetDecorator):
    def get_toplam(self): return self.bilesen.get_toplam() + 100.0
    def get_detay(self): return self.bilesen.get_detay() + " + Kargo Sigortasi (+100 TL)"

class BildirimServisi:
    def bildirimGonder(self, musteri):
        print(f"[BILDIRIM] Onay e-postasi gonderildi: {musteri.getEposta()}")

class ETicaretUygulamasi:
    def __init__(self, musteri, kargoSehri):
        self.sepetUrunleri = []
        self.musteri = musteri
        self.kargoSehri = kargoSehri
        self.indirimKodu = ""
        self.indirim = ServisFabrikasi.servis_olustur("indirim")
        self.kargo = ServisFabrikasi.servis_olustur("kargo")
        self.bildirim = BildirimServisi()
        
        gercek_odeme = IyzicoAdapter()
        self.odeme = OdemeKontrolProxy(gercek_odeme)
        
        self.hediye_paketi = False
        self.sigorta = False

    def sepeteEkle(self, urun): self.sepetUrunleri.append(urun)
    def indirimKoduUygula(self, kod): self.indirimKodu = kod
    def hediye_paketi_ekle(self): self.hediye_paketi = True
    def sigorta_ekle(self): self.sigorta = True

    def siparisiTamamla(self):
        print("\n--- SIPARIS ISLENIYOR ---")
        indirimli = self.indirim.islem_yap(sepetUrunleri=self.sepetUrunleri, indirimKodu=self.indirimKodu, aktifMusteri=self.musteri)
        kargo = self.kargo.islem_yap(sepetUrunleri=self.sepetUrunleri, kargoSehri=self.kargoSehri, aktifMusteri=self.musteri, indirimliFiyat=indirimli)
        
        ilk_tutar = (indirimli + kargo) * 1.20
        
        nihai_sepet = StandartSepet(ilk_tutar)
        if self.hediye_paketi:
            nihai_sepet = HediyePaketiDecorator(nihai_sepet)
        if self.sigorta:
            nihai_sepet = SigortaDecorator(nihai_sepet)
            
        sonTutar = nihai_sepet.get_toplam()
        print(f"Siparis Detayi: {nihai_sepet.get_detay()}")
        
        self.odeme.odeme_al(sonTutar, self.musteri)
        self.bildirim.bildirimGonder(self.musteri)
        print("--- SIPARIS TAMAMLANDI ---\n")

if __name__ == "__main__":
    m = Musteri("Ali Yilmaz", "ali@mail.com", "PLATIN", 1500)
    s = ETicaretUygulamasi(m, "ISTANBUL")

    s.sepeteEkle(Urun("U01", "Arduino", 450, "ELEKTRONIK", 0.2, True))
    s.sepeteEkle(Urun("U02", "Motor", 850, "ELEKTRONIK", 1.5, False))

    s.indirimKoduUygula("TEKNOFEST_INDIRIMI")
    s.hediye_paketi_ekle()
    s.sigorta_ekle()
    
    s.siparisiTamamla()
    
    input("Cikmak icin Enter'a basin...")