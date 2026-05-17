
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
    def __init__(self, isim, eposta, telefon, uyelikTipi, sadakatPuani):
        self.isim = isim
        self.eposta = eposta
        self.telefon = telefon
        self.uyelikTipi = uyelikTipi
        self.sadakatPuani = sadakatPuani
    def getUyelikTipi(self): return self.uyelikTipi
    def getSadakatPuani(self): return self.sadakatPuani
    def getEposta(self): return self.eposta
    def getIsim(self): return self.isim
    def getTelefon(self): return self.telefon


class IndirimStratejisi(ABC):
    @abstractmethod
    def indirim_hesapla(self, sepetUrunleri, araToplam): pass

class VizeHaftasiIndirimi(IndirimStratejisi):
    def indirim_hesapla(self, sepetUrunleri, araToplam):
        return araToplam * 0.15

class HosgeldinIndirimi(IndirimStratejisi):
    def indirim_hesapla(self, sepetUrunleri, araToplam):
        return 50.0

class TeknofestIndirimi(IndirimStratejisi):
    def indirim_hesapla(self, sepetUrunleri, araToplam):
        return sum(u.getTabanFiyat() for u in sepetUrunleri if u.getKategori() == "ELEKTRONIK") * 0.20

class IndirimYokStratejisi(IndirimStratejisi):
    def indirim_hesapla(self, sepetUrunleri, araToplam):
        return 0.0

class Hesaplayici(ABC):
    @abstractmethod
    def islem_yap(self, **kwargs): pass

class IndirimHesaplayici(Hesaplayici):
    def __init__(self):
        self.strateji = IndirimYokStratejisi()
    
    def strateji_belirle(self, strateji: IndirimStratejisi):
        self.strateji = strateji

    def islem_yap(self, sepetUrunleri, aktifMusteri):
        araToplam = sum(u.getTabanFiyat() for u in sepetUrunleri)
        indirimMiktari = self.strateji.indirim_hesapla(sepetUrunleri, araToplam)
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
    def __init__(self): self.iyzico = IyzicoDisSistem()
    def odeme_al(self, miktar, musteri): self.iyzico.iyzico_ile_ode(musteri.getEposta(), miktar)


class OdemeKontrolProxy(OdemeArayuzu):
    def __init__(self, gercek_odeme: OdemeArayuzu): self.gercek_odeme = gercek_odeme
    def odeme_al(self, miktar, musteri):
        if miktar > 15000: print("[PROXY UYARISI] Guvenlik siniri asildi!")
        else:
            print("[PROXY] Odeme guvenlik kontrolunden gecti.")
            self.gercek_odeme.odeme_al(miktar, musteri)


class SepetBileseni(ABC):
    @abstractmethod
    def get_toplam(self): pass
    @abstractmethod
    def get_detay(self): pass


class StandartSepet(SepetBileseni):
    def __init__(self, tutar): self.tutar = tutar
    def get_toplam(self): return self.tutar
    def get_detay(self): return "Standart Sepet Tutari"


class SepetDecorator(SepetBileseni):
    def __init__(self, bilesen: SepetBileseni): self.bilesen = bilesen
    def get_toplam(self): return self.bilesen.get_toplam()
    def get_detay(self): return self.bilesen.get_detay()


class HediyePaketiDecorator(SepetDecorator):
    def get_toplam(self): return self.bilesen.get_toplam() + 50.0
    def get_detay(self): return self.bilesen.get_detay() + " + Hediye Paketi (+50 TL)"



class Gozlemci(ABC):
    @abstractmethod
    def guncelle(self, musteri, siparis_detayi): pass


class EmailBildirimci(Gozlemci):
    def guncelle(self, musteri, siparis_detayi):
        print(f"[EMAIL] {musteri.getEposta()} adresine e-posta gonderildi. Detay: {siparis_detayi}")


class SMSBildirimci(Gozlemci):
    def guncelle(self, musteri, siparis_detayi):
        print(f"[SMS] {musteri.getTelefon()} numarasina SMS gonderildi. Durum: Hazirlaniyor.")


class KargoSirketiBildirimci(Gozlemci):
    def guncelle(self, musteri, siparis_detayi):
        print(f"[KARGO] Sistem kargo firmasina bildirildi. Alici: {musteri.getIsim()}")



class SiparisYayincisi:
    def __init__(self):
        self.gozlemciler = []
    
    def abone_ekle(self, gozlemci: Gozlemci):
        self.gozlemciler.append(gozlemci)
        
    def abonelere_bildir(self, musteri, siparis_detayi):
        print("\n--- GOZLEMCILERE (OBSERVERS) BILDIRIM GONDERILIYOR ---")
        for gozlemci in self.gozlemciler:
            gozlemci.guncelle(musteri, siparis_detayi)



class ETicaretUygulamasi:
    def __init__(self, musteri, kargoSehri):
        self.sepetUrunleri = []
        self.musteri = musteri
        self.kargoSehri = kargoSehri
        
        self.indirim = ServisFabrikasi.servis_olustur("indirim")
        self.kargo = ServisFabrikasi.servis_olustur("kargo")
        
        gercek_odeme = IyzicoAdapter()
        self.odeme = OdemeKontrolProxy(gercek_odeme)
        self.hediye_paketi = False
        

        self.yayinci = SiparisYayincisi()
        self.yayinci.abone_ekle(EmailBildirimci())
        self.yayinci.abone_ekle(SMSBildirimci())
        self.yayinci.abone_ekle(KargoSirketiBildirimci())

    def sepeteEkle(self, urun): self.sepetUrunleri.append(urun)
    def hediye_paketi_ekle(self): self.hediye_paketi = True
    

    def strateji_belirle(self, strateji: IndirimStratejisi):
        self.indirim.strateji_belirle(strateji)

    def siparisiTamamla(self):
        print("\n--- SIPARIS ISLENIYOR ---")
        indirimli = self.indirim.islem_yap(sepetUrunleri=self.sepetUrunleri, aktifMusteri=self.musteri)
        kargo = self.kargo.islem_yap(sepetUrunleri=self.sepetUrunleri, kargoSehri=self.kargoSehri, aktifMusteri=self.musteri, indirimliFiyat=indirimli)
        
        ilk_tutar = (indirimli + kargo) * 1.20
        
        nihai_sepet = StandartSepet(ilk_tutar)
        if self.hediye_paketi:
            nihai_sepet = HediyePaketiDecorator(nihai_sepet)
            
        sonTutar = nihai_sepet.get_toplam()
        print(f"Siparis Detayi: {nihai_sepet.get_detay()}")
        
        self.odeme.odeme_al(sonTutar, self.musteri)
        
    
        self.yayinci.abonelere_bildir(self.musteri, nihai_sepet.get_detay())
        print("--- SIPARIS TAMAMLANDI ---\n")

if __name__ == "__main__":
    m = Musteri("Ali Yilmaz", "ali@mail.com", "05551234567", "PLATIN", 1500)
    s = ETicaretUygulamasi(m, "ISTANBUL")

    s.sepeteEkle(Urun("U01", "Arduino", 450, "ELEKTRONIK", 0.2, True))
    s.sepeteEkle(Urun("U02", "Motor", 850, "ELEKTRONIK", 1.5, False))


    s.strateji_belirle(TeknofestIndirimi())
    s.hediye_paketi_ekle()
    
    s.siparisiTamamla()
    
    input("Cikmak icin Enter'a basin...")