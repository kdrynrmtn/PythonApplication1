# Faz 3 AI Kullaným Raporu :

Görüþme Süresi: Yaklaþýk 45 Dakika

# Ne Tartýþtýk ve Nasýl Ýlerledi?
Bu fazda AI ile "Pair Programming" yaparak sistemi Açýk/Kapalý Prensibine (OCP) uygun hale getirdik. Ýndirim hesaplamalarýndaki karmaþýk if-else yapýsýný çözmek için Strategy, sipariþ sonrasý bildirimleri yönetmek için ise Observer desenini koda entegre ettik.
Sonrasýnda profesyonel bir CI/CD süreci için .github/workflows/ci.yml dosyasýný oluþturarak GitHub Actions pipeline'ýný kurduk. Tüm adýmlarý küçük parçalara bölerek ilerledik ve tasarýmlar üzerine fikir alýþveriþi yaptýk.

# AI olmadan bu faz ne kadar sürerdi?
AI olmadan bu faz planladýðýmdan en az üç kat daha fazla sürerdi. Hangi tasarým desenini nerede uygulayacaðýmý seçmek ve tüm bu geçiþi tek baþýma tasarlamak ekstra bir planlama zamaný gerektirecekti. Bunun dýþýnda, tasarladýðým koddaki mantýksal veya söz dizimsel hatalarý tek baþýma çözerken sürekli bir deneme-yanýlma döngüsüne girecek ve normalde basit olan detaylarda çok fazla zaman kaybedecektim. 
Yapay zeka ile tüm bu iþleri bir iþbirlikçi gibi yürüterek bu fazý olmasý gerekenden üç kat daha hýzlý ve sorunsuz bitirdim.

# AI sizi nerede yanýlttý?
Bu oturumda AI beni özellikle iki noktada yanýlttý ve müdahale etmem gerekti:

- UML Diyagramý Çizim Aracý:
AI, sistemin mimari diyagramýný oluþturmam için bana ilk olarak harici bir araç olan draw.io'yu kullanmamý ve görseli projeye resim olarak eklememi önerdi. Ancak konuyu biraz daha araþtýrýnca, GitHub'ýn Markdown içinde doðrudan desteklediði Mermaid.js kütüphanesinin çok daha mantýklý, sürdürülebilir ve kodla entegre olduðunu fark ettim. AI'ýn önerisini reddedip UML diyagramýný Mermaid ile çizmeye karar verdim.

- Gereksiz (Over-engineering) Kod Üretimi:
Projemin mantýðýný ve gereksinimlerini AI'a anlattýktan sonra, AI bana çalýþabilen ancak projenin kapsamý için aþýrý karmaþýk ve iþime yaramayan bazý ekstra sýnýf tasarýmlarý sundu. Bunlarý doðrudan projeye almak yerine, kodu inceleyip bana yaramayan kýsýmlarý temizlemem ve projeme uygun sade bir yapýya getirecek þekilde düzenlemem gerekti.