# Tarag - Network Scanner

Ağdaki cihazları bulur. Herhangi bir bağımlılığı yoktur.


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