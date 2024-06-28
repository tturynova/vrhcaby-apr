class HerniKamen:
    def __init__(self, symbol):
        self.symbol = symbol
        self.trasa = []

    def zaznamenej_pozici(self, pozice):
        self.trasa.append(pozice)

    def __str__(self):
        return self.symbol