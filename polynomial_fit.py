# -*- coding: utf-8 -*-
"""
- fit data using least squares regression
- curve_fit_func: returns a function of x that is a polynomial fit to the data

use with: 
    from polynomial_fit import curve_fit_func
    xdata = [some x points]
    ydata = [some y points]
    power = the heighest power in the polynomial (ex. 3=cubic)
    chisqr, fit_coeficients, func = curve_fit_func(power, xdata, ydata)
    interpolated_val = func(some new x value)

@date: April 12 - 2021
@author: Isaac Lehman
"""

import numpy as np
from scipy.optimize import curve_fit


""" returns a function that computes x**n """
def powers(n):
    return lambda x: x**n

"""
 Returns a polynomial function
   params are a, b, c, d, ...
       - for: a + bx + cx**2 + ...
       - initial guess is 1.0's
"""
def make_poly_func(power=1):
    power_fncs = [powers(i) for i in range(power+1)]
    return [1.0 for i in range(power+1)], lambda x, *params: sum([p(x)*params[i] for i, p in enumerate(power_fncs)])

"""
 Returns a function of x that is a polynomial fit to the data
"""
def curve_fit_func(power, xdata, ydata):
    if power > len(xdata):
        raise ValueError("ERROR: you must have at least one more data point than your power.")
    # make the function
    ysigma = np.std(ydata) * np.ones(len(xdata),float) # 1 standard deviation of the data set
    func_guess, func = make_poly_func(power)
    # fit the function
    coeficients, pcov = curve_fit(func, xdata, ydata, p0=func_guess, sigma=ysigma, absolute_sigma=False)
    # calculate the chi squared error in the fit
    chisqr = 0
    for i in range(len(xdata)):
        chisqr += ( ( func(xdata[i], *coeficients)-ydata[i] )/ysigma[i] )**2
    # return error, fit coeficients, and the actual f(x)
    return chisqr, coeficients, lambda x: func(x, *coeficients)



