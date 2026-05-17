Evrimleþen Sistem - E-Ticaret Sepeti ve Sipariþ Yönetimi

# Neden Bu Konuyu Seçtim?

Listedeki diðer konular teknik olarak geliþtirilmeye açýk olsa da, benim hem kiþisel ilgimin olmasý hem de kariyer hedefim açýsýndan en doðru noktanýn E-Ticaret Sepeti olduðunu düþündüm. Bu projeye sadece bir "ödev" gözüyle bakmaktansa, ilgi alaným olan bir konu üzerinde çalýþmak gerçek bir mühendis bakýþ açýsýyla yaklaþmama imkan saðladý. Bu sebeple projemi D þýkký üzerinden ilerletmeye karar verdim.

# Projenin Amacý ve Geliþim Süreci

Baþlangýçta her þeyin tek bir ETicaretUygulamasi sýnýfý içine yýðýldýðý, indirim ve kargo hesaplamalarýnýn uzun if-else bloklarýyla yapýldýðý, birbirine sýký sýkýya baðlý bir "spagetti kod" yapým vardý. Üç fazlýk bu süreçte, tasarým örüntülerini (Design Patterns) kullanarak kodumu daha modüler, esnek ve geliþime açýk (SOLID prensiplerine uygun) hale getirdim.

# Faz 1: Creational (Yaratýmsal) Tasarým

Factory Method: Ýndirim ve kargo servisi oluþturma iþini ana sýnýftan kopardým ve ServisFabrikasi adýnda tek bir merkeze devrettim. Böylece nesne üretim sürecini kontrol altýna aldým.

# Faz 2: Structural (Yapýsal) Tasarým

Adapter: Dýþarýdan sisteme entegre ettiðim Iyzico ödeme sistemini kendi OdemeArayuzu standartlarýma uydurmak için kullandým.

Decorator: Müþteri sepete "Hediye Paketi" veya "Sigorta" eklemek istediðinde bir sürü alt sýnýf yazmak (sýnýf patlamasý) yerine, temel sepeti çalýþma zamanýnda (runtime) süsledim/sarmaladým.

Proxy: Ödeme adýmýndan hemen önce 15.000 TL'lik bir güvenlik sýnýrý denetimi eklemek için araya bir vekil sýnýf (Proxy) yerleþtirdim.

# Faz 3: Behavioral (Davranýþsal) Tasarým

Strategy: O bitmek bilmeyen if-else indirim kampanyalarý döngüsünden kurtuldum. Artýk yeni bir kampanya eklendiðinde sadece yeni bir strateji sýnýfý yazýyorum (Açýk/Kapalý - OCP prensibini tam olarak saðladým).

Observer: Sipariþ tamamlandýðýnda email, SMS ve kargo firmasýna bildirim gitmesi gerekiyordu. Sistemi sýký sýkýya baðlamak yerine sipariþi "Yayýncý", servisleri "Gözlemci" yaptým. Sipariþ bitince sistem uyarý veriyor, abone olan servisler kendi iþini yapýyor.

# Final Mimari Diyagramým (UML);

```mermaid
classDiagram
    %% Çekirdek Sýnýflar
    class Urun {
        +getTabanFiyat()
        +getKategori()
    }
    class Musteri {
        +getUyelikTipi()
        +getEposta()
    }

    %% FAZ 1: Factory Method
    class Hesaplayici {
        <<abstract>>
        +islem_yap()
    }
    class IndirimHesaplayici {
        +strateji_belirle()
        +islem_yap()
    }
    class KargoHesaplayici {
        +islem_yap()
    }
    class ServisFabrikasi {
        +servis_olustur()
    }
    Hesaplayici <|-- IndirimHesaplayici
    Hesaplayici <|-- KargoHesaplayici
    ServisFabrikasi ..> Hesaplayici : Üretir

    %% FAZ 3: Strategy (Ýndirim Hesaplayýcý Kullanýr)
    class IndirimStratejisi {
        <<interface>>
        +indirim_hesapla()
    }
    class TeknofestIndirimi
    class VizeHaftasiIndirimi
    class HosgeldinIndirimi
    class IndirimYokStratejisi
    IndirimStratejisi <|-- TeknofestIndirimi
    IndirimStratejisi <|-- VizeHaftasiIndirimi
    IndirimStratejisi <|-- HosgeldinIndirimi
    IndirimStratejisi <|-- IndirimYokStratejisi
    IndirimHesaplayici o-- IndirimStratejisi : Strateji Kullanýr

    %% FAZ 2: Decorator
    class SepetBileseni {
        <<interface>>
        +get_toplam()
        +get_detay()
    }
    class StandartSepet
    class SepetDecorator
    class HediyePaketiDecorator
    class SigortaDecorator
    SepetBileseni <|-- StandartSepet
    SepetBileseni <|-- SepetDecorator
    SepetDecorator o-- SepetBileseni : Sarmalar
    SepetDecorator <|-- HediyePaketiDecorator
    SepetDecorator <|-- SigortaDecorator

    %% FAZ 2: Adapter & Proxy
    class OdemeArayuzu {
        <<interface>>
        +odeme_al()
    }
    class IyzicoDisSistem {
        +iyzico_ile_ode()
    }
    class IyzicoAdapter
    class OdemeKontrolProxy
    OdemeArayuzu <|-- IyzicoAdapter
    IyzicoAdapter --> IyzicoDisSistem : Adapte Eder
    OdemeArayuzu <|-- OdemeKontrolProxy
    OdemeKontrolProxy o-- OdemeArayuzu : Kontrol Eder

    %% FAZ 3: Observer
    class SiparisYayincisi {
        +abone_ekle()
        +abonelere_bildir()
    }
    class Gozlemci {
        <<interface>>
        +guncelle()
    }
    class EmailBildirimci
    class SMSBildirimci
    class KargoSirketiBildirimci
    SiparisYayincisi o-- Gozlemci : Aboneleri Tetikler
    Gozlemci <|-- EmailBildirimci
    Gozlemci <|-- SMSBildirimci
    Gozlemci <|-- KargoSirketiBildirimci

    %% Ana Sistem / Context
    class ETicaretUygulamasi {
        +sepeteEkle()
        +siparisiTamamla()
    }
    ETicaretUygulamasi --> ServisFabrikasi : Servis Ýster
    ETicaretUygulamasi --> OdemeArayuzu : Ödeme Yapar
    ETicaretUygulamasi --> SiparisYayincisi : Bildirim Baþlatýr
    ETicaretUygulamasi *-- Urun : Ýçerir
    ETicaretUygulamasi --> Musteri : Sahiplik
```

# Nasýl Çalýþtýrýlýr?

Bilgisayarýnýzda Python 3.x kurulu olduðundan emin olun.

Komut satýrýndan projenin ana dizinine gidin.

python src/spagetti_code.py komutu ile uygulamayý çalýþtýrýp konsoldaki sipariþ adýmlarýný ve örüntü loglarýný inceleyebilirsiniz.