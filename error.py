import uncertainties.unumpy as unp
import sympy

class Error:
    # Takes the function as a string and the values
    # As tuples ('a', ufloat(1, 0.1))
    def __init__(self, fun, *numbers):
        self.f = sympy.sympify(fun)
        print(f'f := {self.f}')
        self.numbers = numbers
        return

#  For this method:
#  The MIT License (MIT)

#  Copyright (c) 2014 PeP et al. e.V.

#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:

#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
    def getLatexError(self, err_vars=None):
        from sympy import Symbol, latex
        s = 0
        latex_names = dict()

        if err_vars is None:
            err_vars = self.f.free_symbols

        for v in err_vars:
            err = Symbol('latex_std_' + v.name)
            s += self.f.diff(v)**2 * err**2
            latex_names[err] = '\\sigma_{' + latex(v) + '}'

        return latex(sympy.sqrt(s), symbol_names=latex_names)

    def getNumericalError(self):
        args = sympy.symbols(
            ' '.join([self.numbers[i][0] for i in range(len(self.numbers))]))
        num = [self.numbers[i][1] for i in range(len(self.numbers))]
        res = sympy.lambdify(args, self.f, modules=[{'sqrt': unp.sqrt}])(*num)
        return res
