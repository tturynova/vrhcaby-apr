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
    
    def pridej_kamen(self, color):
        self.kameny.append(color)
    
    def odeber_kamen(self, color):
        if color in self.kameny:
            self.kameny.remove(color)
    
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

