#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')
from urllib.request import urlopen
from bs4 import BeautifulSoup

# In[2]:


url = "http://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)

# In[3]:


soup = BeautifulSoup(html, 'lxml')
type(soup)

# In[4]:


title = soup.title
print(title)

# In[5]:


text = soup.get_text()
print(soup.text)

# In[6]:


soup.find_all('a')

# In[7]:


all_links = soup.find_all("a")
for link in all_links:
    print(link.get("href"))

# In[8]:


rows = soup.find_all('tr')
print(rows[:10])

# In[10]:


for row in rows:
    row_td = row.find_all('td')
print(row_td)
type(row_td)

# In[13]:


str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
print(cleantext)

# In[27]:


import re

list_rows = []
for row in rows:
    #     print('row',row)
    cells = row.find_all('td')
    #     print('cells',cells)
    str_cells = str(cells)
    #     print('str_c',str_cells)
    clean = re.compile('<.*?>')
    #     print(clean)
    clean2 = (re.sub(clean, '', str_cells))
    #     print(clean2)
    list_rows.append(clean2)
# print(list_rows)
print(clean2)
type(clean2)

# In[28]:


# print(list_rows)
df = pd.DataFrame(list_rows)
df.head(10)

# In[30]:


df1 = df[0].str.split(',', expand=True)
df1.head(10)

# In[32]:


df1[0] = df1[0].str.strip('[')
df1.head(10)

# In[36]:


col_labels = soup.find_all('th')
print(col_labels)

# In[38]:


all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
print(all_header)

# In[43]:


df2 = pd.DataFrame(all_header)
df2.head()

# In[44]:


df3 = df2[0].str.split(',', expand=True)
df3.head()

# In[45]:


frames = [df3, df1]

df4 = pd.concat(frames)
df4.head(10)

# In[48]:


df5 = df4.rename(columns=df4.iloc[0])
df5.head(2)

# In[49]:


df5.info()
df5.shape

# In[51]:


df6 = df5.dropna(axis=0, how='any')
df6.info()
df6.shape

# In[81]:


df7.rename(columns={'[Place': 'Place'}, inplace=True)
df7.rename(columns={' Team]': 'Team'}, inplace=True)
df7.head()
df7['Team'] = df7['Team'].str.strip(']')
df7.head()

# In[53]:


df7.rename(columns={'[Place': 'Place'}, inplace=True)
df7.rename(columns={' Team]': 'Team'}, inplace=True)
df7.head()

# In[54]:


df7['Team'] = df7['Team'].str.strip(']')
df7.head()

# In[82]:


time_list = df7[' Chip Time'].tolist()

# You can use a for loop to convert 'Chip Time' to minutes

time_mins = []
for i in time_list:

    if len(i.split(':')) == 2:
        m = i.split(':')[0]
        s = i.split(':')[1]
    elif len(i.split(':')) == 3:
        h = i.split(':')[0]
        m = i.split(':')[1]
        s = i.split(':')[2]
    math = (int(h) * 3600 + int(m) * 60 + int(s)) / 60
    time_mins.append(math)
# print(time_mins)


# In[83]:


df7['runner_mins'] = time_mins
df7.head()

# In[97]:


# df7.drop(columns=[])
df7.describe(include=[np.number])

# In[90]:


from pylab import rcParams

rcParams['figure.figsize'] = 15, 5

df7.boxplot(column='runner_mins')
plt.grid(True, axis='y')
plt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])

# In[92]:


x = df7['runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor': 'black'})
plt.show()

# In[94]:


f_fuko = df7.loc[df7[' Gender'] == ' F']['runner_mins']
m_fuko = df7.loc[df7[' Gender'] == ' M']['runner_mins']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor': 'black'}, label='Female')
sns.distplot(m_fuko, hist=False, kde=True, rug=False, hist_kws={'edgecolor': 'black'}, label='Male')
plt.legend()

# In[96]:


g_stats = df7.groupby(" Gender", as_index=True).describe()
print(g_stats)

# In[99]:


df7.boxplot(column='runner_mins', by=' Gender')
plt.ylabel('Chip Time')
plt.suptitle("")
