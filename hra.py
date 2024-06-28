import random
import json


from herni_kamen import *
from bar import *
from dvojkostka import *
from herni_pole import *
from hrac import *


bold = "\033[1m"
normal = "\033[0m"



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