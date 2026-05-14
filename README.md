D :  Listedeki diger konular teknik olarak gelistirilmeye acik olsa da,
benim hem kisisel ilgimin olmasi hem de kariyer hedefim acisindan en dogru noktanin E-Ticaret Sepeti oldugunu dusundum.
Odev gozuyle bakmaktansa ilgi alanim olan bir konu uzeridne proje yapmak gercek bir muhendis bakis acisiyle yaklasmama olanak sagladi.
Bu sebeple D þýkkýndan ilerlmeye karar verdim.

```mermaid
classDiagram
    %% Adapter Pattern
    class OdemeArayuzu {
        <<interface>>
        +odeme_al()
    }
    class IyzicoDisSistem {
        +iyzico_ile_ode()
    }
    class IyzicoAdapter {
        +odeme_al()
    }
    class OdemeKontrolProxy {
        +odeme_al()
    }
    
    OdemeArayuzu <|-- IyzicoAdapter
    OdemeArayuzu <|-- OdemeKontrolProxy
    OdemeKontrolProxy o-- OdemeArayuzu : Kontrol Eder
    IyzicoAdapter --> IyzicoDisSistem : Çevirir

    %% Decorator Pattern
    class SepetBileseni {
        <<interface>>
        +get_toplam()
        +get_detay()
    }
    class StandartSepet {
        +get_toplam()
    }
    class SepetDecorator {
        +get_toplam()
    }
    class HediyePaketiDecorator {
        +get_toplam()
    }
    class SigortaDecorator {
        +get_toplam()
    }
    
    SepetBileseni <|-- StandartSepet
    SepetBileseni <|-- SepetDecorator
    SepetDecorator o-- SepetBileseni : Sarmalar
    SepetDecorator <|-- HediyePaketiDecorator
    SepetDecorator <|-- SigortaDecorator