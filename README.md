# vrhcaby-apr
Python implementace deskové hry jako seminární práce.

#Zadání seminární práce KI/(K)APR2 LS 2023
Vytvořte implementaci hry vrhcáby (eng. backgammon), která podporuje hru dvou hráčů či hru proti jednoduché umělé inteligenci.


----------░V░R░H░C░Á░B░Y░----------
> Povinně implementovaná funkčnost:
>> generování hodu kostkami
>> výpis všech možných tahů hráče
>> jednoduchá umělá inteligence, která náhodně volí jeden z platných tahů
>> trasování chodu každého jednotlivého kamene (od vstupu z baru po vyhození/vyvedení) - herní pole se chovají jako zásobník
>> uložení a obnova stavu hry (s návrhem vlastního JSON formátu pro uložení)

> Co musí zobrazovat výpis na standartním vstupu:
>> výsledky hodů kostkami
>> pozice všech kamenů na desce (včetně těch "na baru")
>> stručný komentář toho, co se ve hře událo a nemusí být zřejmé ze zobrazení na desce (kámen vstoupil do hry, byl "vyhozen", opustil hru, hráč nemůže hrát tj. ani házet, pod.)
>> počet vyvedených kamenů
>> po výhře typ výhry
>> po ukončení se zobrazí statistika o všech kamenech ve hře (zvlášť pro bílého a černého), například:
>>> počet kamenů vyhozených, vyvedených a opuštěných
>>> průměrná životnost kamene v tazích

> Implementované třídy:
>> Hra (Herní deska)
>>> HerníPole (modifikovaný zásobník, lze vkládat jen kameny stejných barev)
>>> Dvojkostka (vrací seznam možných dvojic či čtveřic)
>>> Bar (továrna na herní kameny, s řízenou produkcí)
>>> Herní kámen (s pamětí, kde se postupně nacházel)

>> Hráč
>>> KonzolovýHráč
>>> AiHráč
