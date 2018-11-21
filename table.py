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

    def genFormatString(self, roundingPrecision):
        return r'{:.' + str(roundingPrecision) + 'f' +'}'

    def getDefaultFormat(self):
        if(self.defaultFormat == ''):
            return self.genFormatString(self.roundPrecision)
        else:
            return self.defaultFormat

    def genOptions(self):
        return '\n'.join([f'\\caption{{{self.caption}}}',
                         f'\\label{{{self.label}}}',
                          r'\centering']) + '\n'

    def genLayout(self):
        a = '{'
        for i in range(len(self.names)):
            a += 'S['
            a += ','.join(self.rowOptions[i])
            a += ']'
        return a + '} \n'

    def genToprule(self):
        return ('\\toprule\n' +
                ' & '.join(['{' + x + '}' for x in self.names]) + r'\\' + '\n')

    def genMidrule(self):
        a = '\\midrule\n'
        # v is the vertical index, h is the horizontal index
        for v in range(len(self.data[0])):
            column = []
            for (h, e) in enumerate(self.data):
                if(h in self.rowFormats):
                    num = self.rowFormats[h].format(e[v])
                else:
                    num = self.getDefaultFormat().format(e[v])
                column.append(num)
            a += ' & '.join(column) + r'\\' + '\n'
        return a

    # Used to add options in [] within the toprule
    # row: The row for which the optio is specified
    # option: A string that is inserted into the rows [] in the toprule
    # statement
    def addRowOption(self, row, option):
        self.rowOptions[row].append(option)
        return

    def setRowRounding(self, row, precision):
        self.rowFormats[row] = self.genFormatString(precision)
        return

    def genBotrule(self):
        return '\\bottomrule\n'

    def genTex(self):
        return ''.join([r"\begin{table}", self.genOptions(),
                        self.genInnerTex(),
                        r"\end{table}"])

    def genInnerTex(self):
        return ''.join([r"\begin{tabular}", self.genLayout(), self.genToprule(),
                        self.genMidrule(),
                        self.genBotrule(), r"\end{tabular}"])

    def writeFile(self, loc):
        with open(loc, 'w+') as f:
            f.write(self.genTex())


class Combined:
    def __init__(self, tables, subOptions = r'.5\linewidth', caption=''):
        self.tables = tables
        self.subOptions = subOptions
        self.caption = caption
        return

    def genSubTable(self, table):
        return ''.join([r"\begin{subtable}",
                        f"{{{self.subOptions}}}",
                        table.genOptions(), table.genInnerTex(),
                        r"\end{subtable}"])

    def genSubTableArray(self):
        tables = '\n'.join([self.genSubTable(t) for t in self.tables])
        return tables

    def genTex(self):
        return ' '.join([r'\begin{table}', f"\\caption{{{self.caption}}}",
                         self.genSubTableArray(), r'\end{table}'])

    def writeFile(self, loc):
        with open(loc, 'w+') as f:
            f.write(self.genTex())

    def writeInnerTables(self, loc):
        with open(loc, 'w+') as f:
            f.write(self.genSubTableArray())

