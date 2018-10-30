import sys
sys.path.append('../') # Only needed because tabelle.py sits in parent folder

from table import TexTable

a = TexTable([[0, 2, 3], [4, 5, 6]], ['eins', 'zwei'])
a.addRowOption(0, ' ')
a.setRowRounding(1, 3)
a.writeFile('test.tex')
