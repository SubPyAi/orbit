import math
import time

class VarCalculator:

    def calculate_G(Sn, Rn):
        if Sn + Rn != 0:
            return (Sn + Rn) / 70
        else:
            return 0

    def calculate_M(Sn, Rn):
        if Sn + Rn != 0:
            return (1 - 2 * math.fabs((Sn / (Sn + Rn)) - 0.5))
        else:
            return 0

    def calculate_I(G):
        if G >= 17.14:
            return True
        else:
            return False

