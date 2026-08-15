import math
import time

class VarCalculator:

    def calculate_G(Sn, Rn):
        return (Sn + Rn) / 70

    def calculate_M(Sn, Rn):
        return (1 - 2 * math.fabs((Sn / (Sn + Rn)) - 0.5))

    def calculate_I(G):
        if G >= 17.14:
            return True
        else:
            return False

