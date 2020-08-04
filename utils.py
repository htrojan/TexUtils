import uncertainties.unumpy as unp
import numpy as np
from uncertainties import ufloat
from scipy.linalg import inv

def least_squares(A, measured, errors):
    size = A.shape[0]
    W = np.identity(size)
    row, col = np.diag_indices_from(W)
    W[row, col] = np.array(1/errors**2)
    # print(A, W)

    B = inv((A.T).dot(W).dot(A))
    C = (A.T).dot(W).dot(measured)

    mu = B.dot(C)
    mu_err = np.sqrt(np.diag(inv((A.T).dot(W).dot(A))))
    res = unp.uarray(mu, np.abs(mu_err))
    return res

def weighted_erroraverage(values, errors):
    w = 1/errors**2
    x = sum(values * w)
    delta = np.sqrt(1/sum(w))
    return ufloat(x, delta)

def measurement_average(values):
    std = np.std(values, ddof=1)
    mean = np.mean(values)
    N = len(values)
    return ufloat(mean, std/np.sqrt(N))

def measurement_average_error(values):
    v = unp.nominal_values(values)
    errors = unp.std_devs(values)

    # w = 1/errors**2
    # x = sum(v * w)
    # delta = np.sqrt(1/sum(w))
    N = len(values)
    delta = (1/N) * np.sqrt(sum(errors**2))

    mean = np.mean(v)
    std = (1/np.sqrt(N)) * np.std(v, ddof=1)

    return ufloat(mean, np.sqrt(std**2 + delta**2))
