import random


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