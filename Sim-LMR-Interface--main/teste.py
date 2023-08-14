import matplotlib.pyplot as plt
import pandas as pd 

r"""zhang_teo_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curva_ZHang_TE.csv", encoding='latin1', delimiter=';')
zhang_teo_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curva_ZHang_TM.csv", encoding='latin1', delimiter=';')
"""
zhang_comsol_TE = pd.read_csv(r"C:\Users\Adeilson\Downloads\Resultados Comsol\Zhang TE\Zhang_TE_1_47.txt", encoding='latin1', delimiter=',')
zhang_comsol_TM = pd.read_csv(r"C:\Users\Adeilson\Downloads\Curvas_Comsol(1)\Curvas_Comsol\Comsol_LMR_Zhang2022e_147_TM.txt", encoding='latin1', delimiter=',')

zhang_simlmr_TE = pd.read_csv(r"Zhang_TE_Reflectance_vs_analyte_1_47_TE.txt", encoding='latin1', delimiter=',')
zhang_simlmr_TM = pd.read_csv(r"Zhang_TM_Reflectance_vs_analyte_1_47_TM.txt", encoding='latin1', delimiter=',')

df_TE = [zhang_comsol_TE, zhang_simlmr_TE]
df_TM = [zhang_comsol_TM, zhang_simlmr_TM]

x_te = []
y_te = []

x_tm = []
y_tm = []

for n in df_TE: 
    x_te.append(list(n.iloc[:, 0])) 
    y_te.append(list(n.iloc[:, 1]))

for m in df_TM: 
    x_tm.append(list(m.iloc[:, 0])) 
    y_tm.append(list(m.iloc[:, 1]))


legenda = [ 'COMSOL', 'Sim-LMR']
grafico = ['-', '--']

figure1, ax1 = plt.subplots(dpi=200)
figure2, ax2 = plt.subplots(dpi=200)

for i in range(len(legenda)):
    ax1.plot(x_te[i], y_te[i], ls = grafico[i], linewidth=2.5)
    ax1.legend(legenda)
    ax1.set_title('Polarização TE')
    ax1.set_xlabel("Ângulo de incidência(°)")
    ax1.set_ylabel("Reflectância")
    ax1.grid(alpha=0.3)

    ax2.plot(x_tm[i], y_tm[i], ls = grafico[i], linewidth=2.5)
    ax2.set_title('Polarização TM')
    ax2.set_xlabel("Ângulo de incidência(°)")
    ax2.set_ylabel("Reflectância")
    ax2.legend(legenda)
    ax2.grid(alpha=0.3)


plt.show()



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