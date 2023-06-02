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
      for i in range(len(tah)):
        if tah[i] not in Dvojkostka().mozne_hody:
            raise ValueError("Neplatný tah")
        if bar.vrat_pocet_kamenu() > 0 and not self.je_povoleny_tah(tah, bar):
            raise ValueError("Neplatný tah")
        elif bar.vrat_pocet_kamenu() == 0 and not self.je_povoleny_tah(tah):
            raise ValueError("Neplatný tah")
        else:
            self.pole[self.hraci[self.na_tahu].kameny[i].pozice] = 0
            self.pole[self.hraci[self.na_tahu].kameny[i].pozice + tah[i]] += 1
            self.hraci[self.na_tahu].kameny[i].pozice += tah[i]
                    
            if self.hraci[self.na_tahu].kameny[i].pozice == 23:
              self.pole[23] = self.hraci[self.na_tahu].kameny[i].barva
              self.pole[self.hraci[self.na_tahu].kameny[i].pozice] = 0
              self.hraci[self.na_tahu].kameny.remove(self.hraci[self.na_tahu].kameny[i])
              self.hraci[self.na_tahu].pocet_vyhozenych_kamenu += 1
              self.hraci[self.na_tahu].pocet_umistenych_kamenu += 1
              break
                    
            self.na_tahu = (self.na_tahu + 1) % 2


class Dvojkostka:
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
        ...

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

