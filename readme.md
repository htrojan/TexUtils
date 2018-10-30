# TexUtils
Just a collection of useful python scripts to make your tex life easier

## table.py
Automatically generates tex tables from your acquired data.
<p> IMPORTANT: You have to use the package sinunitx in your .tex file if you want to import the
           generated file into your main document</p>
Usage:
<pre> <code>
x, y = np.genfromtxt('data.txt')
table = TexTable([x, y], ['Y / V', 'X / Ampere'], label='table:mytable', caption='Description')
table.writeFile('myTable.tex')
</code></pre>

And in tex just include:

<pre> <code>
\begin{document}
....
\input{myTable.tex}
...
\end{document}
</code> </pre>

The TexTable takes two necessary arguments: 

1. First an array with your data rows
2. Second an array with the names the rows have

<p>Optional arguments are:</p>

- label - The label of the table
- caption - The Caption of the table
- roundPrecision - How many places should be rounded (default 2)
