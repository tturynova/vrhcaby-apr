import random


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