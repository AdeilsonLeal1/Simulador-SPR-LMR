import pandas as pd
import matplotlib.pyplot as plt

files = ['Stelling', 'Chen', 'Song-DJ4']

df = [pd.read_csv(fr'C:\Users\Adeilson\Downloads\{i}.csv') for i in files]

font = dict(size=14, family='Times New Roman')  # Font and size
plt.rc('font', **font)

#Stelling
fig, a = plt.subplots(dpi = 200)
a.plot(df[0]['wl']*1000,df[0]['n'],'-b',df[0]['wl']*1000,df[0]['k'], '-r', linewidth=3)
a.grid()
a.legend(["Real part","Imaginary part"])
a.set_xlabel("Wavelength (nm)")
a.set_ylabel("Refractive index (RIU)")

#Chen
fig, b = plt.subplots(dpi = 200)
b.plot(df[1]['wl']*1000,df[1]['n'],'-b',df[1]['wl2']*1000,df[1]['k'],  '-r', linewidth=3)
b.grid()
b.legend(["Real part","Imaginary part"])
b.set_xlabel("Wavelength (nm)")
b.set_ylabel("Refractive index (RIU)")

#Song-DJ4
fig, b = plt.subplots(dpi = 200)
b.plot(df[2]['wl']*1000,df[2]['n'],'-b',df[2]['wl']*1000,df[2]['k'], '-r', linewidth=3)
b.grid()
b.legend(["Real part","Imaginary part"])
b.set_xlabel("Wavelength (nm)")
b.set_ylabel("Refractive index (RIU)")

plt.show()