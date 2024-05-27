# Můj závěrečný projekt PRG 2023/2024
Toto je můj výstupní projekt ze třetího ročníku v Python

Plánuji udělat hru za pomocí knihovny Pygame.
Jako své výchozí IDE jsem zvolil PyCharm.

## Deník
### Update 1 (4 hodiny)

Zvolil jsem si nové IDE, se kterým mám nulové zkušenosti na doporučení spolužáka.

Založil jsem si PyCharm účet a seznámil se s jeho vývojovým prostředí.

Svůj PyCharm jsem propojil s Githubem, vytvořil a přejmenoval herní okno, vyrenderoval jsem si 
první mrak, který se ovládá pomocí šípek. 

Dále jsem se naučil jak fungují "kolize". Udělal jsem si obdélník, přes který projížděl výše zmíněný mrak, když na něj najel, změnila se barva toho detekčního obdelníka.

### Update 2 (2 hodiny)

Založil jsem soubor entities, díky kterému se postavička pohybuje doleva a doprava. 

V souboru utils načítám obrázky ze složky data a nasledných podsložek.  

Založil jsem soubor tutorial, kde ukládám všechny "pomocné" kódy, které mi pomáhaly otestovat různé funkce v programu např. kolize.

### Update 3 (2 hodiny)

Založil jsem soubor tilemap ve kterém renderuji ze složky ninjagame/data/images/tiles, které načítám pomocí souboru utils, konkrétně funkce load_images().

Vytřídil jsem a uklidil v samotné složce, dal souborům a složkám smysluplné názvy.  

### Update 4 (1 hodina)

Začaly se kolem ninjy vytvářet imaginární obdelníčky, které kontrolují kolizi s podlahou (to způsobí, že se nepropadnu do země), či se stěnou (neprojdu zdí), každá kolize funguje na principu obelníček překryje obdelníček a něco se stane.

Nabindoval jsem dále skákání (zatím infinity) na šipku nahoru, abych mohl otestovat kolize shora a zdola. 

Nastavil jsem padání na max rychlost 5, každý frame se postupně zvyšuje rychlost, kterou panáček padá až na max hodnotu. (velocity)

### Update 5 (1 hodina)

Naučil jsem se s kamerou, chytá se na panáčka, ovšem se pohybuje pomaleji (vytváří efekt rychlosti), když se zastavím vycentruje mi panáčka.

Do pozadí jsem dal background.png

Vytvořil jsem soubor clouds.py, kde se mi vytváří 16 náhgodných mraků, které jsou v loopu, díky modulu, tudíž vždy zajedou vpravo a objeví se vlevo a naopak.

### Update 6 (1 hodina)

Stáhl jsem Pycharm i na jiný počítač a naučil se více pracovat s Githubem (klonovat, pull, push...)

Optimalizoval jsem renderování pixelů, aktuálně se mi renderují jen pixely, co jsou viditelné na obrazovce, pixely mimo obrazovku vůbec nerenderuji a hra je díky tomuto plynulejší.

### Update 7 (2 hodiny)

Nastudoval jsem si princip animací, jejich délku trvání, flipování podle osy X (jestli běžíme vlevo, či vpravo), že potřebujeme "rezervovat" větší místo pro frame běžícího panáčka, protože má nohy více do šířky.

Přidal jsem si logiku animací pro ninju, pokud je ve vzduchu tak má animaci skoku, pokud není ve vzduchu ale pohybuje se po ose X, tak má animaci běhu, pokud nedělá ani jedno z toho, tak nemá animaci žádnou.