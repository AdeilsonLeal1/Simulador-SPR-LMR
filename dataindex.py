import pandas as pd 

perovskite_id = pd.read_csv("/home/adeilson/Downloads/Song-DJ4.csv")

wl = list(perovskite_id['wl'])
n = list(perovskite_id['n'])
k = list(perovskite_id['k'])

print(wl, n, k)


