import numpy as np
import types
import numbers
from uncertainties import ufloat
from uncertainties import unumpy as unp
from .stdVars import ureg
from .table import *

class Data:
    # _rows = dict()
    # _errors = dict()
    # _order = list()

    def __init__(self):
        self._rows = dict()
        self._errors = dict()
        self._order = list()

    def define_row(self, name, error=None, **kwargs):
        row = Row(**kwargs)
        self._rows[name] = row
        self._errors[name] = error
        self._order.append(name)
        return
    
    def unp(self, name):
        return self._rows[name].as_unumpy()

    def unp_array(self, name):
        return self._rows[name].as_unumpy_array()

    def load_data(self, txt, **kwargs):
        data = np.genfromtxt(txt, unpack=True, delimiter=',', **kwargs)

        if isinstance(data, np.ndarray) and data.shape is (1,0):
            name = self._order[0]
            error = self.compute_error(self._errors[name] ,data)
            self._rows[name].fill(data, error)
            return

        # print(data)
        for i, name in enumerate(self._order, 0):
            error = self.compute_error(self._errors[name] ,data[i])
            # print(f'Filling with: {data[i]}')
            self._rows[name].fill(data[i], error)
        return

    def add_row(self, name, data, error=None, **kwargs):
        row = Row(**kwargs)

        if isinstance(error, np.ndarray) or error is None:
            row.fill(data, error)
        else:
            row.fill(data, self.compute_error(error, data))
        self._rows[name] = row
        self._order.append(name)
        return

    def compute_error(self, error, data):
        error_obj = error
        if error_obj is None:
            return None
        if isinstance(error_obj, types.FunctionType):
            return error(data)
        if isinstance(error_obj, numbers.Number):
            return np.ones(data.shape) * error_obj 

    def __getitem__(self, key):
        return self._rows[key].as_numpy()

    def gen_textable(self):
        table_rows = list()
        names = list()
        for row_name in self._order:
            row = self._rows[row_name]
            # Create table row name
            name = row._displayname
            if row._unit is not None:
                if(name[-1] is '$'):
                    name = name[0:-1] + f' / ' + '{:Lx}'.format(row._unit) + '$'
                else:
                    name += f' / ' + '{:Lx}'.format(row._unit)

            names.append(name)
            # Create array of ufloats in case of errors
            if row._error is None:
                new_row = row.as_numpy()
                table_rows.append(new_row)
            else:
                row_value, row_err = row.as_numpy()
                new_row = [ufloat(r, e) for r, e in zip(row_value, row_err)]
                table_rows.append(new_row)
        
        table = TexTable(table_rows, names)
        return table


class Row:
    _data = np.array([])
    _error = None
    _displayname = str()
    _unit = None

    def __init__(self, displayname=str('display'), unit=None ):
        self._unit = unit
        self._displayname = displayname
        # print(displayname)
        return 
    
    def fill(self, data, error=None):
        self._data = data
        self._error = error
        return
    
    def as_unumpy(self):
        res = unp.uarray(self._data, std_devs = self._error)
        return res

    def as_unumpy_array(self):
        res = [ufloat(m, e) for m, e in zip(self._data, self._error)]
        return np.array(res)

    def as_numpy(self):
        if self._error is None:
            return self._data
        else:
            return self._data, self._error

    def __str__(self):
        if self._error is not None:
            errstr = np.array2string(self._error)
        else:
            errstr = 'None'
        return ('Name: ' + self._displayname + '\n'
        + 'Data: ' + np.array2string(self._data)
        + '\nError:' + errstr)
