import numpy as np
from uncertainties import ufloat
from .stdVars import ureg

def getParamString(params, cov_mat, names):
    errors = np.sqrt(np.diag(cov_mat))
    return '\n'.join([(names[x] + ' = ' + str(params[x])
                       + ' +- ' + str(errors[x])) for x in range(len(params))])


def writeParamTxt(params, cov_mat, names, filename):
    with open(filename, 'w+') as f:
        f.write(getParamString(params, cov_mat, names))
        return

# Takes a pint unit and prints it
def getLatexCode(value):
    number = value.magnitude
    unit = value.units
    ret = f'{unit:Lx}'.replace('si', 'SI')
    return ret[:5] + f'{{{number}}}' + ret[5:]

# Thanks @Alexey for the idea!
# Warning: This method only works if pint is installed on your system!
def writeValueTex(value, filename):
    value *= ureg.m / ureg.m
    with open(filename, 'w+') as f:
        f.write(getValueTexString(value))

def writeValueTexSimple(value, filename):
    with open(filename, 'w+') as f:
        f.write(f'\\si{{{value}}}')

def getValueTexString(value):
    return ((f'{value:.fLx}').replace('+/-', '+-'))


def writeTexBlock(array, names, filename):
    with open(filename, 'w+') as f:
        f.write(r'\\'.join([names[x] + '=' +
                getValueTexString(array[x]) for x in range(len(array))]))
