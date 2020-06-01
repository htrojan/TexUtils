from collections import defaultdict


class TexTable:
    # data and names are arrays with the same dimensions
    def __init__(self, data, names, label='', caption='', roundPrecision=2,
                 defaultFormat=''):
        self.data = data
        self.names = names
        self.label = label
        self.caption = caption
        self.roundPrecision = roundPrecision
        self.rowOptions = defaultdict(list)
        self.rowFormats = {} # Empty dict for format strings
        self.defaultFormat = defaultFormat

    def gen_formatstring(self, roundingPrecision):
        return r'{:.' + str(roundingPrecision) + 'f' +'}'

    def get_defaultformat(self):
        if(self.defaultFormat == ''):
            return self.gen_formatstring(self.roundPrecision)
        else:
            return self.defaultFormat

    def gen_options(self):
        return '\n'.join([f'\\caption{{{self.caption}}}',
                         f'\\label{{{self.label}}}',
                          r'\centering']) + '\n'

    def gen_layout(self):
        a = '{'
        for i in range(len(self.names)):
            a += 'S['
            a += ','.join(self.rowOptions[i])
            a += ']'
        return a + '} \n'

    def gen_toprule(self):
        return ('\\toprule\n' +
                ' & '.join(['{' + x + '}' for x in self.names]) + r'\\' + '\n')

    def gen_midrule(self):
        a = '\\midrule\n'
        # v is the vertical index, h is the horizontal index
        for v in range(len(self.data[0])):
            column = []
            for (h, e) in enumerate(self.data):
                if(h in self.rowFormats):
                    num = self.rowFormats[h].format(e[v])
                else:
                    num = self.get_defaultformat().format(e[v])
                column.append(num.replace('+/-', '+-'))
            a += ' & '.join(column) + r'\\' + '\n'
        return a

    # Used to add options in [] within the toprule
    # row: The row for which the optio is specified
    # option: A string that is inserted into the rows [] in the toprule
    # statement
    def add_row_option(self, row, option):
        self.rowOptions[row].append(option)
        return

    def set_row_rounding(self, row, precision):
        self.set_custom_format(row, self.gen_formatstring(precision))
        return

    def set_custom_format(self, row, format):
        self.rowFormats[row] = format
        return

    def gen_botrule(self):
        return '\\bottomrule\n'

    def gen_tex(self):
        return ''.join([r"\begin{table}", self.gen_options(),
                        self.gen_inner_tex(),
                        r"\end{table}"])

    def gen_inner_tex(self):
        return ''.join([r"\begin{tabular}", self.gen_layout(), self.gen_toprule(),
                        self.gen_midrule(),
                        self.gen_botrule(), r"\end{tabular}"])

    def write_file(self, loc):
        with open(loc, 'w+') as f:
            f.write(self.gen_tex())


class Combined:
    # multirow specifies how many tables are made per row
    def __init__(self, tables, multirow = 2, caption='', label=''):
        self.tables = tables
        # As latex has problems with precise fractions, a small amount is subtracted
        self.subOptions = f'{(1 / multirow - 0.1 / multirow):0.2f}\\linewidth'
        self.caption = caption
        self.label = label
        return

    def gen_subtable(self, table):
        return ''.join([r"\begin{subtable}[t]",
                        f"{{{self.subOptions}}}",
                        table.gen_options(), table.gen_inner_tex(),
                        r"\end{subtable}"])

    def gen_subtable_array(self):
        tables = '\n'.join([self.gen_subtable(t) for t in self.tables])
        return tables

    def gen_tex(self):
        return ' '.join([r'\begin{table}', 
                         self.gen_subtable_array(), 
                         f"\\caption{{{self.caption}}}",
                         f"\\label{{{self.label}}}",
                         r'\end{table}'])

    def write_file(self, loc):
        with open(loc, 'w+') as f:
            f.write(self.gen_tex())

    def write_inner_tables(self, loc):
        with open(loc, 'w+') as f:
            f.write(self.gen_subtable_array())

