import matplotlib as mpl  
import matplotlib.pyplot as plt  
import pandas as pd
import numpy as np

# output = "reports/data_exploration/line_feature.html"
time_segments_type = snakemake.params["time_segments_type"]
data_yield = pd.read_csv("data/raw/person1/galaxyfit_heartrate_raw.csv")

x = data_yield['local_date_time']
y = data_yield['heartrate']

s = data_yield['local_date_time']
total = len(s)

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xticks(np.arange(0, total+1, 14))
ax.plot(x, y, linewidth=1.0)
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig('reports/data_exploration/line_graph.png')
