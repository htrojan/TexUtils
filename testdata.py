from data import *
from stdVars import ureg
import numpy as np

data = Data()
data.define_row('row1', displayname=r'N', error= lambda x: np.sqrt(x))
data.define_row('row2', displayname=r'Current', error=1, unit=ureg.volt)
data.load_data('test.txt')

a = np.array([1,2,3,4,5])
data.add_row('row2', a, error=lambda x: np.sqrt(x), unit=ureg.ampere)
tab = data.gen_textable()
tab.set_caption('Hi, this is a caption')
tab.set_label('tab:table1')
tab.write_file('test_table.tex')

# data_with_poissonerror = data.unp('a')
# # print(data._rows['a'])
# # print(data.unp('a'))
# # print(data['a'])