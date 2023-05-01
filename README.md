## Zadání seminární práce KI/(K)APR2 LS 2023
Stručný popis zadání:
Vytvořte implementaci hry vrhcáby, která podporuje hru dvou hráčů či hru proti jednoduché umělé inteligenci.

### povinně implementovaná funkčnost:
- generování hodu kostkami
- výpis všech možných tahů hráče
- jednoduchá umělá inteligence, která náhodně volí jeden z platných tahů
- trasování chodu každého jednotlivého kamene (od vstupu z baru po vyhození/vyvedení), herní pole se chovají jako zásobník
- uložení a obnova stavu hry (s návrhem vlastního JSON formátu pro uložení)

### co musí zobrazovat displej (výpis na standardním vstupu)
- výsledky hodů kostkami
- pozice všech kamenů na desce (včetně těch "na baru")
- stručný komentář toho, co se ve hře událo a nemusí být zřejmé ze zobrazení na desce (kámen vstoupil do hry, byl "vyhozen", opustil hru, hráč nemůže hrát tj. ani házet, pod.)
- počet vyvedených kamenů
- po výhře typ výhry
- po ukončení se zobrazí statistika o všech kamenech ve hře (zvlášť pro bílého a černého), například:
  - počet kamenů vyhozených, vyvedených a opuštěných
  - průměrná životnost kamene v tazích

### nepovinná funkčnost:
- GUI rozhraní
- inteligentnější AI

### implementované třídy:
- Hra (Herní deska)
- obsahuje:
  - HerníPole (modifikovaný zásobník, lze vkládat jen kameny stejných barev)
  - Dvojkostka (vrací seznam možných dvojic či čtveřic)
  - Bar (továrna na herní kameny, s řízenou produkcí)
- Herní kámen (s pamětí, kde se postupně nacházel)
- Hráč:
- odvozené třídy:
  - KonzolovýHráč
  - AIHráč
