Faz 1: Creational (Yaratýmsal) Örüntüler 

Factory Method (Fabrika Yöntemi)

Nerede Uygulandý?
ETicaretUygulamasi sýnýfýnýn içinde kullanýlan IndirimHesaplayici ve KargoHesaplayici nesnelerini oluþtururken uyguladým.

Neden Uygulandý?
ETicaretUygulamasi sýnýfýnýn sürekli nesne üretme iþiyle uðraþmasýný istemedim. Bu yüzden nesne oluþturma iþlemlerini ayrý bir fabrikaya taþýdým. Böylece sýnýflar birbirine daha az baðlý oldu ve kod daha düzenli hale geldi.

Ne Kazandýrdý?
Sisteme yeni bir hesaplayýcý eklemek istediðimde ana kodun içini deðiþtirmem gerekmiyor. Mesela ileride VergiHesaplayici eklersem sadece fabrikaya ekleme yapmam yeterli olacak. Bu da kodu geliþtirmeyi daha kolay hale getirdi.

