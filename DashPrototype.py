
# coding: utf-8

# In[27]:


import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("3201_1c2.csv", sep=",")
data = data.apply(pd.to_numeric)

del data['Numero']

mean = data.mean(axis=0,skipna=True)

data2 = pd.read_csv("3201_2c2.csv", sep=",")
data2 = data2.apply(pd.to_numeric)

# del data['Numero']

mean2 = data2.mean(axis=0,skipna=True)

df = pd.concat([mean,mean2], axis=1).transpose()
print(df)
print(data)
print(data2)


# In[2]:


df = df.rename(index={0:'T1', 1:'T2'})
print(df)
df.transpose().plot.bar(rot=0)


# In[3]:


print(data.iloc[0])
print(data2.iloc[0])

#df2 = pd.concat(data.iloc[0],data2.iloc[0])
df2 = pd.DataFrame([data.iloc[0],data2.iloc[0]], index = ["T1","T2"])
print(df2)


# In[4]:


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
new_t = [  "HIS", "BIO", "QUI", "FIS", "MAT", "DES","FRA","POR", "FIL", "SOC", "GEO"]
#new_t = [ "FRA","BIO", "GEO", "HIS", "FIS", "QUI", "FIL",  "SOC", "POR", "MAT", "DES"]
data = data.reindex(columns=new_t)
data2 = data2.reindex(columns=new_t)
df = pd.DataFrame(dict(
    r=data.iloc[0],
    theta= data.columns))
fig = px.line_polar(df, r='r', theta='theta', line_close=True)
fig.show()


# In[9]:


fig2 = go.Figure()

fig2.add_trace(go.Scatterpolar(
      r=data.iloc[0],
      theta=data.columns,
      fill='toself',
      name='T1'
))
fig2.add_trace(go.Scatterpolar(
      r=data2.iloc[0],
      theta=data.columns,
      fill='toself',
     name='T2'
))
fig2.add_trace(go.Scatterpolar(
      r=data.mean(),
      theta=data.columns,
      fill='toself',
     name='MeanT1'
))
fig2.add_trace(go.Scatterpolar(
      r=data2.mean(),
      theta=data.columns,
      fill='toself',
     name='MeanT2'
))

fig2.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 10]
    )),
  showlegend=False
)

fig2.show()


# In[7]:


print(df2)
print(data.mean())


# In[ ]:


print(pd.DataFrame([data,data2]))


# In[ ]:


import numpy as np
#data['T'] = "T1"
#T = ["T1","T2"]
T = ["T1"]
print(len(data.columns))
#print(data.groupby("T"))
datanp = np.array(data).reshape(len(data.index),len(data.columns) * len(T))
print(data)
midx = pd.MultiIndex.from_product([T, data.columns])
test = pd.DataFrame(datanp, index=datanp, columns=midx)


# In[39]:


diff = data2-data
disciplines = 2
for threshold in range(3,5):
    print(f"Threshold:{threshold}")
    print(diff[diff<-threshold].dropna(thresh=disciplines))

