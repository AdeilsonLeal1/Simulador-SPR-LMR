import matplotlib.pyplot as plt
import pandas as pd 
from numpy import *
from scipy.signal import butter, filtfilt

fwhm_TM = list()
da_TM = list()
def butter_lowpass_filter(data, cutoff, fs, order):
    # Get the filter coefficients 
    b, a = butter(order, cutoff, btype='low', fs = fs)
    y = filtfilt(b, a, data)
    return y

def find_max_min(seq):
        max_list = []
        min_list = []

        for i in range(1, len(seq) - 1):
            if i == 1 and seq[i] > seq[i+1]: 
                max_list.append((i, seq[i]))
            elif i == (len(seq) - 2) and seq[i] >= seq[i-1]:
                max_list.append((i, seq[i]))
            elif seq[i] > seq[i-1] and seq[i] > seq[i+1]:
                max_list.append((i, seq[i]))
            elif seq[i] < seq[i-1] and seq[i] < seq[i+1]:
                min_list.append((i, seq[i]))
        
        return max_list, min_list

def calc_FWHM(xlist, ylist):
    fwhm_TM = list()
    da_TM = list()
    for n in range(len(xlist)):
        fwhm_ = []
        da_ = []
        curve = butter_lowpass_filter(ylist[n], cutoff=2, fs=40, order=5)
        xlist_ = xlist[n]
        max_list, min_list = find_max_min(curve)
        for m in range(len(max_list)-1):
            lambda_i = list(xlist_[max_list[m][0]:max_list[m+1][0]])
            y = list(curve[max_list[m][0]:max_list[m+1][0]])

            id_min = y.index(min(y))  # Position of the minimum point of the curve

            y_left = y[0:(id_min+1)]
            y_right = y[id_min:len(y)]

            y_mx_left = max(y_left)
            y_mn_left = min(y_left)

            y_mx_right = max(y_right)
            y_mn_right = min(y_right)

            y_med_left = (y_mx_left + y_mn_left)/2
            y_med_right = (y_mx_right + y_mn_right)/2

            y_med = (y_med_left + y_med_right)/2
            #y_med = (1+min(y))/2    
            #y_med = (max(y) + min(y))/2 
            #y_med = max(y)/2
            #y_med = y_mx_right
            

                # Gaur's methodology for calculating FWHM
            y_left = asarray(y_left)
            y_right = asarray(y_right)
            idx1 = (abs(y_left - y_med_left)).argmin() 
            idx2 = (abs(y_right - y_med_right)).argmin() 
            x1= lambda_i[idx1]
            x2= lambda_i[id_min + idx2]
            
            f = sqrt(abs((x2-x1))**2 + abs(y_med_right - y_med_left)**2)
            
            fwhm_.append(round(f, 6))
            da_.append(round(1/f, 6))

            fwhm_TM.append(fwhm_)
            da_TM.append(da_)

        fwhm_TM = [[row[i] for row in fwhm_TM] for i in range(len(fwhm_TM[0]))]
        da_TM = [[row[i] for row in da_TM] for i in range(len(da_TM[0]))]

    return fwhm_TM, da_TM

gaur_ref_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Default Dataset (2).csv", encoding='latin1')
gaur_simlmrspr_TM = pd.read_csv(r"C:\Users\Adeilson\Documents\UFCG\Pesquisa\Sim-LMR_SPR\Simulação_Power_transmitted_vs_analyte_1_33_TM.txt", encoding='latin1')

#df_TE = [wu_ref_TE, wu_comsol_TE, wu_simlmr_TE]
df_TM = [gaur_simlmrspr_TM, gaur_ref_TM ]

#x_te = []
#y_te = []

x_tm = []
y_tm = []

#for n in df_TE: 
    #x_te.append(list(n.iloc[:, 0])) 
    #y_te.append(list(n.iloc[:, 1]))

for m in df_TM: 
    x_tm.append(list(m.iloc[:, 0])) 
    y_tm.append(list(m.iloc[:, 1]))


legenda = ['Sim-LMR+SPR', 'Gaur et. al (GAUR et al., 2022)']
grafico = ['-', '--']


font = dict(family='Arial')  # Font and size
plt.rc('font', **font)

#figure1, ax1 = plt.subplots(dpi=250)
figure2, ax2 = plt.subplots(dpi=250)

for i in range(len(legenda)):
    #ax1.plot(x_te[i], y_te[i], ls = grafico[i], linewidth=2.5)
    #ax1.legend(legenda)
    #ax1.set_title('S-Polarization (TE)')
    #ax1.set_xlabel("Angle of incidence (°)")
    #ax1.set_ylabel("Reflectance")
    #ax1.grid(alpha=0.3)

    ax2.plot(x_tm[i], y_tm[i], ls = grafico[i], linewidth=2)
    #ax2.set_title('P-Polarization (TM)')
    ax2.set_xlabel("Comprimento de Onda (nm)")
    ax2.set_ylabel("Potencia Transmitida Normalizada")
    ax2.legend(legenda)
    ax2.grid(alpha=0.3)


fwhm_TM, da_TM = calc_FWHM(x_tm, y_tm)

print(fwhm_TM, da_TM)
plt.show()

r"""wu_ref_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Default Dataset (1).csv", encoding='latin1')
wu_ref_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Default Dataset 2.csv", encoding='latin1')

wu_comsol_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Resultados Comsol\wu TE\Wu_TE_1_34.txt", encoding='latin1')
wu_comsol_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Wu_TM_1_34.txt", encoding='latin1')

wu_simlmr_TE = pd.read_csv(r"wu_TE_Reflectance_vs_analyte_1_34_TE.txt", encoding='latin1')
wu_simlmr_TM = pd.read_csv(r"wu_TM_Reflectance_vs_analyte_1_34_TM.txt", encoding='latin1')"""

r"""Yadollahzadeh_ref_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\WIM_Ref_TE.csv", encoding='latin1')
Yadollahzadeh_ref_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\WIM_Ref_TM.csv", encoding='latin1')

Yadollahzadeh_comsol_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\WIM_1_42_TE.txt", encoding='latin1')
Yadollahzadeh_comsol_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\WIM_1_42_TM.txt", encoding='latin1')

Yadollahzadeh_simlmr_TE = pd.read_csv(r"Yadollahzadeh_simlmr_Reflectance_vs_analyte_1_42_TE.txt", encoding='latin1')
Yadollahzadeh_simlmr_TM = pd.read_csv(r"Yadollahzadeh_simlmr_Reflectance_vs_analyte_1_42_TM.txt", encoding='latin1')"""

r"""zhang_teo_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curva_ZHang_TE.csv", encoding='latin1', delimiter=';')
zhang_teo_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curva_ZHang_TM.csv", encoding='latin1', delimiter=';')

zhang_comsol_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Resultados Comsol\Zhang TE\Zhang_TE_1_47.txt", encoding='latin1', delimiter=',')
zhang_comsol_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curvas_Comsol(1)\Curvas_Comsol\Comsol_LMR_Zhang2022e_147_TM.txt", encoding='latin1', delimiter=',')

zhang_simlmr_TE = pd.read_csv(r"Zhang_TE_Reflectance_vs_analyte_1_47_TE.txt", encoding='latin1', delimiter=',')
zhang_simlmr_TM = pd.read_csv(r"Zhang_TM_Reflectance_vs_analyte_1_47_TM.txt", encoding='latin1', delimiter=',')
"""

r"""
saini_teo_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curva_Saini_Teor_TE.csv", encoding='latin1', delimiter=';')
saini_teo_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curva_Saini_Teor_TM.csv", encoding='latin1', delimiter=';')

saini_exp_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curva_Saini_Exp_TE.csv", encoding='latin1', delimiter=';')
saini_exp_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curva_Saini_Exp_TM.csv", encoding='latin1', delimiter=';')

saini_simlmr_TE = pd.read_csv(r"Saini_TE_Reflectance_vs_analyte_1_45_TE.txt", encoding='latin1', delimiter=',')
saini_simlmr_TM = pd.read_csv(r"Saini_TM_Reflectance_vs_analyte_1_45_TM.txt", encoding='latin1', delimiter=',')

saini_comsol_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curvas_Comsol(1)\Curvas_Comsol\Comsol_LMR_Saini2019e_145_TE.txt", encoding='latin1', delimiter=',')
saini_comsol_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curvas_Comsol(1)\Curvas_Comsol\Comsol_LMR_Saini2019e_145_TM.txt", encoding='latin1', delimiter=',')

df_TE = [saini_teo_TE, saini_exp_TE, saini_comsol_TE, saini_simlmr_TE]
df_TM = [saini_teo_TM, saini_exp_TM, saini_comsol_TM, saini_simlmr_TM]"""