# Faz 1: Creational (Yaratýmsal) Örüntüler 

Factory Method (Fabrika Yöntemi)

Nerede Uygulandý?
    ETicaretUygulamasi sýnýfýnýn içinde kullanýlan IndirimHesaplayici ve KargoHesaplayici nesnelerini oluþtururken uyguladým.

Neden Uygulandý?
    ETicaretUygulamasi sýnýfýnýn sürekli nesne üretme iþiyle uðraþmasýný istemedim. Bu yüzden nesne oluþturma iþlemlerini ayrý bir fabrikaya taþýdým. Böylece sýnýflar birbirine daha az baðlý oldu ve kod daha düzenli hale geldi.

Ne Kazandýrdý?
    Sisteme yeni bir hesaplayýcý eklemek istediðimde ana kodun içini deðiþtirmem gerekmiyor. Mesela ileride VergiHesaplayici eklersem sadece fabrikaya ekleme yapmam yeterli olacak. Bu da kodu geliþtirmeyi daha kolay hale getirdi.


# Faz 2: Structural (Yapýsal) Örüntüler 

1. Adapter (Adaptör) Deseni
Nerede kullandým?
    Dýþarýdan gelen IyzicoDisSistem API’sini kendi sistemimde kullandýðým OdemeArayuzu yapýsýna uyarlarken kullandým (IyzicoAdapter).
Neden kullandým?
    Çünkü dýþarýdaki bir API’nin yapýsýný deðiþtiremiyorum. Ben de sistemi ona uydurmak yerine araya bir çevirici koyarak iki sistemi birbirine baðladým.
Neden diðer seçenek deðil?
    Facade’i düþünmedim çünkü burada amaç karmaþýk bir sistemi gizlemek deðil, uyumsuz iki yapýyý konuþturmak.


2. Decorator (Dekoratör) Deseni
Nerede kullandým?
    Sepete eklenen ekstra hizmetlerde kullandým. Mesela hediye paketi ve kargo sigortasý gibi ek ücretleri dinamik olarak eklemek için kullandým.
Neden kullandým?
    Kalýtým yapsaydým her kombinasyon için ayrý sýnýf açmam gerekecekti ve bu kodu çok þiþirirdi. Decorator ile mevcut sepeti bozmadan üstüne özellik ekleyebildim.


3. Proxy (Vekil) Deseni
Nerede kullandým?
    Ödeme iþleminden önce kontrol yapan OdemeKontrolProxy yapýsýnda kullandým.
Neden kullandým?
    Gerçek ödeme sistemine dokunmadan araya bir kontrol katmaný koymak istedim. Yani ödeme yapýlmadan önce güvenlik kontrolü gibi bir filtre eklemiþ oldum.


# Faz 3: Behavioral (Davranýþsal) Örüntüler

Bu fazda sistemin çalýþma anýndaki davranýþlarý esnekleþtirdim ve OCP (Açýk/Kapalý Prensibi) kuralýný saðladým.

1. Strategy (Strateji) Deseni
Nerede Kullandým?
    Ýndirim hesaplama mantýðýnda kullandým. (`IndirimStratejisi`, `TeknofestIndirimi` vb.).
Neden Seçtim?
    Faz 1'deki `IndirimHesaplayici` sýnýfý içinde büyümeye müsait çirkin bir `if-else` yýðýný vardý. Strategy sayesinde bu yýðýný sildim. Artýk yeni bir kampanya eklendiðinde mevcut kodlara hiç dokunmadan sadece yeni bir strateji sýnýfý yazabiliyorum (Tam OCP uyumu).

2. Observer (Gözlemci) Deseni
Nerede Kullandým? 
    Sipariþ tamamlandýðýnda müþteriye ve kargo firmasýna giden bildirim altyapýsýnda kullandým. (`SiparisYayincisi`, `Gozlemci`).
Neden Seçtim?
    Eskiden sipariþ tamamlandýðýnda ana uygulama zorla email atýyordu. Þimdi ana uygulama (Yayýncý) sadece "Sipariþ Bitti" diye baðýrýyor, buna abone olan SMS, Email ve Kargo servisleri (Gözlemciler) kendi iþlerini yapýyor. Sistemi birbirine sýký sýkýya baðlamaktan kurtardýk.