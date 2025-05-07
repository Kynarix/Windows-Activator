import os
import sys
import ctypes
import subprocess
import winreg
import time
import random
import platform

def admin_kontrolu():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not admin_kontrolu():
    print("Yönetici izni gerekiyor! Yeniden başlatılıyor...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

class Renkler:
    MAVI = '\033[94m'
    YESIL = '\033[92m'
    SARI = '\033[93m'
    KIRMIZI = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def windows_surumu_tespit():
    try:
        win_ver = platform.win32_ver()[0]
        win_edition = "Bilinmiyor"
        
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
            product_name = winreg.QueryValueEx(key, "ProductName")[0]
            if product_name:
                win_edition = product_name
        except:
            pass
    
        if win_edition == "Bilinmiyor":
            try:
                output = subprocess.check_output("wmic os get Caption", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                lines = [line.strip() for line in output.split('\n') if line.strip()]
                if len(lines) > 1:
                    win_edition = lines[1]
            except:
                pass
        
        if win_edition == "Bilinmiyor":
            try:
                output = subprocess.check_output("powershell -command \"(Get-WmiObject -class Win32_OperatingSystem).Caption\"", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                win_edition = output.strip()
            except:
                pass
        
        if win_edition == "Bilinmiyor":
            try:
                output = subprocess.check_output("systeminfo | findstr /B /C:\"OS Name\"", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                if ":" in output:
                    win_edition = output.split(":", 1)[1].strip()
            except:
                pass
        
        if win_edition == "Bilinmiyor":
            try:
                output = subprocess.check_output("ver", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                win_edition = f"Windows {output.strip()}"
            except:
                pass
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
            build_number = int(winreg.QueryValueEx(key, "CurrentBuildNumber")[0])
            if build_number >= 22000:
                win_edition = win_edition.replace("Windows 10", "Windows 11")
                win_ver = "11"
        except:
            pass
        
        print(f"{Renkler.BOLD}{Renkler.MAVI}Tespit edilen Windows sürümü: {win_edition} ({win_ver}){Renkler.RESET}")
        
        if "Windows 11" in win_edition or win_ver == "11":
            return "11", win_edition
        elif "Windows 10" in win_edition:
            return "10", win_edition
        elif "Windows 8.1" in win_edition or ("8.1" in win_ver):
            return "8.1", win_edition
        elif "Windows 8" in win_edition or (win_ver.startswith("8") and not "8.1" in win_ver):
            return "8", win_edition
        elif "Windows 7" in win_edition or win_ver.startswith("7"):
            return "7", win_edition
        else:
            for ver in ["11", "10", "8.1", "8", "7"]:
                if ver in win_edition or ver in win_ver:
                    return ver, win_edition
            print(f"{Renkler.KIRMIZI}Windows sürümü otomatik olarak tespit edilemedi!{Renkler.RESET}")
            print(f"{Renkler.SARI}Lütfen Windows sürümünüzü seçin:{Renkler.RESET}")
            print("1. Windows 11")
            print("2. Windows 10")
            print("3. Windows 8.1")
            print("4. Windows 8")
            print("5. Windows 7")
            
            secim = input(f"{Renkler.BOLD}Seçiminiz (1-5): {Renkler.RESET}")
            
            if secim == "1":
                return "11", "Windows 11"
            elif secim == "2":
                return "10", "Windows 10"
            elif secim == "3":
                return "8.1", "Windows 8.1"
            elif secim == "4":
                return "8", "Windows 8"
            elif secim == "5":
                return "7", "Windows 7"
            else:
                return "10", "Windows 10" 
    
    except Exception as e:
        print(f"{Renkler.KIRMIZI}Windows sürümü tespit edilirken hata oluştu: {str(e)}{Renkler.RESET}")
        print(f"{Renkler.SARI}Varsayılan olarak Windows 10 kabul ediliyor...{Renkler.RESET}")
        return "10", "Windows 10"

KMS_SUNUCULARI = [
    "kms.digiboy.ir",
    "kms.cangshui.net",
    "kms.03k.org",
    "kms.chinancce.com",
    "kms.ddns.net",
    "kms.loli.beer",
    "kms.ddz.red",
    "kms.mogeko.me",
    "kms8.msguides.com",
    "kms9.msguides.com",
    "kms.srv.crsoo.com",
    "kms.loli.best",
    "kms.digiboy.ir",
    "kms.library.hk"
]

WINDOWS_KEYS = {
    "7": {
        "Professional": "FJ82H-XT6CR-J8D7P-XQJJ2-GPDD4",
        "Professional N": "MRPKT-YTG23-K7D7T-X2JMM-QY7MG",
        "Enterprise": "33PXH-7Y6KF-2VJC9-XBBR8-HVTHH",
        "Enterprise N": "YDRBP-3D83W-TY26F-D46B2-XCKRJ",
        "Enterprise E": "C29WB-22CC8-VJ326-GHFJW-H9DH4",
        "Ultimate": "RHTBY-VWY6D-QJRJ9-JGQ3X-Q2289"
    },
    "8": {
        "Professional": "NG4HW-VH26C-733KW-K6F98-J8CK4",
        "Professional N": "XCVCF-2NXM9-723PB-MHCB7-2RYQQ",
        "Enterprise": "32JNW-9KQ84-P47T8-D8GGY-CWCK7",
        "Enterprise N": "JMNMF-RHW7P-DMY6X-RF3DR-X2BQT"
    },
    "8.1": {
        "Professional": "GCRJD-8NW9H-F2CDX-CCM8D-9D6T9",
        "Professional N": "HMCNV-VVBFX-7HMBH-CTY9B-B4FXY",
        "Enterprise": "MHF9N-XY6XB-WVXMC-BTDCT-MKKG7",
        "Enterprise N": "TT4HM-HN7YT-62K67-RGRQJ-JFFXW"
    },
    "10": {
        "Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
        "Home N": "3KHY7-WNT83-DGQKR-F7HPR-844BM",
        "Home Single Language": "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
        "Home Country Specific": "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR",
        "Professional": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
        "Professional N": "MH37W-N47XK-V7XM9-C7227-GCQG9",
        "Education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
        "Education N": "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",
        "Enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
        "Enterprise N": "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
        "Enterprise LTSC 2019": "M7XTQ-FN8P6-TTKYV-9D4CC-J462D",
        "Enterprise N LTSC 2019": "92NFX-8DJQP-P6BBQ-THF9C-7CG2H"
    },
    "11": {
        "Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
        "Home N": "3KHY7-WNT83-DGQKR-F7HPR-844BM",
        "Professional": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
        "Professional N": "MH37W-N47XK-V7XM9-C7227-GCQG9",
        "Education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
        "Education N": "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",
    }
}

OFFICE_KEYS = {
    "2010": {
        "Professional Plus": "VYBBJ-TRJPB-QFQRF-QFT4D-H3GVB",
        "Standard": "V7QKV-4XVVR-XYV4D-F7DFM-8R6BM",
        "Home and Business": "D6QFG-VBYP2-XQHM7-J97RH-VVRCK"
    },
    "2013": {
        "Professional Plus": "YC7DK-G2NP3-2QQC3-J6H88-GVGXT",
        "Standard": "KBKQT-2NMXY-JJWGP-M62JB-92CD4",
        "Home and Business": "VFTYK-CD9Y3-77WBP-2D7Y9-9KYWG"
    },
    "2016": {
        "Professional Plus": "XQNVK-8JYDB-WJ9W3-YJ8YR-WFG99",
        "Standard": "JNRGM-WHDWX-FJJG3-K47QV-DRTFM",
        "Project Professional": "YG9NW-3K39V-2T3HJ-93F3Q-G83KT",
        "Visio Professional": "PD3PC-RHNGV-FXJ29-8JK7D-RJRJK"
    },
    "2019": {
        "Professional Plus": "NMMKJ-6RK4F-KMJVX-8D9MJ-6MWKP",
        "Standard": "6NWWJ-YQWMR-QKGCB-6TMB3-9D9HK",
        "Project Professional": "B4NPR-3FKK7-T2MBV-FRQ4W-PKD2B",
        "Visio Professional": "9BGNQ-K37YR-RQHF2-38RQ3-7VCBB"
    },
    "2021": {
        "Professional Plus": "FXYTK-NJJ8C-GB6DW-3DYQT-6F7TH",
        "Standard": "KDX7X-BNVR8-TXXGX-4Q7Y8-78VT3",
        "Project Professional": "FTNWT-C6WBT-8HMGF-K9PRX-QV9H8",
        "Visio Professional": "KNH8D-FGHT4-T8RK3-CTDYJ-K2HT4"
    }
}

def komut_calistir(komut, baslik=None):
    if baslik:
        print(f"\n{Renkler.BOLD}{Renkler.SARI}[{baslik}]{Renkler.RESET}")
    
    print(f"{Renkler.MAVI}Çalıştırılıyor: {komut}{Renkler.RESET}")
    
    try:
        sonuc = subprocess.check_output(komut, shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        print(f"{Renkler.YESIL}{sonuc}{Renkler.RESET}")
        return True, sonuc
    except subprocess.CalledProcessError as e:
        print(f"{Renkler.KIRMIZI}Hata: {e.output}{Renkler.RESET}")
        return False, e.output
    except UnicodeDecodeError:

        try:
            sonuc = subprocess.check_output(komut, shell=True, stderr=subprocess.STDOUT)
            sonuc_str = sonuc.decode('cp850', errors='replace')
            print(f"{Renkler.YESIL}{sonuc_str}{Renkler.RESET}")
            return True, sonuc_str
        except Exception as e:
            print(f"{Renkler.KIRMIZI}Kodlama hatası: {str(e)}{Renkler.RESET}")
            return False, str(e)

def windows_aktive_et(win_ver, win_edition):
    print(f"\n{Renkler.BOLD}{Renkler.SARI}Windows {win_ver} {win_edition} aktivasyonu başlatılıyor...{Renkler.RESET}")
    
    if win_ver == "11":
        print(f"{Renkler.BOLD}{Renkler.MAVI}Windows 11 tespit edildi. Windows 11 için özel ürün anahtarları kullanılacak.{Renkler.RESET}")
    
    mevcut_anahtar = mevcut_windows_anahtari_tespit()
    if mevcut_anahtar:
        print(f"{Renkler.BOLD}{Renkler.YESIL}Mevcut Windows ürün anahtarı tespit edildi: {mevcut_anahtar}{Renkler.RESET}")
        kullan_secim = input(f"{Renkler.BOLD}Mevcut anahtarı kullanmak istiyor musunuz? (E/H): {Renkler.RESET}").upper()
        if kullan_secim == "E":
            anahtar = mevcut_anahtar
        else:
            anahtar = None
    else:
        print(f"{Renkler.KIRMIZI}Mevcut Windows ürün anahtarı tespit edilemedi!{Renkler.RESET}")
        anahtar = None
    
    if not anahtar:
        for edition in WINDOWS_KEYS.get(win_ver, {}):
            if edition.lower() in win_edition.lower():
                anahtar = WINDOWS_KEYS[win_ver][edition]
                break
    
    if not anahtar:
        print(f"{Renkler.KIRMIZI}Uygun ürün anahtarı bulunamadı!{Renkler.RESET}")
        editions = list(WINDOWS_KEYS.get(win_ver, {}).keys())
        if editions:
            print(f"{Renkler.SARI}Mevcut sürümler:{Renkler.RESET}")
            for i, edition in enumerate(editions, 1):
                print(f"{Renkler.BOLD}{i}.{Renkler.RESET} {edition}")
            
            secim = input(f"\n{Renkler.BOLD}Hangi sürümü aktive etmek istiyorsunuz? (numara girin): {Renkler.RESET}")
            try:
                secim_index = int(secim) - 1
                if 0 <= secim_index < len(editions):
                    selected_edition = editions[secim_index]
                    anahtar = WINDOWS_KEYS[win_ver][selected_edition]
                    print(f"{Renkler.YESIL}Seçilen sürüm: {selected_edition}{Renkler.RESET}")
                else:
                    print(f"{Renkler.KIRMIZI}Geçersiz seçim! Lütfen 1-{len(editions)} arasında bir sayı girin.{Renkler.RESET}")
                    return False
            except ValueError:
                print(f"{Renkler.KIRMIZI}Geçersiz giriş! Lütfen bir sayı girin.{Renkler.RESET}")
                return False
        else:
            print(f"{Renkler.SARI}Ürün anahtarını manuel olarak girmek ister misiniz?{Renkler.RESET}")
            manuel_secim = input(f"{Renkler.BOLD}Manuel anahtar girişi (E/H): {Renkler.RESET}").upper()
            if manuel_secim == "E":
                anahtar = input(f"{Renkler.BOLD}Ürün anahtarını girin (XXXXX-XXXXX-XXXXX-XXXXX-XXXXX): {Renkler.RESET}")
                if len(anahtar.replace("-", "")) != 25:
                    print(f"{Renkler.KIRMIZI}Geçersiz ürün anahtarı formatı!{Renkler.RESET}")
                    return False
            else:
                return False
    komut_calistir("cscript //nologo %windir%\\system32\\slmgr.vbs /upk", "Mevcut ürün anahtarı kaldırılıyor")
    komut_calistir("cscript //nologo %windir%\\system32\\slmgr.vbs /cpky", "Ürün anahtarı kayıt bilgileri temizleniyor")

    komut_calistir(f"cscript //nologo %windir%\\system32\\slmgr.vbs /ipk {anahtar}", "Yeni ürün anahtarı yükleniyor")
    
    kms_sunucu = random.choice(KMS_SUNUCULARI)
    komut_calistir(f"cscript //nologo %windir%\\system32\\slmgr.vbs /skms {kms_sunucu}", "KMS sunucusu ayarlanıyor")
    
    basarili, _ = komut_calistir("cscript //nologo %windir%\\system32\\slmgr.vbs /ato", "Windows aktivasyonu yapılıyor")
    
    if not basarili:
        print(f"{Renkler.SARI}Farklı bir KMS sunucusu deneniyor...{Renkler.RESET}")
        
        for sunucu in KMS_SUNUCULARI:
            if sunucu != kms_sunucu:
                komut_calistir(f"cscript //nologo %windir%\\system32\\slmgr.vbs /skms {sunucu}", "Alternatif KMS sunucusu ayarlanıyor")
                basarili, _ = komut_calistir("cscript //nologo %windir%\\system32\\slmgr.vbs /ato", "Windows aktivasyonu tekrar deneniyor")
                if basarili:
                    print(f"\n{Renkler.BOLD}{Renkler.YESIL}Windows {win_ver} {win_edition} başarıyla aktive edildi!{Renkler.RESET}")
                    return True
        
        print(f"\n{Renkler.BOLD}{Renkler.KIRMIZI}Tüm KMS sunucuları denendi, aktivasyon başarısız!{Renkler.RESET}")
        return False
    
    print(f"\n{Renkler.BOLD}{Renkler.YESIL}Windows {win_ver} {win_edition} başarıyla aktive edildi!{Renkler.RESET}")
    return True

def windows_aktivasyon_iptal():
    print(f"\n{Renkler.BOLD}{Renkler.SARI}Windows aktivasyonu iptal ediliyor...{Renkler.RESET}")
    
    komut_calistir("cscript //nologo %windir%\\system32\\slmgr.vbs /upk", "Ürün anahtarı kaldırılıyor")
    komut_calistir("cscript //nologo %windir%\\system32\\slmgr.vbs /cpky", "Ürün anahtarı kayıt bilgileri temizleniyor")
    
    print(f"\n{Renkler.BOLD}{Renkler.YESIL}Windows aktivasyonu başarıyla iptal edildi!{Renkler.RESET}")
    return True

def office_surumu_tespit():
    print(f"{Renkler.BOLD}{Renkler.MAVI}Office sürümü tespit ediliyor...{Renkler.RESET}")
    
    office_versiyonlari = []
    
    if os.path.exists("C:\\Program Files\\Microsoft Office\\Office14") or os.path.exists("C:\\Program Files (x86)\\Microsoft Office\\Office14"):
        office_versiyonlari.append("2010")
    
    if os.path.exists("C:\\Program Files\\Microsoft Office\\Office15") or os.path.exists("C:\\Program Files (x86)\\Microsoft Office\\Office15"):
        office_versiyonlari.append("2013")
    
    if os.path.exists("C:\\Program Files\\Microsoft Office\\Office16") or os.path.exists("C:\\Program Files (x86)\\Microsoft Office\\Office16"):

        try:

            office_path = None
            if os.path.exists("C:\\Program Files\\Microsoft Office\\Office16"):
                office_path = "C:\\Program Files\\Microsoft Office\\Office16"
            elif os.path.exists("C:\\Program Files (x86)\\Microsoft Office\\Office16"):
                office_path = "C:\\Program Files (x86)\\Microsoft Office\\Office16"
            
            if office_path:
                if os.path.exists(f"{office_path}\\OSPP.VBS"):
                    try:
                        output = subprocess.check_output(f"cscript //nologo \"{office_path}\\OSPP.VBS\" /dstatus", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                        if "Office 21" in output:
                            office_versiyonlari.append("2021")
                        elif "Office 19" in output:
                            office_versiyonlari.append("2019")
                        else:
                            office_versiyonlari.append("2016")
                    except:
                        office_versiyonlari.append("2016")
        except:
            office_versiyonlari.append("2016")
    
    if office_versiyonlari:
        print(f"{Renkler.BOLD}{Renkler.MAVI}Tespit edilen Office sürümleri: {', '.join(['Office ' + ver for ver in office_versiyonlari])}{Renkler.RESET}")
    else:
        print(f"{Renkler.BOLD}{Renkler.KIRMIZI}Hiçbir Office sürümü tespit edilemedi!{Renkler.RESET}")
    
    return office_versiyonlari

def office_aktive_et(office_ver):
    print(f"\n{Renkler.BOLD}{Renkler.SARI}Office {office_ver} aktivasyonu başlatılıyor...{Renkler.RESET}")
    
    office_path = None
    office_arch = None
    
    if os.path.exists("C:\\Program Files\\Microsoft Office"):
        office_path = "C:\\Program Files\\Microsoft Office"
        office_arch = "64"
    elif os.path.exists("C:\\Program Files (x86)\\Microsoft Office"):
        office_path = "C:\\Program Files (x86)\\Microsoft Office"
        office_arch = "32"
    
    if not office_path:
        print(f"{Renkler.KIRMIZI}Office kurulum yolu bulunamadı!{Renkler.RESET}")
        return False
    
    ospp_path = None
    
    if office_ver == "2010":
        ospp_path = f"{office_path}\\Office14\\OSPP.VBS"
    elif office_ver == "2013":
        ospp_path = f"{office_path}\\Office15\\OSPP.VBS"
    elif office_ver in ["2016", "2019", "2021"]:
        ospp_path = f"{office_path}\\Office16\\OSPP.VBS"
    
    if not os.path.exists(ospp_path):
        print(f"{Renkler.KIRMIZI}OSPP.VBS dosyası bulunamadı: {ospp_path}{Renkler.RESET}")
        return False
    
    print(f"{Renkler.SARI}Office {office_ver} için mevcut sürümler:{Renkler.RESET}")
    for i, edition in enumerate(OFFICE_KEYS[office_ver].keys(), 1):
        print(f"{i}. {edition}")
    
    secim = input(f"{Renkler.BOLD}Hangi sürümü aktive etmek istiyorsunuz? (numara girin): {Renkler.RESET}")
    
    try:
        secim_index = int(secim) - 1
        editions = list(OFFICE_KEYS[office_ver].keys())
        selected_edition = editions[secim_index]
        anahtar = OFFICE_KEYS[office_ver][selected_edition]
    except:
        print(f"{Renkler.KIRMIZI}Geçersiz seçim!{Renkler.RESET}")
        return False
    
    komut_calistir(f"cscript //nologo \"{ospp_path}\" /osppsvcrestart", "OSPP servisi yeniden başlatılıyor")
    komut_calistir(f"cscript //nologo \"{ospp_path}\" /inpkey:{anahtar}", "Ürün anahtarı yükleniyor")
    
    kms_sunucu = random.choice(KMS_SUNUCULARI)
    komut_calistir(f"cscript //nologo \"{ospp_path}\" /sethst:{kms_sunucu}", "KMS sunucusu ayarlanıyor")
    
    basarili, _ = komut_calistir(f"cscript //nologo \"{ospp_path}\" /act", "Office aktivasyonu yapılıyor")
    
    if basarili:
        print(f"\n{Renkler.BOLD}{Renkler.YESIL}Office {office_ver} {selected_edition} başarıyla aktive edildi!{Renkler.RESET}")
    else:
        print(f"\n{Renkler.BOLD}{Renkler.KIRMIZI}Office aktivasyonu başarısız oldu!{Renkler.RESET}")
        print(f"{Renkler.SARI}Farklı bir KMS sunucusu deneniyor...{Renkler.RESET}")
        
        for sunucu in KMS_SUNUCULARI:
            if sunucu != kms_sunucu:
                komut_calistir(f"cscript //nologo \"{ospp_path}\" /sethst:{sunucu}", "Alternatif KMS sunucusu ayarlanıyor")
                basarili, _ = komut_calistir(f"cscript //nologo \"{ospp_path}\" /act", "Office aktivasyonu tekrar deneniyor")
                if basarili:
                    print(f"\n{Renkler.BOLD}{Renkler.YESIL}Office {office_ver} {selected_edition} başarıyla aktive edildi!{Renkler.RESET}")
                    return True
        
        print(f"\n{Renkler.BOLD}{Renkler.KIRMIZI}Tüm KMS sunucuları denendi, aktivasyon başarısız!{Renkler.RESET}")
        return False
    
    return True

def office_aktivasyon_iptal(office_ver):
    print(f"\n{Renkler.BOLD}{Renkler.SARI}Office {office_ver} aktivasyonu iptal ediliyor...{Renkler.RESET}")
    
    office_path = None
    
    if os.path.exists("C:\\Program Files\\Microsoft Office"):
        office_path = "C:\\Program Files\\Microsoft Office"
    elif os.path.exists("C:\\Program Files (x86)\\Microsoft Office"):
        office_path = "C:\\Program Files (x86)\\Microsoft Office"
    
    if not office_path:
        print(f"{Renkler.KIRMIZI}Office kurulum yolu bulunamadı!{Renkler.RESET}")
        return False
    
    ospp_path = None
    
    if office_ver == "2010":
        ospp_path = f"{office_path}\\Office14\\OSPP.VBS"
    elif office_ver == "2013":
        ospp_path = f"{office_path}\\Office15\\OSPP.VBS"
    elif office_ver in ["2016", "2019", "2021"]:
        ospp_path = f"{office_path}\\Office16\\OSPP.VBS"
    
    if not os.path.exists(ospp_path):
        print(f"{Renkler.KIRMIZI}OSPP.VBS dosyası bulunamadı: {ospp_path}{Renkler.RESET}")
        return False
    
    komut_calistir(f"cscript //nologo \"{ospp_path}\" /unpkey:ALL", "Tüm ürün anahtarları kaldırılıyor")
    
    print(f"\n{Renkler.BOLD}{Renkler.YESIL}Office {office_ver} aktivasyonu başarıyla iptal edildi!{Renkler.RESET}")
    return True

def mevcut_windows_anahtari_tespit():
    print(f"\n{Renkler.BOLD}{Renkler.SARI}Mevcut Windows ürün anahtarı tespit ediliyor...{Renkler.RESET}")
    
    try:
        output = subprocess.check_output("wmic path softwarelicensingservice get OA3xOriginalProductKey", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1 and len(lines[1]) > 5: 
            return lines[1]
        
        output = subprocess.check_output('powershell -command "(Get-WmiObject -query \'select * from SoftwareLicensingService\').OA3xOriginalProductKey"', shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        if len(output.strip()) > 5:
            return output.strip()
        
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SoftwareProtectionPlatform")
            anahtar = winreg.QueryValueEx(key, "BackupProductKeyDefault")[0]
            if anahtar and len(anahtar) > 5:
                return anahtar
        except:
            pass
        
        try:
            output = subprocess.check_output("cscript //nologo %windir%\\system32\\slmgr.vbs /dlv", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            for line in output.split('\n'):
                if "Product Key:" in line or "Ürün Anahtarı:" in line:
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        anahtar = parts[1].strip()
                        if len(anahtar) > 5 and anahtar != "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX":
                            return anahtar
        except:
            pass
        
        return None
    except Exception as e:
        print(f"{Renkler.KIRMIZI}Ürün anahtarı tespit edilirken hata oluştu: {str(e)}{Renkler.RESET}")
        return None

def konsol_modernlestir():
    os.system("title Windows Activator - Yapımcı: Kynarix")
    
    os.system("color")
    
    os.system("mode con: cols=120 lines=30")
    
    os.system("cls" if os.name == "nt" else "clear")

def banner_goster():
    print(f"""
    {Renkler.YESIL}██╗    ██╗██╗███╗   ██╗    {Renkler.SARI} █████╗  ██████╗████████╗██╗██╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗ 
    {Renkler.YESIL}██║    ██║██║████╗  ██║    {Renkler.SARI}██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    {Renkler.YESIL}██║ █╗ ██║██║██╔██╗ ██║    {Renkler.SARI}███████║██║        ██║   ██║██║   ██║███████║   ██║   ██║   ██║██████╔╝
    {Renkler.YESIL}██║███╗██║██║██║╚██╗██║    {Renkler.SARI}██╔══██║██║        ██║   ██║╚██╗ ██╔╝██╔══██║   ██║   ██║   ██║██╔══██╗
    {Renkler.YESIL}╚███╔███╔╝██║██║ ╚████║    {Renkler.SARI}██║  ██║╚██████╗   ██║   ██║ ╚████╔╝ ██║  ██║   ██║   ╚██████╔╝██║  ██║
    {Renkler.YESIL} ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝    {Renkler.SARI}╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝{Renkler.RESET}
{Renkler.BOLD}{Renkler.MAVI}                                                                                                       Yapımcı: Kynarix{Renkler.RESET}
""")

def cizgi_ciz(renk=Renkler.MAVI, uzunluk=100):
    print(f"{Renkler.BOLD}{renk}{'-' * uzunluk}{Renkler.RESET}")

def baslik_goster(baslik, renk=Renkler.MAVI):
    print(f"\n{Renkler.BOLD}{renk}[ {baslik} ]{Renkler.RESET}")
    cizgi_ciz(renk)

def yukleniyor(mesaj, sure=2):
    animasyon = ["|", "/", "-", "\\"]
    baslangic = time.time()
    i = 0
    while time.time() - baslangic < sure:
        print(f"\r{Renkler.BOLD}{Renkler.SARI}{mesaj} {animasyon[i % len(animasyon)]}{Renkler.RESET}", end="")
        time.sleep(0.1)
        i += 1
    print(f"\r{Renkler.BOLD}{Renkler.YESIL}{mesaj} Tamamlandı!{Renkler.RESET}" + " " * 10)

def bilgi_kutusu(baslik, mesaj, renk=Renkler.MAVI):
    print(f"\n{Renkler.BOLD}{renk}[ {baslik} ]{Renkler.RESET}")
    print(f"{renk}{'-' * 50}{Renkler.RESET}")
    print(f"{Renkler.BOLD}{mesaj}{Renkler.RESET}")
    print(f"{renk}{'-' * 50}{Renkler.RESET}")

def sistem_bilgilerini_goster(win_ver, win_edition, office_versiyonlari):
    cpu_info = "Bilinmiyor"
    try:
        output = subprocess.check_output("wmic cpu get name", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            cpu_info = lines[1]
    except:
        try:
            output = subprocess.check_output('powershell -command "(Get-WmiObject -Class Win32_Processor).Name"', shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            if output.strip():
                cpu_info = output.strip()
        except:
            pass
    
    ram_gb = "Bilinmiyor"
    try:
        output = subprocess.check_output("wmic ComputerSystem get TotalPhysicalMemory", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1 and lines[1].isdigit():
            ram_gb = f"{round(int(lines[1]) / (1024**3))}"
    except:
        try:
            output = subprocess.check_output('powershell -command "[math]::Round((Get-WmiObject -Class Win32_ComputerSystem).TotalPhysicalMemory / 1GB)"', shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            if output.strip() and output.strip().isdigit():
                ram_gb = output.strip()
        except:
            try:
                output = subprocess.check_output("systeminfo | findstr /C:\"Total Physical Memory\"", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                if ":" in output:
                    ram_str = output.split(":", 1)[1].strip()
                    ram_str = ram_str.replace(",", "").replace("MB", "").strip()
                    if ram_str.isdigit():
                        ram_gb = f"{round(int(ram_str) / 1024)}"
            except:
                pass
    
    disk_gb = "Bilinmiyor"
    free_disk_gb = "Bilinmiyor"
    try:
        output = subprocess.check_output("wmic logicaldisk where DeviceID='C:' get Size,FreeSpace", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                free_space = int(parts[0])
                total_size = int(parts[1])
                free_disk_gb = f"{round(free_space / (1024**3))}"
                disk_gb = f"{round(total_size / (1024**3))}"
    except:
        try:
            output = subprocess.check_output('powershell -command "$disk = Get-WmiObject -Class Win32_LogicalDisk -Filter \\"DeviceID=\'C:\'\\" | Select-Object Size,FreeSpace; [math]::Round($disk.Size / 1GB)"', shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            if output.strip() and output.strip().isdigit():
                disk_gb = output.strip()
                
            output = subprocess.check_output('powershell -command "$disk = Get-WmiObject -Class Win32_LogicalDisk -Filter \\"DeviceID=\'C:\'\\" | Select-Object Size,FreeSpace; [math]::Round($disk.FreeSpace / 1GB)"', shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            if output.strip() and output.strip().isdigit():
                free_disk_gb = output.strip()
        except:
            try:
                output = subprocess.check_output("dir C:", shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                for line in output.split('\n'):
                    if "bytes free" in line.lower():
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part.replace(",", "").isdigit() and i+2 < len(parts) and parts[i+1] == "bytes" and parts[i+2] == "free":
                                free_bytes = int(part.replace(",", ""))
                                free_disk_gb = f"{round(free_bytes / (1024**3))}"
                                break
            except:
                pass
    
    baslik_goster("SİSTEM BİLGİLERİ", Renkler.YESIL)
    print(f"{Renkler.BOLD}İşletim Sistemi: {Renkler.RESET}{win_edition}")
    print(f"{Renkler.BOLD}Windows Sürümü: {Renkler.RESET}Windows {win_ver}")
    print(f"{Renkler.BOLD}Office Sürümleri: {Renkler.RESET}{', '.join(['Office ' + v for v in office_versiyonlari]) if office_versiyonlari else 'Bulunamadı'}")
    print(f"{Renkler.BOLD}CPU: {Renkler.RESET}{cpu_info[:60]}")
    
    if ram_gb != "Bilinmiyor":
        print(f"{Renkler.BOLD}RAM: {Renkler.RESET}{ram_gb} GB")
    else:
        print(f"{Renkler.BOLD}RAM: {Renkler.RESET}Bilinmiyor")
    
    if disk_gb != "Bilinmiyor" and free_disk_gb != "Bilinmiyor":
        print(f"{Renkler.BOLD}Disk (C:): {Renkler.RESET}{disk_gb} GB (Boş: {free_disk_gb} GB)")
    elif disk_gb != "Bilinmiyor":
        print(f"{Renkler.BOLD}Disk (C:): {Renkler.RESET}{disk_gb} GB")
    else:
        print(f"{Renkler.BOLD}Disk (C:): {Renkler.RESET}Bilinmiyor")
    
    cizgi_ciz(Renkler.YESIL)

def ana_menu():
    konsol_modernlestir()
    
    banner_goster()
    
    yukleniyor("Sistem bilgileri yükleniyor", 1)
    
    win_ver, win_edition = windows_surumu_tespit()

    office_versiyonlari = office_surumu_tespit()
    
    sistem_bilgilerini_goster(win_ver, win_edition, office_versiyonlari)
    
    baslik_goster("MENÜ", Renkler.SARI)
    
    print(f"{Renkler.BOLD}Windows İşlemleri:{Renkler.RESET}")
    print(f"  1. Windows'u Aktive Et")
    print(f"  2. Windows Aktivasyonunu İptal Et")
    print(f"  3. Windows Aktivasyon Durumunu Kontrol Et")
    print()
    print(f"{Renkler.BOLD}Office İşlemleri:{Renkler.RESET}")
    print(f"  4. Office'i Aktive Et")
    print(f"  5. Office Aktivasyonunu İptal Et")
    print(f"  6. Office Aktivasyon Durumunu Kontrol Et")
    print()
    print(f"{Renkler.BOLD}Diğer İşlemler:{Renkler.RESET}")
    print(f"  7. Tüm Aktivasyonları İptal Et")
    print(f"  8. Çıkış")
    cizgi_ciz(Renkler.SARI)
    
    secim = input(f"{Renkler.BOLD}Seçiminiz (1-8): {Renkler.RESET}")
    
    if secim == "1":
        windows_aktive_et(win_ver, win_edition)
    elif secim == "2":
        windows_aktivasyon_iptal()
    elif secim == "3":
        komut_calistir("cscript //nologo %windir%\\system32\\slmgr.vbs /dli", "Windows Aktivasyon Durumu")
        komut_calistir("cscript //nologo %windir%\\system32\\slmgr.vbs /xpr", "Windows Aktivasyon Süresi")
    elif secim == "4":
        if office_versiyonlari:
            if len(office_versiyonlari) > 1:
                baslik_goster("OFFİCE SÜRÜMÜ SEÇİN", Renkler.SARI)
                print("Birden fazla Office sürümü tespit edildi.")
                for i, ver in enumerate(office_versiyonlari, 1):
                    print(f"{Renkler.BOLD}{i}.{Renkler.RESET} Office {ver}")
                ver_secim = input(f"\n{Renkler.BOLD}Hangi Office sürümünü aktive etmek istiyorsunuz? (numara girin): {Renkler.RESET}")
                try:
                    selected_ver = office_versiyonlari[int(ver_secim) - 1]
                    office_aktive_et(selected_ver)
                except:
                    bilgi_kutusu("HATA", "Geçersiz seçim!", Renkler.KIRMIZI)
            else:
                office_aktive_et(office_versiyonlari[0])
        else:
            baslik_goster("OFFİCE BULUNAMADI", Renkler.KIRMIZI)
            print("Hiçbir Office sürümü tespit edilemedi!")
            print(f"{Renkler.SARI}Manuel olarak Office sürümünü seçin:{Renkler.RESET}")
            for i, ver in enumerate(["2010", "2013", "2016", "2019", "2021"], 1):
                print(f"{Renkler.BOLD}{i}.{Renkler.RESET} Office {ver}")
            ver_secim = input(f"\n{Renkler.BOLD}Hangi Office sürümünü aktive etmek istiyorsunuz? (numara girin): {Renkler.RESET}")
            try:
                office_versiyonlari = ["2010", "2013", "2016", "2019", "2021"]
                selected_ver = office_versiyonlari[int(ver_secim) - 1]
                office_aktive_et(selected_ver)
            except:
                bilgi_kutusu("HATA", "Geçersiz seçim!", Renkler.KIRMIZI)
    elif secim == "5":
        if office_versiyonlari:
            if len(office_versiyonlari) > 1:
                baslik_goster("OFFİCE SÜRÜMÜ SEÇİN", Renkler.SARI)
                print("Birden fazla Office sürümü tespit edildi.")
                for i, ver in enumerate(office_versiyonlari, 1):
                    print(f"{Renkler.BOLD}{i}.{Renkler.RESET} Office {ver}")
                ver_secim = input(f"\n{Renkler.BOLD}Hangi Office sürümünün aktivasyonunu iptal etmek istiyorsunuz? (numara girin): {Renkler.RESET}")
                try:
                    selected_ver = office_versiyonlari[int(ver_secim) - 1]
                    office_aktivasyon_iptal(selected_ver)
                except:
                    bilgi_kutusu("HATA", "Geçersiz seçim!", Renkler.KIRMIZI)
            else:
                office_aktivasyon_iptal(office_versiyonlari[0])
        else:
            baslik_goster("OFFİCE BULUNAMADI", Renkler.KIRMIZI)
            print("Hiçbir Office sürümü tespit edilemedi!")
            print(f"{Renkler.SARI}Manuel olarak Office sürümünü seçin:{Renkler.RESET}")
            for i, ver in enumerate(["2010", "2013", "2016", "2019", "2021"], 1):
                print(f"{Renkler.BOLD}{i}.{Renkler.RESET} Office {ver}")
            ver_secim = input(f"\n{Renkler.BOLD}Hangi Office sürümünün aktivasyonunu iptal etmek istiyorsunuz? (numara girin): {Renkler.RESET}")
            try:
                office_versiyonlari = ["2010", "2013", "2016", "2019", "2021"]
                selected_ver = office_versiyonlari[int(ver_secim) - 1]
                office_aktivasyon_iptal(selected_ver)
            except:
                bilgi_kutusu("HATA", "Geçersiz seçim!", Renkler.KIRMIZI)
    elif secim == "6":
        if office_versiyonlari:
            if len(office_versiyonlari) > 1:
                baslik_goster("OFFİCE SÜRÜMÜ SEÇİN", Renkler.SARI)
                print("Birden fazla Office sürümü tespit edildi.")
                for i, ver in enumerate(office_versiyonlari, 1):
                    print(f"{Renkler.BOLD}{i}.{Renkler.RESET} Office {ver}")
                ver_secim = input(f"\n{Renkler.BOLD}Hangi Office sürümünün aktivasyon durumunu kontrol etmek istiyorsunuz? (numara girin): {Renkler.RESET}")
                try:
                    selected_ver = office_versiyonlari[int(ver_secim) - 1]
                    office_aktivasyon_kontrol(selected_ver)
                except:
                    bilgi_kutusu("HATA", "Geçersiz seçim!", Renkler.KIRMIZI)
            else:
                office_aktivasyon_kontrol(office_versiyonlari[0])
        else:
            baslik_goster("OFFİCE BULUNAMADI", Renkler.KIRMIZI)
            print("Hiçbir Office sürümü tespit edilemedi!")
    elif secim == "7":
        baslik_goster("AKTİVASYON İPTAL", Renkler.SARI)
        print("Tüm aktivasyonlar iptal ediliyor...")
        yukleniyor("İşlem yapılıyor", 1)
        windows_aktivasyon_iptal()
        if office_versiyonlari:
            for ver in office_versiyonlari:
                office_aktivasyon_iptal(ver)
        bilgi_kutusu("BAŞARILI", "Tüm aktivasyonlar başarıyla iptal edildi!", Renkler.YESIL)
    elif secim == "8":
        baslik_goster("ÇIKIŞ", Renkler.SARI)
        print("Programdan çıkılıyor...")
        yukleniyor("Çıkış yapılıyor", 1)
        sys.exit(0)
    else:
        bilgi_kutusu("HATA", "Geçersiz seçim!", Renkler.KIRMIZI)
    
    input(f"\n{Renkler.BOLD}Ana menüye dönmek için Enter tuşuna basın...{Renkler.RESET}")
    ana_menu()

def office_aktivasyon_kontrol(office_ver):
    print(f"\n{Renkler.BOLD}{Renkler.SARI}Office {office_ver} aktivasyon durumu kontrol ediliyor...{Renkler.RESET}")
    
    office_path = None
    
    if os.path.exists("C:\\Program Files\\Microsoft Office"):
        office_path = "C:\\Program Files\\Microsoft Office"
    elif os.path.exists("C:\\Program Files (x86)\\Microsoft Office"):
        office_path = "C:\\Program Files (x86)\\Microsoft Office"
    
    if not office_path:
        print(f"{Renkler.KIRMIZI}Office kurulum yolu bulunamadı!{Renkler.RESET}")
        return False
    
    ospp_path = None
    
    if office_ver == "2010":
        ospp_path = f"{office_path}\\Office14\\OSPP.VBS"
    elif office_ver == "2013":
        ospp_path = f"{office_path}\\Office15\\OSPP.VBS"
    elif office_ver in ["2016", "2019", "2021"]:
        ospp_path = f"{office_path}\\Office16\\OSPP.VBS"
    
    if not os.path.exists(ospp_path):
        print(f"{Renkler.KIRMIZI}OSPP.VBS dosyası bulunamadı: {ospp_path}{Renkler.RESET}")
        return False
    
    komut_calistir(f"cscript //nologo \"{ospp_path}\" /dstatus", "Office Aktivasyon Durumu")
    
    return True

if __name__ == "__main__":
    ana_menu()