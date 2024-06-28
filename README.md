# vrhcaby-apr
Python implementace deskové hry jako seminární práce.

# Zadání seminární práce KI/(K)APR2 LS 2023
Vytvořte implementaci hry vrhcáby (eng. backgammon), která podporuje hru dvou hráčů či hru proti jednoduché umělé inteligenci.


----------░V░R░H░C░Á░B░Y░----------
### Povinně implementovaná funkčnost:
generování hodu kostkami <br />
výpis všech možných tahů hráče<br />
jednoduchá umělá inteligence, která náhodně volí jeden z platných tahů<br />
trasování chodu každého jednotlivého kamene _(od vstupu z baru po vyhození/vyvedení) - herní pole se chovají jako zásobník_ <br />
uložení a obnova stavu hry _(s návrhem vlastního JSON formátu pro uložení)_ <br />

### Co musí zobrazovat výpis na standartním vstupu:
výsledky hodů kostkami <br />
pozice všech kamenů na desce (včetně těch "na baru") <br />
stručný komentář toho, co se ve hře událo a nemusí být zřejmé ze zobrazení na desce _(kámen vstoupil do hry, byl "vyhozen", opustil hru, hráč nemůže hrát tj. ani házet, pod.)_ <br />
počet vyvedených kamenů <br />
po výhře typ výhry <br />
po ukončení se zobrazí statistika o všech kamenech ve hře (zvlášť pro bílého a černého), například:
- počet kamenů vyhozených, vyvedených a opuštěných
- průměrná životnost kamene v tazích

### Implementované třídy:
Hra _(Herní deska)_ <br />
- HerníPole _(modifikovaný zásobník, lze vkládat jen kameny stejných barev)_
- Dvojkostka _(vrací seznam možných dvojic či čtveřic)_
- Bar _(továrna na herní kameny, s řízenou produkcí)_
- Herní kámen _(s pamětí, kde se postupně nacházel)_

Hráč
- KonzolovýHráč
- AiHráč

## Ukázky ze hry
- Nabídka na začátku hry<br />
![Startovací nabídka hry](https://github.com/tturynova/vrhcaby-apr/blob/main/vrhcaby_menu.png)
- Průběh hry - lze vidět kámen v baru<br />
![Průběh hry (AiHráč proti AiHráči)](https://github.com/tturynova/vrhcaby-apr/blob/main/vrhcaby_hra.png)
- Statistika na konci hry - vyvedené, vyhozené a opuštěné kameny<br />
![Statistika na konci hry (ukázková)](https://github.com/tturynova/vrhcaby-apr/blob/main/vrhcaby_statistika.png)


