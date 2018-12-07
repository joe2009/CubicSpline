
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from math import sqrt
from sklearn.metrics import mean_squared_error
from patsy import dmatrix
from scipy import interpolate


# In[3]:


# read dataset
data = pd.read_csv("uswages.csv")
data.head()


# In[4]:


## data exploration ##
data.describe()


# In[5]:


print(data.info())


# In[6]:


## exper vs wage ##
data_x = data[['exper']]
data_y = data[['wage']]

#visualize the relationship between experience and wage
plt.scatter(data_x, data_y, facecolor = 'None', edgecolor = 'k', alpha = 0.3)
plt.suptitle('Fig 1. Relationship between experience and wage', fontsize=12)
plt.xlabel('experience')
plt.ylabel('wage')
plt.show()

# remove outlier
data_ylim = data.loc[data['wage']<= 4000]
wage = data_ylim[['wage']]
exper_x = data_ylim[['exper']]

#visualize the relationship between experience and wage
plt.scatter(exper_x, wage, facecolor = 'None', edgecolor = 'k', alpha = 0.3)
plt.suptitle('Fig 2. Relationship between experience and wage (remove outlier)', fontsize=12)
plt.xlabel('experience')
plt.ylabel('wage')
plt.show()


# In[7]:


# test model with simple linear regression

#add an intercept (beta_0) to our model
exper_x = sm.add_constant(exper_x)  

# model fitting
model = sm.OLS(wage, exper_x).fit()
print(model.summary())

# find fitted value
predictions1 = model.predict(exper_x) 

# data visualization
plt.scatter(exper_x['exper'], wage, facecolor = 'None', edgecolor = 'k', alpha = 0.3)
plt.plot(exper_x['exper'], predictions1, color = 'green', linewidth = 1.5)
plt.suptitle('Fig 3. Relationship between experience and wage: using simple linear regression', fontsize=12)
plt.xlabel('experience')
plt.ylabel('wage')
plt.show()

# Calculating RMSE value
rms1 = sqrt(mean_squared_error(wage, predictions1))
print(rms1)


# In[8]:


# refit model using polynomial regression, degree = 2
# "exper" with degree = 2

exper_x['exper2'] = np.power(exper_x['exper'], 2)

# model fitting
model2 = sm.OLS(wage, exper_x).fit()
print(model2.summary())

# find fitted value
predictions2 = model2.predict(exper_x)


# reduce samples down to 100
x_lim = np.linspace(start = exper_x['exper'].min(), stop = exper_x['exper'].max(), num = 100)
x_lim_df = pd.DataFrame({'exper':x_lim})
x_lim_df['exper2'] = np.power(x_lim_df['exper'], 2)
x_lim_df = sm.add_constant(x_lim_df) 

# find fitted value using x_lim
fit_reduce = model2.predict(x_lim_df)

# data visualization
plt.scatter(exper_x['exper'], wage, facecolor = 'None', edgecolor = 'k', alpha = 0.3)
plt.plot(x_lim_df[['exper']], fit_reduce, color = 'blue', linewidth = 1.5, label='experience with degree = 2')
plt.legend()
plt.suptitle('Fig 4. Relationship between experience and wage: using polynomial regression (degree = 2)', fontsize=12)
plt.xlabel('experience')
plt.ylabel('wage')
plt.show()

# Calculating RMSE value
rms2 = sqrt(mean_squared_error(wage, predictions2))
print(rms2)


# In[34]:


# refit model using polynomial regression, degree = 4
# "exper" with degree = 4
exper_x['exper3'] = np.power(exper_x['exper'], 3)
exper_x['exper4'] = np.power(exper_x['exper'], 4)

# model fitting
model3 = sm.OLS(wage, exper_x).fit()
print(model3.summary())

# find fitted value
predictions3 = model3.predict(exper_x)


# reduce samples down to 100
x_lim = np.linspace(start = exper_x['exper'].min(), stop = exper_x['exper'].max(), num = 100)
x_lim_df = pd.DataFrame({'exper':x_lim})
x_lim_df['exper2'] = np.power(x_lim_df['exper'], 2)
x_lim_df['exper3'] = np.power(x_lim_df['exper'], 3)
x_lim_df['exper4'] = np.power(x_lim_df['exper'], 4)
x_lim_df = sm.add_constant(x_lim_df) 

# find fitted value using x_lim
fit_reduce2 = model3.predict(x_lim_df)

# data visualization
plt.scatter(exper_x['exper'], wage, facecolor = 'None', edgecolor = 'k', alpha = 0.3)
plt.plot(x_lim_df[['exper']], fit_reduce2, color = 'purple', linewidth = 1.5, label='experience with degree up to 5')
plt.legend()
plt.suptitle('Fig 5. Relationship between experience and wage: using polynomial regression (degree = 4)', fontsize=12)
plt.xlabel('experience')
plt.ylabel('wage')
plt.show()

# Calculating RMSE value
rms3 = sqrt(mean_squared_error(wage, predictions3))
print(rms3)


# In[33]:


## cubic regression ##
# cubic spline with 3 knots (quantile) at 8, 15, 27
cubic_x1 = dmatrix("bs(data, knots = (8, 15, 27), include_intercept = False)", {"data": exper_x[['exper']]}, return_type = 'dataframe')
model4 = sm.GLM(wage, cubic_x1).fit()
print(model4.summary())

# find fitted value
predictions4 = model4.predict(cubic_x1)

# reduce samples down to 100
x_lim = np.linspace(start = exper_x[['exper']].min(), stop = exper_x[['exper']].max(), num = 100)


# find fitted value using x_lim
fit_reduce3 = model4.predict(dmatrix(formula_like = "bs(train, knots = (8, 15, 27), include_intercept = False)", data = {"train": x_lim}, return_type = 'dataframe'))

# plot spline
plt.scatter(exper_x[['exper']], wage, facecolor='None', edgecolor='k', alpha=0.1)
plt.plot(x_lim, fit_reduce3, color='r', linewidth = 1.5, label='Specifying 3 knots, knots = (8, 15, 27)')
plt.legend()
plt.suptitle('Fig 6. Relationship between experience and wage: using cubic regression, knots = (8, 15, 27)', fontsize=12)
plt.ylim(0, 5000)
plt.xlabel('experience')
plt.ylabel('wage')
plt.show()

# Calculating RMSE value
rms4 = sqrt(mean_squared_error(wage, predictions4))
print(rms4)


# In[36]:


## cubic regression ##
# cubic spline with 3 knots (quantile) at 15, 30, 45
cubic_x2 = dmatrix("bs(data, knots = (15, 30, 45), include_intercept = False)", {"data": exper_x[['exper']]}, return_type = 'dataframe')
model5 = sm.GLM(wage, cubic_x2).fit()
print(model5.summary())

# find fitted value
predictions5 = model5.predict(cubic_x2)

# reduce samples down to 100
x_lim = np.linspace(start = exper_x[['exper']].min(), stop = exper_x[['exper']].max(), num = 100)


# find fitted value using x_lim
fit_reduce4 = model5.predict(dmatrix(formula_like = "bs(train, knots = (15, 30, 45), include_intercept = False)", data = {"train": x_lim}, return_type = 'dataframe'))

# plot spline
plt.scatter(exper_x[['exper']], wage, facecolor='None', edgecolor='k', alpha=0.1)
plt.plot(x_lim, fit_reduce4, color='y', linewidth = 1.5, label='Specifying 3 knots, knots = (15, 30, 45)')
plt.legend()
plt.suptitle('Fig 7. Relationship between experience and wage: using cubic regression, knots = (15, 30, 45)', fontsize=12)
plt.ylim(0, 5000)
plt.xlabel('experience')
plt.ylabel('wage')
plt.show()

# Calculating RMSE value
rms5 = sqrt(mean_squared_error(wage, predictions5))
print(rms5)


# In[30]:


## summary ##
# overlay three regression curve
plt.scatter(exper_x[['exper']], wage, facecolor='None', edgecolor='k', alpha=0.1)
plt.plot(exper_x['exper'], predictions1, color = 'green', linewidth = 1.5, label = 'Simple Linear Regression')
plt.plot(x_lim_df['exper'], fit_reduce, color = 'blue', linewidth = 1.5, label='Polynomial Regression, experience degree = 2')
plt.plot(x_lim_df['exper'], fit_reduce2, color = 'purple', linewidth = 1.5, label='Polynomial Regression, experience up to degree = 4')
plt.plot(x_lim, fit_reduce2, color='r', linewidth = 1.5, label='Cubic Regrssion, knots = (8, 15, 27)')
plt.plot(x_lim, fit_reduce3, color='y', linewidth = 1.5, label='Cubic Regrssion, knots = (15, 30, 45)')
plt.legend()
plt.suptitle('Fig 8. Relationship between experience and wage', fontsize=12)
plt.ylim(0, 5000)
plt.xlabel('experience')
plt.ylabel('wage')
plt.show()


# In[37]:


# compare root of mse
model = ['SLR', 'Polynomial (degree = 2)', 'Polynomial (degree = 4)', 'Spline(knots = 8, 15, 27)', 'Spline(knots = 15, 30, 45)']
RMSE = [rms1, rms2, rms3, rms4, rms5]
compare = pd.DataFrame({'Model':model, 'RMSE':RMSE})
print(compare)

