# 🔐 Etik Ağ Güvenlik Test Aracı

Bu proje, kendi ağınızda **etik güvenlik testleri** yapmanıza olanak tanır. Amacı, ağınızın güvenliğini kontrol etmek, olası zafiyetleri görmek ve farkındalık sağlamaktır. **Kesinlikle başkasının ağı üzerinde kullanılmamalıdır.**

---

## Özellikler

- 🌐 **Network Scan:** Ağınızdaki cihazları tespit eder ve port taraması yapar.  
- 📡 **Wi-Fi Güvenlik Taraması:** Wi-Fi ağlarını listeler ve olası güvenlik açıklarını tespit eder.  
- ⚡ **DeAuth Testi:** Belirli cihazlara veya tüm istemcilere deauthentication paketleri gönderir.  
- 🎭 **MITM Testi (ARP Spoofing):** Kendi ağınızda hedef IP ile router arasındaki ARP paketlerini test eder.  
- 📝 **Otomatik PDF Raporlama:** Tüm testlerin sonuçları zaman damgalı PDF raporuna kaydedilir.  

---


*Uyarılar

Bu araç sadece kendi ağınızda test etmek için tasarlanmıştır.

Başkasının ağında kullanmak yasalara aykırıdır.

Etik kullanım önemlidir; sorumluluk tamamen kullanıcıya aittir.


## Kullanım

1. Kodun çalışması için root yetkisine sahip olmanız gerekir.  
2. Terminalde çalıştırın:

```bash
sudo python3 main.py


Sırayla çalışır

Network Scan

Wi-Fi taraması

DeAuth testi (BSSID ve istemci MAC sorulur)

MITM testi (Gateway ve hedef IP sorulur)

Tüm sonuçlar security_report_YYYYMMDD_HHMMSS.pdf olarak kaydedilir.
Gereksinimler

Python 3.x

Scapy (pip install scapy)

Nmap (sudo apt install nmap)

Aircrack-ng, Airodump-ng, Aireplay-ng (sudo apt install aircrack-ng)

ReportLab (pip install reportlab)


