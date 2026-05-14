D :  Listedeki diger konular teknik olarak gelistirilmeye acik olsa da,
benim hem kisisel ilgimin olmasi hem de kariyer hedefim acisindan en dogru noktanin E-Ticaret Sepeti oldugunu dusundum.
Odev gozuyle bakmaktansa ilgi alanim olan bir konu uzeridne proje yapmak gercek bir muhendis bakis acisiyle yaklasmama olanak sagladi.
Bu sebeple D þýkkýndan ilerlmeye karar verdim.

```mermaid
classDiagram
    class Hesaplayici {
        <<abstract>>
        +islem_yap()
    }
    class IndirimHesaplayici {
        +islem_yap()
    }
    class KargoHesaplayici {
        +islem_yap()
    }
    class ServisFabrikasi {
        +servis_olustur()
    }
    class ETicaretUygulamasi {
        +siparisiTamamla()
    }

    Hesaplayici <|-- IndirimHesaplayici
    Hesaplayici <|-- KargoHesaplayici
    ServisFabrikasi ..> IndirimHesaplayici
    ServisFabrikasi ..> KargoHesaplayici
    ETicaretUygulamasi --> ServisFabrikasi