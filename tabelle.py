class TexTable:
    # data and names are arrays with the same dimensions
    def __init__(self, data, names, label='', caption='', roundPrecision=2):
        self.data = data
        self.names = names
        self.label = label
        self.caption = caption
        self.roundPrecision = roundPrecision

    def genOptions(self):
        return '\n'.join([f'\\caption{{{self.caption}}}',
                         f'\\label{{{self.label}}}',
                          r'\centering',
                          (r'\sisetup{round-mode = places, round-precision='
                           + str(self.roundPrecision) +
                           r', round-integer-to-decimal=true}')]) + '\n'

    def genLayout(self):
        return '{' + 'S ' * len(self.names) + '}\n'

    def genToprule(self):
        return ('\\toprule\n' +
                ' & '.join(['{' + x + '}' for x in self.names]) + r'\\' + '\n')

    def genMidrule(self):
        a = '\\midrule\n'
        for i in range(len(self.data[0])):
            a += ' & '.join([str(e[i]) for e in self.data]) + r'\\' + '\n'
        return a

    def genBotrule(self):
        return '\\bottomrule\n'

    def genTex(self):
        return ''.join([r"\begin{table}", self.genOptions(), r"\begin{tabular}",
                        self.genLayout(), self.genToprule(), self.genMidrule(),
                        self.genBotrule(), r"\end{tabular}", r"\end{table}"])

    def writeFile(self, loc):
        with open(loc, 'w+') as f:
            f.write(self.genTex())


a = TexTable([[0, 2, 3], [4, 5, 6]], ['eins', 'zwei'])
a.writeFile('test.tex')
print(len(a.data))
print(a.genTex())