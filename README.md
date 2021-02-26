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
    
![tarag](https://user-images.githubusercontent.com/73780835/109354921-8f9cb380-788f-11eb-95f4-0ca277732ef2.jpg)
