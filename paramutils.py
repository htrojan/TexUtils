import numpy as np
from uncertainties import ufloat


def getParamString(params, cov_mat, names):
    errors = np.sqrt(np.diag(cov_mat))
    return '\n'.join([(names[x] + ' = ' + str(params[x])
                       + ' +- ' + str(errors[x])) for x in range(len(params))])


def writeParamTxt(params, cov_mat, names, filename):
    with open(filename, 'w+') as f:
        f.write(getParamString(params, cov_mat, names))
        return


# Thanks @Alexey for the idea!
# Warning: This method only works if pint is installed on your system!
def writeValueTex(value, filename):
    with open(filename, 'w+') as f:
        f.write((f'{value:Lx}').replace('+/-', '+-'))
