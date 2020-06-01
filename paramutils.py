import numpy as np
from uncertainties import ufloat
from .stdVars import ureg

def get_paramstring(params, cov_mat, names):
    errors = np.sqrt(np.diag(cov_mat))
    return '\n'.join([(names[x] + ' = ' + str(params[x])
                       + ' +- ' + str(errors[x])) for x in range(len(params))])


def write_param_txt(params, cov_mat, names, filename):
    with open(filename, 'w+') as f:
        f.write(get_paramstring(params, cov_mat, names))
        return

# Thanks @Alexey for the idea!
# Warning: This method only works if pint is installed on your system!
def write_texvalue(value, filename, scientific = False):
    value *= ureg.m / ureg.m
    with open(filename, 'w+') as f:
        f.write(get_texstring(value, scientific))

def write_texvalue_simple(value, filename, form=r'{:.0f}'):
    with open(filename, 'w+') as f:
        n = form.format(value.magnitude)
        f.write(f'\\num{{{n}}} \\; {value.units:Lx}'
    .replace('electron_volt', 'electronvolt'))
                

def get_texstring(value, scientific = False):
    if(scientific):
        return ((f'{value:.eLx}').replace('+/-', '+-').replace('(', '')
        .replace(')', ''))
    return ((f'{value:.fLx}').replace('+/-', '+-')
    .replace('electron_volt', 'electronvolt'))


def write_texblock(array, names, filename):
    with open(filename, 'w+') as f:
        f.write(r'\\'.join([names[x] + '=' +
                get_texstring(array[x]) for x in range(len(array))]))
