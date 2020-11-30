import matplotlib.pyplot as plt
import numpy as np


def f_1(x, u_1, u_2, k, k1, c, m):
    return u_2


def f_2(x, u_1, u_2, k, k1, c, m):
    return -(1/m)*(c*u_2 + k*u_1 + k1*u_1**3)
    #return -(1/m)*(c*u_2 + k*u_1)


def RK4_s(x_0, u1_0, u2_0, f_1, f_2, k, k1, c, m, h, v_max):
    u1 = u1_0
    u2 = u2_0
    k_1 = np.longdouble(h * f_1(x_0, u1_0, u2_0, k, k1, c, m))
    if abs(k_1) > v_max:
        return v_max, v_max
    l_1 = np.longdouble(h * f_2(x_0, u1_0, u2_0, k, k1, c, m))
    if abs(l_1) > v_max:
        return v_max, v_max
    k_2 = np.longdouble(h * f_1(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, k, k1, c, m))
    if abs(k_2) > v_max:
        return v_max, v_max
    l_2 = np.longdouble(h * f_2(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, k, k1, c, m))
    if abs(l_2) > v_max:
        return v_max, v_max
    k_3 = np.longdouble(h * f_1(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, k, k1, c, m))
    if abs(k_3) > v_max:
        return v_max, v_max
    l_3 = np.longdouble(h * f_2(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, k, k1, c, m))
    if abs(l_3) > v_max:
        return v_max, v_max
    k_4 = np.longdouble(h * f_1(x_0 + h, u1_0 + k_3, u2_0 + l_3, k, k1, c, m))
    if abs(k_4) > v_max:
        return v_max, v_max
    l_4 = np.longdouble(h * f_2(x_0 + h, u1_0 + k_3, u2_0 + l_3, k, k1, c, m))
    if abs(l_4) > v_max:
        return v_max, v_max
    u1 += np.longdouble(1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4))
    if abs(u1) > v_max:
        return v_max, v_max
    u2 += np.longdouble(1 / 6 * (l_1 + 2 * l_2 + 2 * l_3 + l_4))
    if abs(u2) > v_max:
        return v_max, v_max
    return u1, u2


def num_sol_3_task(k, k1, c, m, N_max, f_1, f_2, x_0, u1_0, u2_0, x_end, h, e, e_rb):
    v_max = 10e30
    c1 = 0
    c2 = 0
    u1_ds = u1_0
    u2_ds = u2_0
    S_nor = 0
    counter = 0
    flag = 0
    flag1 = 0

    C1 = [c1]
    C2 = [c2]
    U1 = [u1_0]
    U1_ds = [u1_0]
    U2 = [u2_0]
    U2_ds = [u2_0]
    H = [h]
    Error_arr = [0]
    X = [x_0]

    while (x_0+h <= x_end) or (flag1):
        if flag:
            break
        if counter > N_max:
            break
        temp_1, temp_2 = RK4_s(x_0, u1_0, u2_0, f_1, f_2, k, k1, c, m, h, v_max)
        temp1_ds, temp2_ds = RK4_s(x_0, u1_0, u2_0, f_1, f_2, k, k1, c, m, h / 2, v_max)
        temp1_ds, temp2_ds = RK4_s(x_0 + h / 2, temp1_ds, temp2_ds, f_1, f_2, k, k1, c, m, h / 2, v_max)
        if temp_1 == v_max or temp_2 == v_max or temp1_ds == v_max or temp1_ds == v_max:
            break
        S_nor = max(temp_1 - temp1_ds, temp_2 - temp2_ds, key=abs)/15
        #S_nor = abs(((temp_1 - temp1_ds) ** 2 + (temp_2 - temp2_ds) ** 2) ** (1 / 2))
        if abs(S_nor) > e or flag1:
            h = h / 2
            c1 += 1
        else:
            u1_0 = temp_1
            u2_0 = temp_2
            u1_ds = temp1_ds
            u2_ds = temp2_ds
            x_0 = x_0 + h
            H.append(h)
            U1_ds.append(u1_ds)
            U2_ds.append(u2_ds)
            U1.append(u1_0)
            U2.append(u2_0)
            X.append(x_0)
            Error_arr.append(S_nor*16)
            C2.append(c2)
            C1.append(c1)
            #counter = counter + 1
            if abs(S_nor) < e / 32:
                h = 2 * h
                c2 += 1
        if x_0+h>x_end:
            flag1 = 1
        else:
            flag1 = 0
        if x_0>x_end-e_rb:
            flag = 1
        counter = counter + 1

    data = [X, U1, U1_ds, Error_arr, H, C1, C2, U2, U2_ds, counter-c1] # выводим массив массивов для таблицы
    return data

def draw(data):
    fig, ax = plt.subplots()
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.plot(data[0], data[1], label='Обычный шаг', color='#00BFFF')
    ax.set_xlabel('X - время')
    ax.set_ylabel('V - смещение')
    ax.set_title('Смещение груза на пружине с демпфером \nотносительно положения равновесия \nГрафик V(x)')
    ax1.plot(data[0], data[7], label='Обычный шаг', color='#32CD32' )
    ax1.set_xlabel('X - время')
    ax1.set_ylabel("V' - скорость")
    ax1.set_title("Скорость груза \nГрафик V'(x)")
    ax2.plot(data[1], data[7], label='Обычный шаг', color='#FF0000')
    ax2.set_xlabel('V - смещение')
    ax2.set_ylabel("V' - скорость")
    ax2.set_title("Фазовый портрет")
    ax.plot(data[0], data[2], '.', label='Половинный шаг', color='#1E90FF')
    ax1.plot(data[0], data[8], '.', label='Половинный шаг', color='#3CB371')
    ax2.plot(data[2], data[8], '.', label='Половинный шаг', color='#DC143C')
    ax.legend()
    ax1.legend()
    ax2.legend()
    plt.show()


