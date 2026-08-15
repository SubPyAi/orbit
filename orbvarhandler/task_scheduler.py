import time
import sql_handler
import var_calculator

while True:
    query = "select id, user_a_msgs, user_b_msgs, G, I from Users where last_var_assignment < (NOW() - INTERVAL 7 DAY)"
    result = sql_handler.execute_query(query)
    for i in result:
        user_id = i[0]
        user_a_msgs = i[1]
        user_b_msgs = i[2]
        g_prev = i[3]
        i_prev = i[4]
        G = (g_prev + var_calculator.VarCalculator.calculate_G(user_a_msgs, user_b_msgs)) / 2
        M = var_calculator.VarCalculator.calculate_M(user_a_msgs, user_b_msgs)
        I = var_calculator.VarCalculator.calculate_I(G)
        if I:
            I = i_prev + 1
        query = "update Users set last_var_assignment = NOW(), G = %s, M = %s, I = %s where id = %s"
        params = (G, M, I, user_id)
        sql_handler.execute_query(query, params)
    time.sleep(10)