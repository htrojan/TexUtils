import sys
sys.path.append('../') # Only needed because tabelle.py sits in parent folder

from uncertainties import ufloat
from error import Error

e = Error('A + sqrt(b)', ('A', ufloat(3, 0.1)), ('b', ufloat(4, 0.5)))
print(e.getLatexError())
print(e.getNumericalError())
