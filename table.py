from collections import defaultdict


class TexTable:
    # data and names are arrays with the same dimensions
    def __init__(self, data, names, label='', caption='', roundPrecision=2):
        self.data = data
        self.names = names
        self.label = label
        self.caption = caption
        self.roundPrecision = roundPrecision
        self.rowOptions = defaultdict(list)

    def genOptions(self):
        return '\n'.join([f'\\caption{{{self.caption}}}',
                         f'\\label{{{self.label}}}',
                          r'\centering',
                          (r'\sisetup{round-mode = places, round-precision='
                           + str(self.roundPrecision) +
                           r', round-integer-to-decimal=true}')]) + '\n'

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
        for i in range(len(self.data[0])):
            a += ' & '.join([str(e[i]) for e in self.data]) + r'\\' + '\n'
        return a

    # Used to add options in [] within the toprule
    # row: The row for which the optio is specified
    # option: A string that is inserted into the rows [] in the toprule
    # statement
    def addRowOption(self, row, option):
        self.rowOptions[row].append(option)
        return

    def setRowRounding(self, row, precision):
        self.addRowOption(row, f'round-precision={precision}')

    def genBotrule(self):
        return '\\bottomrule\n'

    def genTex(self):
        return ''.join([r"\begin{table}", self.genOptions(), r"\begin{tabular}",
                        self.genLayout(), self.genToprule(), self.genMidrule(),
                        self.genBotrule(), r"\end{tabular}", r"\end{table}"])

    def writeFile(self, loc):
        with open(loc, 'w+') as f:
            f.write(self.genTex())
