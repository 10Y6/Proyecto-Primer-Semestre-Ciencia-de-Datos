import plotly.express as px
import Functions as fnc

data_in_situ = fnc.data_in_situ()
data_onei = fnc.data_onei()
data_online = fnc.data_online()
data_exch_rate = fnc.load_exch_rate()

for i in data_online:
  print(i)

