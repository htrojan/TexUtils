import os
import sys
import math
import matplotlib
matplotlib.use('pgf')

import matplotlib.pyplot as plt
from .plotter import *


def set_preamble(path):
    matplotlib.rcParams.update({
        'pgf.preamble': f'\\input{{{path}}}'
    })


# Make plotting faster
def set_plotmode(mode):
    path = os.path.dirname(os.path.realpath(__file__))
    if (mode is 'fast'):
        matplotlib.rc_file(path + '/fast.rc')   
        set_preamble(path + '/header_matplotlib_fast.tex')
    elif (mode is 'pretty'):
        matplotlib.rc_file(path + '/pretty.rc')
        set_preamble(path + '/header_matplotlib_pretty.tex')
        print(path + 'header_matplotlib_pretty.tex')
    else:
        print('No mode recognized, using default.')

if 'release' in sys.argv:
    print('Release flag detected. Using pretty backend.')
    set_plotmode('pretty')
else:
    print('Using fast mode')
    set_plotmode('fast')