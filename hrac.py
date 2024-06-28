import random

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