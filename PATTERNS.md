Faz 1: Creational (Yaratýmsal) Örüntüler 

Factory Method (Fabrika Yöntemi)

Nerede Uygulandý?
ETicaretUygulamasi sýnýfýnýn içinde kullanýlan IndirimHesaplayici ve KargoHesaplayici nesnelerini oluþtururken uyguladým.

Neden Uygulandý?
ETicaretUygulamasi sýnýfýnýn sürekli nesne üretme iþiyle uðraþmasýný istemedim. Bu yüzden nesne oluþturma iþlemlerini ayrý bir fabrikaya taþýdým. Böylece sýnýflar birbirine daha az baðlý oldu ve kod daha düzenli hale geldi.

Ne Kazandýrdý?
Sisteme yeni bir hesaplayýcý eklemek istediðimde ana kodun içini deðiþtirmem gerekmiyor. Mesela ileride VergiHesaplayici eklersem sadece fabrikaya ekleme yapmam yeterli olacak. Bu da kodu geliþtirmeyi daha kolay hale getirdi.


Faz 2: Structural (Yapýsal) Örüntüler 

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