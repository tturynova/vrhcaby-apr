import random
import json
import os


bold = "\033[1m"
normal = "\033[0m"


class HerniKamen:
    def __init__(self, symbol):
        self.symbol = symbol
        self.trasa = []

    def zaznamenej_pozici(self, pozice):
        self.trasa.append(pozice)

    def __str__(self):
        return self.symbol


class Bar:
    def __init__(self):
        self.kameny = []

    def pridej_kamen(self, symbol):
        kamen = HerniKamen(symbol=symbol)
        self.kameny.append(kamen)
        print(f"Kámen {symbol} byl přidán do baru.")

    def odeber_kamen(self, symbol):
        if self.kameny:
            return self.kameny.pop()
        return None

    def vrat_pocet_kamenu(self):
        return len(self.kameny)

    def __str__(self):
        return str([str(kamen) for kamen in self.kameny])
    

class Dvojkostka:
    def __init__(self):
        self.mozne_hody = [1, 2, 3, 4, 5, 6]

    def hod(self):
        hod1 = random.randint(1, 6)
        hod2 = random.randint(1, 6)
        if hod1 == hod2:
            return [hod1] * 4
        else: 
            return [hod1, hod2]


class HerniPole:
    def __init__(self, hra):
        self.pole = [0] * 24
        self.hra = hra
        self.bar_dict = self.hra.bar_dict
        self.vyvedene_kameny = {"X": 0, "O": 0}
        hodnoty = [2, 5, 3, 5]
        for x in range(4):
            limit = [0,5] if x < 2 else [6,11]
            bod = self.vygeneruj_bod(limit)
            self.pole[bod] = hodnoty[x]
            self.pole[23 - bod] = - hodnoty[x]

    def vygeneruj_bod(self, limit): #nalezení náhodného volného bodu aneb kam rozmístit kameny
        rand = random.randint(limit[0], limit[1])
        while self.pole[rand] != 0:
            rand = self.vygeneruj_bod(limit)
        return rand

    def vypis_pole(self):
        vertical_space = max(map(abs, self.pole))
        start = 11
        end = -1
        step = 1
        start2 = 0
        end2 = vertical_space
        border = 5
        output = []
        output.append(" 12 11 10  9  8  7     6  5  4  3  2  1")
        output.append("╔═══════════════════╤════════════════════╗")
        for j in range(2):
            for i in range(start2, end2, step):
                line = "║ "
                for index in range(start, end, -step):
                    if index == border:
                        line += "│  "
                    if abs(self.pole[index]) > i:
                        if self.pole[index] > 0:
                            line += "X  "
                        elif self.pole[index] < 0:
                            line += "O  "
                    else:
                        line += "∙  "
                line += "║"
                output.append(line)
            if j == 0:
                output.append("║                   │                    ║")
            start = 12
            end = 24
            step = -1
            start2 = vertical_space - 1
            end2 = -1
            border = 18
        output.append("╚═══════════════════╧════════════════════╝")
        output.append(" 13 14 15 16 17 18    19 20 21 22 23 24")
        return "\n".join(output)

    def je_povoleny_tah(self, tah, symbol):
        if len(tah) != 2: #pokud nemá vstup dvě hodnoty, nemůže být povoleným tahem
            return False 

        prvni_pozice, druha_pozice = tah
        if prvni_pozice == 0: #kontroluje, zda je tah začíná z baru
            if symbol == "X" and 1 <= druha_pozice <= 24 and self.pole[druha_pozice - 1] >= -1:
                return True
            elif symbol == "O" and 1 <= druha_pozice <= 24 and self.pole[24 - druha_pozice] <= 1:
                return True
            return False
    
        elif druha_pozice == 0: #kontroluje, zda tah umožňuje hráčovi vyvést kámen z herní desky
            if symbol == "X" and 1 <= prvni_pozice <= 24 and self.pole[prvni_pozice - 1] > 0:
                return True
            elif symbol == "O" and 1 <= prvni_pozice <= 24 and self.pole[24 - prvni_pozice] < 0:
                return True
            return False
        
        elif prvni_pozice <= 24 and druha_pozice <= 24: #kontroluje platnost tahů mezi dvěmi pozicemi na herní desce
            if prvni_pozice < 1 or druha_pozice < 1:
                return False

            znamenko = 1 if symbol == "X" else -1
            if self.pole[prvni_pozice - 1] * znamenko > 0 and self.pole[druha_pozice - 1] * znamenko >= -1:
                return True

            return False

        return False   

    def proved_tah(self, tah, hrac):
        prvni_pozice, druha_pozice = tah
        print(f"Provedení tahu: {tah} hráčem {hrac.symbol}")

        if prvni_pozice == 0: #tah začíná v baru
            if hrac.symbol == "X":
                pozice = druha_pozice - 1
            else:
                pozice = 24 - druha_pozice

            print(f"Pozice pro tah z baru: {pozice+1}")

            if hrac.symbol == "X": 
                if self.pole[pozice] == -1:
                    self.pole[pozice] = 1
                    self.hra.bar_dict["O"].pridej_kamen("O") #pozice byla obsazena kamenem O a hráč X ji zabral → kámen O je vyhozen ze hry
                else:
                    self.pole[pozice] += 1
            else:
                if self.pole[pozice] == 1:
                    self.pole[pozice] = -1
                    self.hra.bar_dict["X"].pridej_kamen("X") #to samé co výše, ale opačně
                else:
                    self.pole[pozice] -= 1

            self.hra.bar_dict[hrac.symbol].odeber_kamen(hrac.symbol) #aktualizace baru po tom co hráč vrací kámen zpět do hry

        elif druha_pozice == 0: #vyhazování kamene ze hry
            if hrac.symbol == "X":
                pozice = prvni_pozice - 1
            else:
                pozice = 24 - prvni_pozice

            print(f"Tah do baru z pozice {pozice+1}.")

            if hrac.symbol == "X":
                if self.pole[pozice] > 0:
                    self.pole[pozice] -= 1
                    self.vyvedene_kameny["X"] += 1
            else:
                if self.pole[pozice] < 0:
                    self.pole[pozice] += 1
                    self.vyvedene_kameny["O"] += 1

        else: #tah mezi dvěma pozicemi na herní desce
            prvni_pozice -= 1
            druha_pozice -= 1

            if hrac.symbol == "X":
                if self.pole[prvni_pozice] > 0 and self.pole[druha_pozice] >= -1:
                    self.pole[prvni_pozice] -= 1
                    if self.pole[druha_pozice] == -1:
                        self.pole[druha_pozice] = 1
                        self.hra.bar_dict["O"].pridej_kamen("O")
                    else:
                        self.pole[druha_pozice] += 1
            else:
                if self.pole[prvni_pozice] < 0 and self.pole[druha_pozice] <= 1:
                    self.pole[prvni_pozice] += 1
                    if self.pole[druha_pozice] == 1:
                        self.pole[druha_pozice] = -1
                        self.hra.bar_dict["X"].pridej_kamen("X")
                    else:
                        self.pole[druha_pozice] -= 1

        if self.hra.bar_dict[hrac.symbol].kameny: #kontrola, zda bar hráče obsahuje nějaké kameny
            self.hra.bar_dict[hrac.symbol].kameny[-1].zaznamenej_pozici(druha_pozice)



    def mozne_tahy(self, kostky, symbol):
        tahy = set()
        znamenko = 1 if symbol == "X" else -1

        #kontrola, zda jsou v baru nějaké kameny a je možné je vtáhnout zpět do hry
        if self.hra.bar_dict[symbol].vrat_pocet_kamenu() > 0:
            for hod in kostky:
                if symbol == "X" and self.pole[hod - 1] >= -1:
                    tahy.add((0, hod))
                elif symbol == "O" and self.pole[24 - hod] <= 1:
                    tahy.add((0, hod))
        
        #v baru nejsou žádné kameny, tak se provádí standardní tahy na desce
        else:
            for hod in kostky:
                for pozice in range(24):
                    if self.pole[pozice] * znamenko > 0: #znaménko značí +1 (směr 0-24) nebo -1 (směr 24-0)
                        nova_pozice = pozice + hod * znamenko
                        if 0 <= nova_pozice < 24 and self.pole[nova_pozice] * znamenko >= -1:
                            tahy.add((pozice + 1, nova_pozice + 1))

        return list(tahy)

    def je_konec_hry(self): #kontrola, zda jsou všechny kameny hráčů v domácích kvadrantech, kde mají být a zároveň zda jsou vyvedené
        if all(kamen >= 0 for kamen in self.pole[:18]) and self.vyvedene_kameny["X"] == 15: 
            return True 
        if all(kamen <= 0 for kamen in self.pole[6:]) and self.vyvedene_kameny["O"] == 15:
            return True
        return False
    
    def stav(self):
        return self.vypis_pole()

def ziskej_symbol_od_hrace():
    while True:
        symbol = input("Vyberte si symbol (X nebo O): ").upper()
        if symbol == "X":
            return "X", "O"
        elif symbol == "O":
            return "O", "X"
        else:
            print("Neplatný symbol. Zadejte prosím X nebo O.")

        
class Hra:
    def __init__(self, hrac1=None, hrac2=None, na_tahu=None):
        self.hrac1 = hrac1
        self.hrac2 = hrac2
        self.symbol_hrac1 = hrac1.symbol if hrac1 else None
        self.symbol_hrac2 = hrac2.symbol if hrac2 else None 
        self.dvojkostka = Dvojkostka()
        self.bar_dict = {
            "X": Bar(),
            "O": Bar()
        }
        self.herni_pole = HerniPole(self)
        self.konec_hry = False
        self.vitez = None
        self.na_tahu = na_tahu
        self.hra_ulozena = False
        self.tahy_provedene_celkem = 0 #počítá tahy provedené celkem včetně tahů, které nejsou povolené
        self.tahy_od_obnoveni = 0 #počítá tahy provedené po obnovení hry


    def urci_prvniho_hrace(self):
        while True:
            print("")
            print("Nyní se určí, kdo bude hru začínat.")
            input(f"{self.hrac1.jmeno}, stiskněte Enter pro hod kostkou.")
            hod_hrac1 = random.randint(1, 6)
            print(f"{self.hrac1.jmeno} hodil: {hod_hrac1}")
            print("")

            if isinstance(self.hrac2, AiHrac):
                print(f"{self.hrac2.jmeno} AiHráč hází kostkou.")
                hod_hrac2 = random.randint(1, 6)
                print(f"{self.hrac2.jmeno} hodil: {hod_hrac2}")
            else:
                input(f"{self.hrac2.jmeno}, stiskněte Enter pro hod kostkou.")
                hod_hrac2 = random.randint(1, 6)
                print(f"{self.hrac2.jmeno} hodil: {hod_hrac2}")
            print("")

            if hod_hrac1 != hod_hrac2:
                break

            print("Shoda! Hráči hází znovu.")

        if hod_hrac1 > hod_hrac2:
            self.na_tahu = self.hrac1
        else:
            self.na_tahu = self.hrac2

        print(f"Na tahu je {self.na_tahu.jmeno} a hra začíná.")


    def hraj(self, hra_obnovena=False):
        while not self.konec_hry:
            hody_kostkou = self.dvojkostka.hod()
            pocet_tahu = 4 if len(set(hody_kostkou)) == 1 else 2
            tahy_provedene = 0
            while tahy_provedene < pocet_tahu:
                if self.hra_ulozena:
                    break
                print("")
                print("··············· HERNÍ DESKA ················")
                print(f"Bar {self.hrac2.symbol} (hráč 2): ", self.bar_dict[self.hrac2.symbol])
                print(self.herni_pole.vypis_pole())
                print(f"Bar {self.hrac1.symbol} (hráč 1): ", self.bar_dict[self.hrac1.symbol])
                print("··············· HERNÍ DESKA ················")
                print("")
                print(bold + f"{self.na_tahu.jmeno} hodil kostkami: " + str(hody_kostkou) + normal)
                tah_hrace = self.na_tahu.tahni(self.herni_pole, hody_kostkou)
                if tah_hrace:
                    if tah_hrace == "q":
                        print("Hra byla ukončena hráčem. Postup ve hře nebyl uložen.")
                        self.konec_hry = True
                        self.hra_ulozena = True
                        break
                    self.herni_pole.proved_tah(tah_hrace, self.na_tahu)
                    hodnota_tahu = abs(tah_hrace[1] - tah_hrace[0])

                    if hodnota_tahu in hody_kostkou:
                        hody_kostkou.remove(hodnota_tahu)
                    tahy_provedene += 1
                    self.tahy_provedene_celkem += 1
                    self.tahy_od_obnoveni += 1

                    if self.herni_pole.je_konec_hry():
                        self.konec_hry = True
                        self.vitez = self.na_tahu
                        break

            if self.tahy_od_obnoveni >= 10 and self.tahy_od_obnoveni % 10 == 0:
                self.uloz_a_obnov_hru()

            if self.na_tahu == self.hrac1:
                self.na_tahu = self.hrac2
            else:
                self.na_tahu = self.hrac1

        if not self.hra_ulozena:
            self.zobraz_vysledky()


    def zobraz_vysledky(self):
        if self.vitez:
            print('------------░K░O░N░E░C░-░H░R░Y░------------')
            print("Vítězem je: ", self.vitez.jmeno)
            print(self.herni_pole.stav())
            print("Typ výhry: ", self.typ_vyhry())
    

    def typ_vyhry(self):
        if self.herni_pole.vyvedene_kameny[self.vitez.symbol] == 15:
            if self.herni_pole.vyvedene_kameny[self.protihrac(self.vitez).symbol] == 0:
                if all(kamen == 0 for kamen in self.herni_pole.pole):
                    return "Backgammon"
                return "Gammon"
            return "Normální výhra" 
        return "Nedokončená hra"


    def protihrac(self, hrac):
        return self.hrac1 if hrac == self.hrac2 else self.hrac2


    def zobraz_vysledky(self):
        if self.vitez:
            print('------------░K░O░N░E░C░-░H░R░Y░------------')
            print("Vítězem je: ", self.vitez.jmeno)
            print(self.herni_pole.stav())
        self.zobraz_statistiku()


    def zobraz_statistiku(self):
        statistika = {
            "X": {"vyhozené": 0, "vyvedené": 0, "opuštěné": 0},
            "O": {"vyhozené": 0, "vyvedené": 0, "opuštěné": 0}
        }

        #počet vyvedených kamenů
        statistika["X"]["vyvedené"] = self.herni_pole.vyvedene_kameny["X"]
        statistika["O"]["vyvedené"] = self.herni_pole.vyvedene_kameny["O"]

        #počet vyhozených kamenů
        statistika["X"]["vyhozené"] = len(self.bar_dict["X"].kameny)
        statistika["O"]["vyhozené"] = len(self.bar_dict["O"].kameny)

        #počet kamenů, které nejsou na baru ani vyvedené
        statistika["X"]["opuštěné"] = 15 - (statistika["X"]["vyvedené"] + statistika["X"]["vyhozené"])
        statistika["O"]["opuštěné"] = 15 - (statistika["O"]["vyvedené"] + statistika["O"]["vyhozené"])

        print("------------░S░T░A░T░I░S░T░I░K░A░------------")
        print("Statistika pro hráče X (černé kameny):")
        print(f"Vyhozené kameny: {statistika['X']['vyhozené']}")
        print(f"Vyvedené kameny: {statistika['X']['vyvedené']}")
        print(f"Opuštěné kameny: {statistika['X']['opuštěné']}")
        print("")
        print("Statistika pro hráče O (bílé kameny):")
        print(f"Vyhozené kameny: {statistika['O']['vyhozené']}")
        print(f"Vyvedené kameny: {statistika['O']['vyvedené']}")
        print(f"Opuštěné kameny: {statistika['O']['opuštěné']}")
        print("---------------------------------------------")


    def uloz_stav(self, soubor): #ukládání do JSON
        stav = {
            "hrac1": self.hrac1.jmeno,
            "hrac2": self.hrac2.jmeno,
            "symbol_hrac1": self.hrac1.symbol,
            "symbol_hrac2": self.hrac2.symbol,
            "na_tahu": self.na_tahu.jmeno,
            "pole": self.herni_pole.pole,
            "bar_X": [str(kamen) for kamen in self.bar_dict["X"].kameny],
            "bar_O": [str(kamen) for kamen in self.bar_dict["O"].kameny],
            "vyvedene_kameny": self.herni_pole.vyvedene_kameny
        }
        with open(soubor, 'w') as f:
            json.dump(stav, f)
        print("Hra byla úspěšně uložena.")


    def obnov_stav(self, soubor):
        with open(soubor, 'r') as f:
            stav = json.load(f)

        self.hrac1 = KonzolovyHrac(stav["hrac1"], stav["symbol_hrac1"])
        self.hrac2 = AiHrac(stav["hrac2"], stav["symbol_hrac2"])
        self.na_tahu = self.hrac1 if stav["na_tahu"] == stav["hrac1"] else self.hrac2
        self.herni_pole.pole = stav["pole"]
        self.bar_dict["X"].kameny = [HerniKamen("X") for _ in stav["bar_X"]]
        self.bar_dict["O"].kameny = [HerniKamen("O") for _ in stav["bar_O"]]
        self.herni_pole.vyvedene_kameny = stav["vyvedene_kameny"]


    #zeptá se hráče po 10 tazích (= dá se změnit v metodě hraj) zda chce ve hře pokračovat nebo ji chce uložit.
    def uloz_a_obnov_hru(self):
        if self.tahy_od_obnoveni >= 10:
            while True:
                print("")
                volba = input("Chcete uložit hru a pokračovat příště? (1 = Ano, 2 = Ne): ")
                if volba == "1":
                    print("")
                    print("... ukládám hru ...")
                    print("")
                    self.uloz_stav("ulozena_hra.json")
                    self.hra_ulozena = True
                    self.konec_hry = True
                    break
                elif volba == "2":
                    print("")
                    print("Hra nebyla uložena.")
                    print("")
                    break
                else:
                    print("Neplatná volba. Zadejte 1 nebo 2.")


class Hrac:
    def __init__(self, jmeno, symbol):
        self.jmeno = jmeno
        self.symbol = symbol

    def tahni(self, herni_pole, hody_kostkou):
        mozne_tahy = herni_pole.mozne_tahy(hody_kostkou, self.symbol)
        if mozne_tahy:
            return random.choice(mozne_tahy)
        return None

class AiHrac(Hrac):
    def tahni(self, herni_pole, hody_kostkou):
        mozne_tahy = herni_pole.mozne_tahy(hody_kostkou, self.symbol)
        if mozne_tahy:
            return random.choice(mozne_tahy)
        return None

class KonzolovyHrac(Hrac):
    def tahni(self, herni_pole, hody_kostkou):
        mozne_tahy = herni_pole.mozne_tahy(hody_kostkou, self.symbol)
        print(f"Možné tahy: {mozne_tahy}")
        if mozne_tahy:
            while True:
                try:
                    print("")
                    tah = input("Zadejte tah (ve formátu 'start cíl' nebo 'q' pro ukončení hry'): ")
                    if tah.lower() == "q":
                        return "q"
                    start, cil = map(int, tah.split(' '))
                    if (start, cil) not in mozne_tahy:
                        raise ValueError
                    return (start, cil)
                except ValueError:
                    print("Neplatný tah, zkus to znovu.")
        return None
    

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