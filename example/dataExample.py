from data import *
from stdVars import ureg
import numpy as np

# Initialize a new data object and add column descriptions
data = Data()
data.define_row('row1', displayname=r'N', error= lambda x: np.sqrt(x)) # The error of the data is automatically calculated using the given formula
data.define_row('row2', displayname=r'Current', error=1, unit=ureg.volt) # Units are taken care of when generating latex output tables
# Load the data described in the data object. Errors are calculated automatically using the given error formulas
data.load_data('test.txt')

a = np.array([1,2,3,4,5])
data.add_row('row2', a, error=lambda x: np.sqrt(x), unit=ureg.ampere)
tab = data.gen_textable()
tab.set_caption('Hi, this is a caption')
tab.set_label('tab:table1')
tab.write_file('test_table.tex')