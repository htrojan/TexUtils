# Utilities for plotting
import numpy as np
from numpy import polyfit
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.lines as mlines
from uncertainties import ufloat
from .stdVars import *
from .table import *


class Chain:
    def __init__(self, alwaysExecute=True):
        self.actions = list()
        self.attributes = dict()
        self.data = dict()
        self.alwaysExecute = alwaysExecute

    def add_link(self, cls):
        self.actions.append(cls)
        if self.alwaysExecute is True:
            self.execute()
        return self

    def execute(self):
        for i in self.actions:
            i.execute()
        self.actions = list()
        return self

    def new_data(self, f, new_name, *names):
        return self.add_link(AddData(self, f, new_name, names))

    def table(self, toSave, label='tab:fig', caption='', output='build/table.tex', rounding=[], names=None):
        self.add_link(TexSave(self, toSave, label, caption, output, rounding, names=names))
        return self

    # Convenience methods for callink add_link
    def plot(self, xname, yname, fmt='+', label='label'):
        self.add_link(Plot(self, xname, yname, fmt=fmt, label=label))
        return self

    def addline(self, x, y, plot='plot'):
        self.add_link(PlotLine(self, x, y, plot))
        return self

    def manipulate(self, f, *datanames):
        self.add_link(DataManipulation(self, f, *datanames))
        return self

    # Calculates linear regression and plots the result if not disabled
    def linReg(self, xname, yname, output='params', plot=True):
        self.add_link(LinRegress(self, xname, yname, output))
        x = self.data[xname]

        if plot is False:
            return self

        def m(chain, x, y):
            x_new = np.array([x[0].magnitude, x[-1].magnitude]) * x[0].units
            y_new = ( x_new.magnitude * chain.attributes[output][0].nominal_value 
                + chain.attributes[output][1].nominal_value)
            chain.data['x_new'] = x_new
            chain.data['y_new'] = y_new

        self.manipulate(m, xname, yname)
        self.plot('x_new', 'y_new', fmt='-')
        return self

    def describePlot(self, xname, yname, useData=True,
    minor_ticks=None):
        self.add_link(PlotDescription(self, xname, yname, useData, minor_ticks=minor_ticks))
        return self

    def savePlot(self, filename, plot='plot'):
        self.add_link(SavePlot(self, filename, plot))
        return self

class PlotLine():
    def __init__(self, chain, x, y, plot='plot'):
        self.chain = chain
        self.x = x
        self.y = y
        self.plot = plot
        print(x, y)

    def execute(self):
        ax = self.chain.attributes[self.plot][1]
        print(self.x, self.y)
        xmin, xmax = ax.get_xbound()
        ymin, ymax = ax.get_ybound()
        lv = mlines.Line2D([xmin, self.x], [self.y, self.y], linestyle='--')
        lh = mlines.Line2D([self.x, self.x], [ymin, self.y], linestyle='--')
        ax.add_line(lv)
        ax.add_line(lh)

class DataManipulation():
    def __init__(self, chain, f, *names):
        """Passes the datasets corresponding to the given names into
        a function\n
        names: Names of the data columns\n
        f: Function that takes chain and parameters as input"""
        self.chain = chain
        self.names = names
        self.f = f

    def execute(self):
        params = list()
        # Collect data sets to pass to function
        for n in self.names:
            params.append(self.chain.data[n])

        self.f(self.chain, *params)

class AddData():
    def __init__(self, chain, f, new_name, *names):
        """Takes a lambda that takes the data sets named in 'names' as input 
        and returns a new data set named 'new_name'"""
        self.chain = chain
        self.f = f
        self.new_name = new_name
        self.names = names[0]

    def execute(self):
        params = list()
        # Collect data sets to pass to function
        print(self.names)
        for n in self.names:
            params.append(self.chain.data[n])
        # Give the returned array a unit if it has none
        ret = self.f(*params) * (ureg.m / ureg.m)
        self.chain.data[self.new_name] = ret

class TexSave():
    def __init__(self, chain, toSave, label, caption, output, rounding,
    names=None):
        self.chain = chain
        self.toSave = toSave
        self.label = label
        self.caption = caption
        self.output = output
        self.rounding = rounding
        self.names = names

    def execute(self):
        data = [self.chain.data[n].magnitude for n in self.toSave]
        if self.names is None:
            names = [f'${n} / {self.chain.data[n].units:Lx}$' for n in self.toSave]
        else:
            names = [f'${name} / {self.chain.data[n].units:Lx}$' 
            for n, name in zip(self.toSave, self.names)]

        t = TexTable(data, names, label=self.label, caption=self.caption)

        for i, r in enumerate(self.rounding):
            t.set_row_rounding(i, r)
        self.chain.attributes['table'] = t
        t.write_file(self.output)


class Data(Chain):
    # Data stores key value pairs 
    def __init__(self, **data):
        super().__init__()
        self.data = data


class TxtData(Data):
    
    def __init__(self, filename, names, units=None):
        """filename: Name of the .txt file to load the data from. \n
        names: List of names for each loaded data set."""

        loaded = np.genfromtxt(filename, unpack=True, delimiter='\t')
        # Set dimensionless as the standard unit
        if units is None:
            units = [ureg.m / ureg.m] * len(names)

        data = dict()
        # Init dict with data
        for name, dat, u in zip(names, loaded, units):
            data[name] = dat * u

        return super().__init__(**data)

class Plot():
    def __init__(self, chain, xname, yname, plot='plot', fmt='+', label='Label'):
        self.chain = chain
        self.xname = xname
        self.yname = yname
        self.plot = plot
        self.fmt = fmt
        self.label = label
        chain.attributes.setdefault(plot, plt.subplots())

    def printType(self):
        print('Plot')

    def execute(self):
        print(f'Plot {self.xname} -> {self.yname} on plot {self.plot}')
        x = self.chain.data[self.xname]
        y = self.chain.data[self.yname]
        ax = self.chain.attributes[self.plot][1]
        fig = self.chain.attributes[self.plot][0]
        ax.plot(x, y, self.fmt, label=self.label)

class PlotDescription():
    def __init__(self, chain, xname, yname, useData=True, plot='plot', minor_ticks = None):
        self.chain = chain
        self.xname = xname
        self.yname = yname
        self.useData = useData
        self.plot = plot
        self.minor_ticks = minor_ticks

    def execute(self):
        ax = self.chain.attributes[self.plot][1]
        fig = self.chain.attributes[self.plot][0]
        if self.useData is True:
            x = self.chain.data[self.xname]
            y = self.chain.data[self.yname]
            ax.set_xlabel(f'${self.xname} / {x.units:Lx}$')
            ax.set_ylabel(f'${self.yname} / {y.units:Lx}$')
        else:
            ax.set_xlabel(self.xname)
            ax.set_ylabel(self.yname)

        if self.minor_ticks is not None:
            ax.get_xaxis().set_minor_locator(matplotlib.ticker.MultipleLocator(self.minor_ticks))


class SavePlot():
    def __init__(self, chain, filename, plot):
        self.chain = chain
        self.filename = filename
        self.plot = plot

    def execute(self):
        ax = self.chain.attributes[self.plot][1]
        fig = self.chain.attributes[self.plot][0]
        ax.legend()
        ax.grid()
        # ax.minorticks_on()
        fig.tight_layout()
        fig.savefig(self.filename)

class LinRegress():
    def __init__(self, chain, xname, yname, output):
        self.chain = chain
        self.xname = xname
        self.yname = yname
        self.output = output

    def execute(self):
        print('LinRegress')
        x = self.chain.data[self.xname]
        y = self.chain.data[self.yname]
        params, cov = np.polyfit(x, y, deg=1, cov=True)
        errors = np.sqrt(np.diag(cov))
        m = ufloat(params[0], errors[0])
        b = ufloat(params[1], errors[1])
        self.chain.attributes[self.output] = [m, b]