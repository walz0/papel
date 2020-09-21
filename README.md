# papel
A raw text document router for writing papers in APA format

# Instructions
- Write your paper within raw.txt
- Press return twice to create a new paragraph
```
The quick brown fox jumps over the 
lazy dog. The quick brown fox jumps
over the lazy dog.

This is a new paragraph because it
is separated by a new line from the
previous paragraph.
```
- Separate your works cited, or references section with a return followed by a forward slash
```
The quick brown fox jumps over the lazy dog
/
Doe, J. (2020). Papel README. Retrieved from https://github.com/walz0/papel/README.md
```
- Press return twice to create a new citation
```
The quick brown fox jumps over the lazy dog
/
Walz, A. (2020). Papel README. 
Retrieved from https://github.com/walz0/papel/README.md

Walz, A. (2020). A new citation. Retrieved from https://github.com/walz0/papel/README.md
```
- When you are finished writing, run papel.py. This will generate output.html which will contain your formatted paper. To convert to pdf, open output.html in your browser and press CTRL+P, select print to PDF. Standard APA margins are 1 inch on all sides, make sure to disable headers / footers.
- If you wish to change some of the styling options you can run papel.py with additional parameters:
```
  -s :: font-size
  -i :: text-indent
  -h :: line-height
  
  Syntax: python3 main.py -s 18 -i 50 -h 20
```
- You may pass any number of these parameters followed by an integer.
