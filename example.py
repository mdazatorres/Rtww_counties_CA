# import rpy2.robjects as robjects
#
# # Define a Python function
# def calculate_mean(numbers):
#     r_code = """
#     result <- mean(numbers)
#     """
#     # Convert Python object to R object
#     r_numbers = robjects.FloatVector(numbers)
#
#     # Assign 'numbers' variable in the global R environment
#     robjects.globalenv['numbers'] = r_numbers
#
#     # Evaluate R code
#     robjects.r(r_code)
#
#     # Retrieve the result from R
#     result = robjects.globalenv['result'][0]
#
#     return result

# Call the function
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore", category=FutureWarning)
data=pd.read_excel('example_data.xlsx',index_col=False)
# Assuming you have already loaded the data and transformed 'SC2_N_norm_PMMoV' into 'y' and 'time' into 'tm'

# Fit ARIMA model
model = ARIMA(np.log(data["conc"]), order=(1, 0, 1))
result = model.fit()

# Calculate predicted values
yhat = np.exp(result.fittedvalues)
wc = 1
#kk = wc / min(yhat[yhat > 0].mean())  # Calculate kk
#k_av10 = wc / min(data["conc"].dropna())  # Calculate k_av10

# Recover cases
#data["Cases_N_av10"] = k_av10 * data["N_av10"]  # Cases from moving average
#data["Cases_N"] = kk * yhat  # Cases from ARIMA

pred = result.get_prediction()
quantiles = pred.conf_int(alpha=0.1)

# # Add quantiles to the DataFrame
data["median"] = yhat  # Cases from ARIMA
data["Lower_Quantile"] = np.exp(quantiles.iloc[:, 0])
data["Upper_Quantile"] = np.exp(quantiles.iloc[:, 1])

import matplotlib.pyplot as plt

plt.plot(data["median"])
plt.plot(data["Lower_Quantile"] )
plt.plot(data["Upper_Quantile"] )
##########


# tm < - 1: dim(data)[1]  # data[,"time"]
# y < - log(data[, "SC2_N_norm_PMMoV"])
# # y = ifelse(y==-Inf,NA,y)
# ## fit the model
# formula = y
# ~f(z, model="ar1")
# result = inla(formula, family="gaussian", data=list(y=y, z=tm))  # , E=E)
# # summary(result)
# # Cases respect to minimum concentration
# wc = 1
# # expected log concetration
# yhat = exp(result$summary.fitted.values)
# kk = wc / min(yhat$mean[yhat$mean > 0], na.rm = T)
# k_av10 = wc / min(data$N_av10, na.rm = T)
# # Recover cases from WW: proportional of cases
# data$Cases_N_av10 = k_av10 * data$N_av10  # Cases from moving average
# data$Cases_N = kk * yhat$mean  # Cases from INLA
