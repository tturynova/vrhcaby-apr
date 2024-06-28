from herni_kamen import *


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