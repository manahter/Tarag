"""
Info:
    module      : Tarag
    description : Ağdaki cihazları bulur
    author      : Manahter


Files:
    getmac      : IP adresini kullanarak MAC adresini bulmamıza yardımcı olur.
                  get_mac_address(ip=ip)
                  main source: "https://github.com/GhostofGoes/getmac",

    getvendor   : MAC adresini kullanarak Üretici Markayı bulmamızı sağlar.
                  get_mac_vendor(mac)

    rapor       : Ağı tarama esnasında ekrana çıktı veren modüldür.

    INPROCESS   : Tarag modül dizininde INPROCESS isimli bir dosyanın varlığı, Tarama işleminde olduğunun göstergesidir.
                  Tarama bittiğinde dosya otomatik olarak silinir. Bu yüzden dosya bazen görünür bazen kaybolur.
                  ""    -> İçi boş dosya

    RESULTS     : Çıktıların biriktiği dosyadır
                  { IP: { "MAC": MAC, "VENDOR": VENDOR}, ... }


Methods:
    tarag.start()   -> None     -> Arka planda ağ taraması başlatılır
    tarag.scan()    -> None     -> start aynı
    tarag.inprocess -> bool     -> Tarama işleminde olup olmadığı sorgulanır.
    tarag.result    -> dict     -> { IP: { "MAC": MAC, "VENDOR": VENDOR}, ... } -> Bulunan cihaz bilgileri
    tarag.devices(  -> list     -> [ ("IP", "MAC", "VENDOR"), ... ] -> Bulunan cihaz bilgileri liste şeklinde
        only_esp    -> bool     -> Sadece bulunan ESPressif ürünlerini döndür
    tarag.wait(     -> bool     -> Tarama bitene kadar bekler. True-> İşlem bitti. False-> Zaman aşımı sonucu döndüm
        timeout     -> float    -> Zaman aşımı


Example:
    # İçe aktarma
    from .Tarag import tarag

    # Arkaplanda Ağ Taramayı başlat
    tarag.scan()

    # Tarama bitene kadar bekle
    tarag.wait()

    # Tarama sonuçlarını kullanabilirsin
    results = tarag.result

    # Bulunan cihaz bilgilerini yazdır
    print(*tarag.devices(), sep="\n")
"""

import subprocess
import time
import json
import sys
import os

# Sabitler
MAC = "MAC"
VENDOR = "VENDOR"
RESULTS = "RESULTS"
INPROCESS = "INPROCESS"

dirname = os.path.dirname(__file__)
PATH_RESULTS = os.path.join(dirname, RESULTS)
PATH_INPROCESS = os.path.join(dirname, INPROCESS)

# Ağ tarama işleminde olup olmadığı, INPROCESS isimli dosyanın olup olmadığına bağlanmıştır.
# Bu yüzden, modül import edilirken, bu dosya önceden kalmışsa silinir
if INPROCESS in os.listdir(dirname):
    os.remove(PATH_INPROCESS)


class TarAg:
    def __init__(self):
        self.inprocess = False

    def start(self):
        self.scan()

    def scan(self):
        """Ağdaki diğer cihazları tarar"""
        if self.inprocess:
            return

        self.inprocess = True

    @property
    def inprocess(self):
        return INPROCESS in os.listdir(dirname)

    @inprocess.setter
    def inprocess(self, value):
        # İşleme başlansın isteniyorsa..
        if value:
            subprocess.Popen([

                # Python konumu
                sys.executable,

                # Script konumu
                dirname,

                # Parametre
                "-p"
            ])

        # İşlem bitirilsin isteniyorsa
        elif self.inprocess:
            os.remove(PATH_INPROCESS)

    @property
    def result(self) -> dict:
        """Sonuçları çağır.
        :return { IP: { "MAC": MAC, "VENDOR": VENDOR}, ... }
        """
        if RESULTS not in os.listdir(dirname):
            return {}
        with open(PATH_RESULTS, "r") as f:
            result = json.load(f)
            return result

    @result.setter
    def result(self, data):
        """Sonuçları kaydet"""

        # Veri girildiyse veriyi dosyaya yaz.
        if data:
            with open(PATH_RESULTS, "w") as f:
                json.dump(data, f)

        # Veri girilmediyse ve dosyada varsa, dosyayı sil
        elif self.result:
            os.remove(PATH_RESULTS)

        # Tarama işleminin bittiğini kaydet
        self.inprocess = False

    @staticmethod
    def devices(only_esp=False):
        """Ağda bulunan cihazları döndürür

        :param only_esp: bool: Sadece ESPressif Cihazlarını Döndür
        :return list: [ ("IP", "MAC", "VENDOR"), (...) ... ]
        """
        data = tarag.result
        if only_esp:
            for i in data.copy():
                if not data[i].get(VENDOR, "").lower().startswith("espressif"):
                    data.pop(i)

        return [(ip, data[ip].get(MAC), data[ip].get(VENDOR)) for ip in data]

    def wait(self, timeout=20) -> bool:
        """İşlem bitene kadar bekle.
        :param timeout: int: Zaman aşımı. Bu kadar bekledikten sonra hala işlem bitmediyse daha bekleme
        :return bool: True -> İşlem bitti
                      False-> Zaman aşımı
        """
        # 1 sn'lik bekleme süresi ekliyoruz. Böylece __main__.py başlayıp INPROCESS dosyasını oluşturabilir.
        time.sleep(1)

        # timeout'u sorgulama için başlangıç zamanı kaydedilir.
        start_t = time.time()

        while self.inprocess:

            # zaman aşımı olduysa işlemi bitir
            if time.time() - start_t > timeout:
                return False

        return True


# Diğer modüllerden işlemler bu değişken üzerinden yapılır.
tarag = TarAg()
