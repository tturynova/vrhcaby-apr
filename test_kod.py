import random 

class Hra:
    def __init__(self, hrac1, hrac2):
        self.hrac1 = hrac1
        self.hrac2 = hrac2
        self.herni_pole = HerniPole()
        self.dvojkostka = Dvojkostka()
        self.bar = Bar()
        self.konec_hry = False
        self.vitez = None

    def hraj(self):
        while not self.konec_hry:
            tah_hrace1 = self.hrac1.tahni(self.herni_pole, self.dvojkostka, self.bar)
            self.herni_pole.proved_tah(tah_hrace1)
            if self.herni_pole.je_konec_hry():
                self.konec_hry = True
                self.vitez = self.hrac1
                break
            tah_hrace2 = self.hrac2.tahni(self.herni_pole, self.dvojkostka, self.bar)
            self.herni_pole.proved_tah(tah_hrace2)
            if self.herni_pole.je_konec_hry():
                self.konec_hry = True
                self.vitez = self.hrac2
                break

        self.zobraz_vysledky()
    
    def zobraz_vysledky(self):
        print("Vítěz: ", self.vitez.jmeno)
        print("Stav herního pole: ", self.herni_pole.stav())

class HerniPole:
    def __init__(self):
        self.pole = [0] * 24
        self.pole[0] = 2
        self.pole[5] = -5
        self.pole[7] = -3
        self.pole[11] = 5
        self.pole[12] = -5
        self.pole[16] = 3
        self.pole[18] = 5
        self.pole[23] = -2
        self.bar = Bar()
     
    def vypis_pole(self):
        print("13 14 15 16 17 18 | 19 20 21 22 23 24")
        print("------------------------------------")
        for i in range(18, 12, -6):
            print(i+1, end=" ")
            for j in range(5): 
                print("|", end=" ")
                if 0 <= 18+j+i <= 23 and self.pole[18+j+i] > 0:
                    print("O", end=" ")
                elif 0 >= 18+j+i >= 23 and self.pole[18+j+i] < 0:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            print("|", end=" ")
            print(i+6)
        print("------------------------------------")
        print("12 11 10  9  8  7 |  6  5  4  3  2  1")   

    def proved_tah(self, tah):
        if not self.je_povoleny_tah(tah):
            raise ValueError("Neplatný tah")
        if self.bar.vrat_pocet_kamenu() > 0:
            pozice = tah[1] - 1
            self.pole[pozice] += 1
            self.bar.odeber_kamen(self.hraci[self.na_tahu].barva)
        else:
            pozice_od = tah[0]
            pozice_do = tah[1]
            if self.pole[pozice_od] <= 0:
                raise ValueError("Neplatný tah")
            self.pole[pozice_od] -= 1
            if self.pole[pozice_do] == -1:
                self.pole[pozice_do] = 1
                self.bar.pridej_kamen(self.hraci[self.na_tahu].barva)
            else:
                self.pole[pozice_do] += 1

        self.na_tahu = (self.na_tahu + 1) % 2
                      
    def mozne_tahy(self, dvojkostka, bar):
        tahy = []
        for hod in dvojkostka.hod():
            if bar.vrat_pocet_kamenu() > 0:
                if self.pole[hod - 1] >= -1:
                    tahy.append((0, hod))
        else:
            for pozice in range(24):
                if self.pole[pozice] > 0:
                    nova_pozice = pozice + hod
                    if nova_pozice < 24 and self.pole[nova_pozice] >= -1:
                        tahy.append((pozice, nova_pozice))
        return tahy

    def je_povoleny_tah(self, tah):
        if len(tah) == 0:
            return False
        if self.bar.vrat_pocet_kamenu() > 0:
            return tah[0] == 0 or tah[0] == 1
        for pozice in range(24):
            if self.pole[pozice] > 0:
                nova_pozice = pozice + tah[0]
                if nova_pozice < 24 and self.pole[nova_pozice] >= -1:
                    return True
        return False

    def je_konec_hry(self):
        pocet_kamenu_v_cili = sum(self.pole[18:])
        if pocet_kamenu_v_cili == 15:
            return True
        return all(kamen <= 0 for kamen in self.pole[:18])
    
class Dvojkostka:
    def __init__(self):
        self.mozne_hody = [1, 2, 3, 4, 5, 6]

    def hod(self):
        hod1 = random.randint(1, 6)
        hod2 = random.randint(1, 6)
        if hod1 == hod2:
            return [hod1, hod1, hod1, hod1]
        else: 
            return [hod1, hod2]
        
class Bar:
    def __init__(self):
        self.kameny = []
    
    def pridej_kamen(self, barva):
        self.kameny.append(barva)
    
    def odeber_kamen(self, barva):
        if barva in self.kameny:
            self.kameny.remove(barva)
    
    def vrat_pocet_kamenu(self):
        return len(self.kameny)
    
    def je_prazdny(self):
        return len(self.kameny) == 0

class HerniKamen:
    def __init__(self, pozice=-1, barva=''):
        self.pozice = pozice
        self.barva = barva
        
    def nastav_pozici(self, pozice):
        self.pozice = pozice

    def nastav_barvu(self, barva):
        self.barva = barva

class KonzolovyHrac:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def tahni(self, herni_pole, dvojkostka, bar):
        while True:
            try:
                hod = input(f"{self.jmeno}, zadej svůj hod (oddělený mezerou): ")
                hod1, hod2 = map(int, hod.split())
                if hod1 not in dvojkostka.mozne_hody or hod2 not in dvojkostka.mozne_hody:
                    raise ValueError
                tah = (hod1, hod2)
                if bar.vrat_pocet_kamenu() > 0 and not herni_pole.je_povoleny_tah(tah, bar):
                    raise ValueError
                elif bar.vrat_pocet_kamenu() == 0 and not herni_pole.je_povoleny_tah(tah):
                    raise ValueError
                else:
                    return tah
            except ValueError:
                print("Neplatný tah, zkus to znovu.")

class AiHrac:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def tahni(self, herni_pole, dvojkostka, bar):
        mozne_tahy = herni_pole.mozne_tahy(dvojkostka, bar)
        if not mozne_tahy:
            return None
        else:
            return self.zvol_tah(mozne_tahy)

    def zvol_tah(self, mozne_tahy):
        return mozne_tahy[0]

hrac1 = Hrac("Hráč 1", "O")
hrac2 = AiHrac("Ai", "X")

hra = Hra(hrac1, hrac2)
hra.hraj()
