from csv_functions import *

PI = 3.1415926535897
C_SPEED = 299792458

def kkr_refr_integ(w, ww, abs):
    return ww * abs / (ww ** 2 - w ** 2)

def integ_rec_tr(x_0, x_1, y_0, y_1):
    if y_1 >= y_0:
        return (y_0 + (abs(y_0 - y_1) / 2)) * (x_1-x_0)
    else:
        return (y_1 + (abs(y_0 - y_1) / 2)) * (x_1-x_0)

def integr_lists(X_list, Y_list, method):
    result = 0
    if method == 'triangle':
        for i in range(len(X_list)-1):
            result += integ_rec_tr(X_list[i], X_list[i+1], Y_list[i], Y_list[i+1])
    return result

def find_refr_from_abs(input_file, output_file):

    antl_spec = f'data/{input_file}'
    abs_func = csv_to_dict(antl_spec)
    w_numbs = list(abs_func.keys())

    file = open(f"data/{output_file}.txt", 'w')
    ref_coeffs = []

    for n in range(len(w_numbs)):
        # обход особой точки (это и есть v.p. интеграл)
        w_left = w_numbs[:n]
        w_right = w_numbs[n + 1:]

        integr_f_left = []
        integr_f_right = []

        for w_i in w_left:
            integr_f_left.append(kkr_refr_integ(w_numbs[n], w_i, abs_func[w_i]))
        for w_i in w_right:
            integr_f_right.append(kkr_refr_integ(w_numbs[n], w_i, abs_func[w_i]))

        n_refr_coeff = 1 + 2 * ((integr_lists(w_left, integr_f_left, 'triangle') + integr_lists(w_right, integr_f_right, 'triangle')) / PI)

        ref_coeffs.append(n_refr_coeff)
        file.write(f"{w_numbs[n]}; {n_refr_coeff}\n")
        print(f"{int((n / len(w_numbs)) * 100)} %, w = {w_numbs[n]} cm-1")
    print(f"refractive index was obtained from {input_file[:-4]}")
    file.close()
    return ref_coeffs

def full_scat_int(n_0, n_1, w, const, output_filename):
    #const = 24*PI**3*I0*V**2, where I0 = 1,  V in m3
    scatt_coeffs = {}
    file = open(f'{output_filename}.txt', 'w')
    for i in range(len(n_0)):
        n_0_ = n_0[i] ** 2
        n_1_ = n_1[i] ** 2
        w_ = w[i] ** 4 / 100 #wave length in m
        scatt = const * w_ * ((n_1_ - n_0_) / (n_1_ + 2 * n_0_)) ** 2
        file.write(f"{w[i]}; {scatt}\n")
        scatt_coeffs[w[i]] = scatt
        print(f"{round(100 * i / len(n_0))}%. scattaring calculation")
    file.close()
    print('DONE')
    return scatt_coeffs


abs_antlerit_file = 'our_antrelit_24Jul2019_r4.CSV'
refr_antlerit_file = 'calc_refr_result_' + abs_antlerit_file[:-4]


n_antlerit = find_refr_from_abs(abs_antlerit_file, refr_antlerit_file)

abs_C6_file = 'C6_300C_77K_5Dec2018.CSV'
refr_C6_file = 'calc_refr_result_' + abs_C6_file[:-4]

n_C6 = find_refr_from_abs(abs_C6_file, refr_C6_file)

particle_d = 5 #diametr, um
V = (4 / 3) * ((particle_d * 10**(-6)) ** 3)  * PI
sc_const = 24 * PI**3 * V**2
w_numbs = list(csv_to_dict('data/C6_300C_77K_5Dec2018.CSV').keys())
scat_spec = full_scat_int(n_C6, n_antlerit, w_numbs, sc_const, 'abs(C6-antl)_prtcl_sz_5000nm')