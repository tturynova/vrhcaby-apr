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
        self.bily_pole = []
        self.cerne_pole = []
        ...
        
class Dvojkostka:
    def hod(self):
        hod1 = random.randint(1, 6)
        hod2 = random.randint(1, 6)
        if hod1 == hod2:
            return [hod1, hod1, hod1, hod1]
        else:
            return [hod1, hod2]
        
class Bar:
    ...

class HerniKamen:
      def __init__(self, pozice=-1, barva=''):
        self.pozice = pozice
        self.barva = barva
        ...

class Hrac:
    ...

class Hrac:
    ...
