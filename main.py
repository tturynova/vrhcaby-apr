import random
import json
import os

from hra import *
from hrac import *
from herni_kamen import *
from herni_pole import *
from bar import *
from dvojkostka import *


bold = "\033[1m"
normal = "\033[0m"



def main():
    print("----------░V░R░H░C░Á░B░Y░-----------")
    input("Stiskněte Enter pro pokračování dále.")
    print("----------░V░R░H░C░Á░B░Y░-----------")
    print("")
    print("------------- Možnosti -------------")
    print("1. Pravidla hry")
    print("2. Hrát hru s AiHráčem")
    print("3. Hrát proti jinému hráči")
    print("4. Hra AiHráče proti dalšímu AiHráči")
    print("5. Načíst poslední uloženou hru")
    
    while True:
        volba = input("Vyberte možnost (1, 2, 3, 4 nebo 5): ")
        if volba == "1":
            print("----------- Pravidla hry -----------")
            print("1. Cílem je přesunout všechny své kameny do svého domácího kvadrantu a poté je vyvést z desky. Vyhrává první hráč, který vyvede všechny kameny.")
            print("")
            print("2. Deska se skládá z 24 polí, nazývaných body, které jsou rozděleny do čtyř kvadrantů. Každý hráč má svůj domácí a vnější kvadrant.")
            print("")
            print("3. Každý hráč má 15 kamenů. Kameny jsou rozestaveny na desce náhodně v hodnotách [2, 3, 5].")
            print("")
            print("4. Hráči hází dvěma kostkami a mohou přesunout své kameny podle hodnot na kostkách. Pokud hráč hodí dvojici, může použít každý hod dvakrát, tedy celkem čtyři tahy.")
            print("")
            print("5. Hráč může obsadit bod, pokud na něm není více než jeden soupeřův kámen. Pokud hráč přesune svůj kámen na bod s jedním soupeřovým kamenem, je soupeřův kámen je vyhozen a umístěn na bar.")
            print("")
            print("6. Kameny na baru musí být vráceny do hry před jakýmkoli jiným pohybem. Hráč musí hodit kostkami a umístit kámen na odpovídající bod v počátečním kvadrantu.")
            print("")
            print("7. Jakmile má hráč všechny své kameny v domácím kvadrantu, může začít vyvádět kameny z desky. Hráč musí hodit kostkami a vyvést kámen z odpovídajícího bodu.")
            print("")
            print("8. Hra končí, když jeden hráč vyvede všechny své kameny. Tento hráč vyhrává.")
            print("")
            print("------------ Typy výher ------------")
            print("Normální: Hráč vyvede všechny své kameny, zatímco soupeř vyvede některé své kameny. ")
            print("")
            print("Gammon: Hráč vyvede všechny své kameny, zatímco soupeř nevyvede žádné své kameny.")
            print("")
            print("Backgammon: Hráč vyvede všechny své kameny ale všechny kameny soupeře jsou stále na desce. ")
            input("Stiskněte Enter pro návrat do menu.")
            return main() 
        
        elif volba in ["2", "3", "4", "5"]:
            break
        else:
            print("Neplatná volba. Zadejte prosím 1, 2, 3, 4 nebo 5.")


    if volba == "5":
        if os.path.exists("ulozena_hra.json"):
            hra = Hra()
            hra.obnov_stav("ulozena_hra.json")
            hra.hraj(hra_obnovena=True)
            return
        else:
            print("Žádná uložená hra nebyla nalezena.")
            return main()


    symbol_hrac1, symbol_hrac2 = ziskej_symbol_od_hrace()

    
    if volba == "2":
        hrac1 = KonzolovyHrac("Hráč 1", symbol_hrac1)
        hrac2 = AiHrac("Hráč 2", symbol_hrac2)
    elif volba == "3":
        hrac1 = KonzolovyHrac("Hráč 1", symbol_hrac1)
        hrac2 = KonzolovyHrac("Hráč 2", symbol_hrac2)
    elif volba == "4":
        hrac1 = AiHrac("AiHráč 1", symbol_hrac1)
        hrac2 = AiHrac("AiHráč 2", symbol_hrac2)


    hra = Hra(hrac1, hrac2)

    hra.urci_prvniho_hrace()

    hra.hraj()

if __name__ == "__main__":
    main()