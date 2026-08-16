import math

class OrbitVarCalculator:

    @staticmethod
    def calculate_G(Sn, Rn):
        if Sn + Rn != 0:
            return (Sn + Rn) / 70
        else:
            return 0

    @staticmethod
    def calculate_M(Sn, Rn):
        if Sn + Rn != 0:
            return (1 - 2 * math.fabs((Sn / (Sn + Rn)) - 0.5))
        else:
            return 0

    @staticmethod
    def calculate_I(G):
        if G >= 17.14:
            return True
        else:
            return False

class SolarVarCalculator:

    @staticmethod
    def calculate_A(m, member_msg_data, k=5):
        N = 0

        for i in member_msg_data:
            N += i["messages"]

        M = 7 * k * (m ** (1.3))

        if N > (1.5 * M):
            return 1
        else:
            return (N / (1.5 * M))

    @staticmethod
    def calculate_C(member_msg_data):
        result = member_msg_data
        n_list = []
    
        for i in member_msg_data:
            n_list.append(i["messages"])
        
        n_list.sort()
        n_max = n_list[-1]
    
        if n_max == 0:
            return None
    
        for i in n_list:
            if i != 0:
                n_min = i
                break

        if n_min == n_max:
            result[i]["messages"] = 1
        
        for i in range(len(n_list)):
            if n_list[i] == 0:
                result[i]["messages"] = 0
            else:
                C_i = math.log((n_list[i] / n_min), (n_max / n_min))
                result[i]["messages"] = C_i

        return result

    @staticmethod
    def calculate_D(m, m_max):
        return (m / m_max)

    @staticmethod
    def calculate_E(member_msg_data):
        n_list = []
        for i in member_msg_data:
            n_list.append(i["messages"])

        mean = math.fsum(n_list) / len(n_list)

        square_mean_differences = []
        for i in n_list:
            square_mean_differences.append(math.pow(math.abs(i - mean), 2))

        variance = math.fsum(square_mean_differences) / len(n_list)

        standard_deviation = variance ** 0.5

        max_deviation = (max(n_list) - min(n_list)) / 2

        if max_deviation == 0:
            return None
        else:
            return (1 - math.log(standard_deviation + 1, max_deviation + 1))
    

        


