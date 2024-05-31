# Můj závěrečný projekt PRG 2023/2024
Toto je můj výstupní projekt ze třetího ročníku v Python.
Jako své výchozí IDE jsem zvolil PyCharm.

Udělal jsem hru, kde ovládáte postavičku malého ninjy, který se snaží zabít všechny nepřátele.
Jeho jedinou zbraní je jeho rychlý ninja DASH, oproti tomu jeho nepřátele na vás budou střílet ze zbraně.
Zvládnete projít všechny tři levely a zneškodnit všechny nepřátele???

## Jak spustit hru
1. Nainstalujte si do svého zařízení Python.
2. V terminále si nainstalujte knihovnu Pygame za pomocí příkazu "pip install pygame".
3. Stáhněte si VŠECHNY soubory hry do jedné složky.
4. Tuto složku otevřete v programovacím IDE dle vaší volby (VS CODE, Pycharm,...).
5. Najdete si soubor game.py a spustíte jej.
6. Zobrazí se vám vyskakovací okno ve kterém by vám měla běžet hra, pokud jste udělali vše správně.

## Ovládání hry
Hra se ovládá úplně jednodušše. 
POHYB - Ninja se pohybuje pomocí šípek, doprava, doleva a skok. 
ÚTOK - Útok neboli tzv.dash se provádí pomocí zmáčknutí klávesy X a šipky, udávající směr, do kterého má ninja zaútočit. Po dobu jeho útoku je nesmrtelný a poté má krátký cooldown, aby nemohl útočit furt.

## Cíl hry
Cílem hry je projít všechny tři připravené levely. Do dalšího levelu se dostanete zabitím všech nepřátel, kteří se budou samozřejmě bránit a budou na vás střílet. Životu máte neomezeně, ovšem když umřete, respawnete se na začátku levelu ve kterém jste umřeli.



## Pracovní deník
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

### Update 8 (2 hodiny)

Začal jsem vytvářet samotnou mapu. Pro tento účel jsem si založil map.json Json je lepší pro prácí se stringami ukládání a zpětné načítání věcí. 

Založil jsem editor.py pro vytváření map, zároveň jsem se naučil inicializovat vstup myši (tlačítka a kolečko) i kombinovat písmena či myš se shiftem. Např. shift + kolečko myši scrolluje mezi variantama blocků. 

### Update 9 (3 hodiny)

Pokračuji ve vytváření editor.py pro vytváření map. 

self.ongrid mi pokládá bloky na "grid", tj. skládá je vedle sebe jako blocky v Minecraftu(používá se primárně pro trávu a kameny), self.offgrid je pokládá , dle přesné polohy myši, mohou to být nepravidelné blocky jako např. stromy či květiny atd...

V souboru tilemap.py jsem udělal autotile. Díky autotilu se mi skupina blocků porovná tak, že nahoře bude tráva a pod ní hlína. Stejně funguje pro kameny. Autotile strašně zjednodušuje tvorbu map.

Udělal jsem particles.py, tento soubor se stará o particly (padající listy). Přidal jsem matiku a nastavil list, aby padal po sinusovce, toto vytváří mnohem reálnější pocit z padajícího listu než umělé násobení random.random() číslem.

### Update 10 (4 hodiny)

Omezil jsem skoky na 1 skok. Po dopadu na zem se vyresetuje a můžete zase skákat. 

Nastavil jsem wall jump a wall slide. Při wall slidu klouže ninja pomaleji než padá normálně ze vzduchu. Může se také odrazit od zdi a skočit tak do určité vzdálenosti.

Nastavil jsem DASH ninji na klávesu X. Zprovoznil jsem samotný dash, posledních 10 framů ninja zpomaluje, prvních 50 framů je "neviditelný". Zároveň těch 10 framů, kdy už ho můžeme vidět a ninja zpomaluje tak probíhá cooldown, abych nemohl dashovat ostošest.

V prvnívh 50 framech, kdy ninja dashuje se mi vytváří tzv. "burst" z černých partuclů.

V posledních 10 framech, kdy brzdí a zastavuje se tak se mi vytvoří 20 náhodných rychlostí a pozic pro spawn stejných černých particlů a toto dělá efekt "splashe", když ninja zastaví.

Script se podívá do map a najde, kam jsem umístil spawnery, poté vyhodnotí jestli to je spawn ninji či enemáka  a spawne je na daných pozicích.

Aby nám enemák nepadal přes okraje tak jsem mu napsala tuto podmínku "pokud je pod enemákem a ze šikma před ním solid tile jde dál, jestli ne, tak se otočí a jde na druhou stranu", fce solid_check soubor tilemap.py

Přidal jsem mu zbraň, která se centruje podle souřadnic enemáka a také flipuje.

### Update 11 (5 hodin)

Přidal jsem projektil, který enemák střílí, když je ninja maximálně na 16 pixelů dleko od něj a na stejné souřadnici Y, zároveň musí být enemák natočen na stranu, kde je ninja.

Projektil zmizí, když narazí do zdi, ninju nebo letí déle než 6 sekund.

Založil jsem spark.py, aby to nebylo jen že střela imploduje, ale mělo to i vizualní efekt.

Při nárazu střely do zdi, se vizuálně "odrazí".

Při trefení ninjy se uděla vizuální "exploze"

Zabití enemáka ninjou je při dashi, udělá se "exploze" stejná jako při zabití ninjy a enemák zmizí.

Když je ninja trefen střelou nebo padá délé než 240 framů (4 sekundy), tak zemře zmizí a level se restartuje od začátku.

Přidal jsem screenshake na místa, kde je to žádoucí (smrt ninjy, enemáka, dash a apod..)

Upravil jsme přechod mezi levely pomocí black screenu, který vizuálně rozdělí 2 levely a zároveň se v něm načte level další.

Zvýraznil jsem frontend hry řekněme lehkým "stínem".

Přidal jsem zvuky na jump, dash, střelu, smrt a v pozadí.

Když člověk hru dohraje zapne se znovu poslední level.
