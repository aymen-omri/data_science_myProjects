#!/usr/bin/env python
# coding: utf-8

#  ### import the necessary libraries

# In[7]:


import pandas as pd
import os 


# ### merge the 12 monthes of sales data into a single csv file 

# In[16]:


df = pd.read_csv(r"C:\Users\TRIEDENT\Desktop\aymen_work\data science\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data\Sales_April_2019.csv")
files = [file for file in os.listdir(r"C:\Users\TRIEDENT\Desktop\aymen_work\data science\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data")]

print(files)

all_months_data = pd.DataFrame()

for file in files:
    df=pd.read_csv("C:/Users/TRIEDENT/Desktop/aymen_work/data science/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/" + file)
    all_months_data= pd.concat([all_months_data, df])   
    
all_months_data.to_csv("C:/Users/TRIEDENT/Desktop/aymen_work/data science/all_data.csv" , index=False)


# In[26]:


####read the updated dataframe


# In[19]:


all_data = pd.read_csv("C:/Users/TRIEDENT/Desktop/aymen_work/data science/all_data.csv")
all_data


# In[20]:


all_data.head()


# In[21]:


all_data.info()


# In[22]:


all_data.describe()


# In[27]:


all_data.isnull()


# In[137]:


nan_df=all_data[all_data.isnull().values.any(axis=1)]
nan_df

all_data = all_data.dropna(how='all')
all_data.head()


# In[138]:


all_data = all_data[all_data['Order Date'].str[0:2]!='Or']
all_data


# In[139]:


all_data['month']=all_data['Order Date'].str[0:2]
all_data['month']=all_data['month'].astype('int32')
all_data


# In[140]:


all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])
all_data['sales'] = all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# ### best month sales ?

# In[141]:


result=all_data.groupby('month').sum()
result


# In[142]:


import matplotlib.pyplot as plt

months = range(1,13)
plt.bar(months,result['sales'])
plt.xticks(months)
plt.xlabel('Month number')
plt.ylabel('sales')
plt.show()


# ### what city had the highest number of sales ?

# In[143]:


all_data['city'] = all_data['Purchase Address'].apply(lambda x : x.split(',')[1] + ' ' + x.split(',')[2].split(' ')[1])
all_data.head()


# In[144]:


res = all_data.groupby('city').sum()
res


# In[145]:


cities = [city for city , df in all_data.groupby('city')]
plt.bar(cities,res['sales'])
plt.xticks(rotation=90)
plt.xlabel('cities')
plt.ylabel('sales')
plt.show()


# ### what time should we display advertisements to maximize likehood custumer's buying product ? 

# In[149]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['hour']= all_data['Order Date'].dt.hour
all_data['minute'] = all_data['Order Date'].dt.minute
all_data.head()


# In[159]:


resul = all_data.groupby('hour').sum()
resul


# In[162]:


hours = [hour for hour , df in all_data.groupby('hour')]
plt.plot(hours,resul['sales'])
plt.xticks(hours)
plt.grid()
plt.xlabel('hours')
plt.ylabel('sales')
#all_data.groupby(['hour']).count()
plt.show()


# ### what products are most ofen sold together?

# In[174]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x : ','.join(x) )
df =df[['Order ID' , 'Grouped']].drop_duplicates()
df.head()


# In[177]:


from itertools import combinations
from collections import Counter

count=Counter()
for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))
    
for key , value in count.most_common(10):
    print(key,value)


# ### what product sold the most ? why do think it sold the most ?

# In[187]:


products = all_data.groupby('Product').sum()
#products.head()
x1 = [product for product , df in all_data.groupby('Product')]
y1=products['Quantity Ordered']

plt.bar(x1,y1)
plt.grid()
plt.xlabel('Products')
plt.ylabel('Quantity Ordered')
plt.xticks(rotation=90 , size = 10 )
plt.show()


# In[201]:


y2 = all_data.groupby('Product').mean()['Price Each']

fig,ax1=plt.subplots()

ax2 = ax1.twinx()
ax1.bar(x1,y1)
ax2.plot(x1,y2)

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered' , color='g')
ax1.set_xticklabels(x1 , rotation='vertical')
ax2.set_ylabel('Price' , color="b")
plt.show()


# In[ ]:




